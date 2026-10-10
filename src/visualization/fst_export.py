"""
Documentation generator for the ResumeLens transducers.

It builds every transducer of the normalization stage (the same
objects used by resume_normalizer.py) and generates:

1. diagrams/fst/<name>.dot   graphical representation (Graphviz DOT)
   diagrams/fst/<name>.svg   rendered diagram (only if Graphviz "dot"
                             is installed)
2. docs/06a_fst_formal_definitions.md
                             complete 7-tuple of every transducer,
                             with the full δ / ω table

Because everything is generated from the transducers themselves,
the diagrams and the tables always match the implementation.

Usage (from the root of the project):

    python -m src.visualization.fst_export
"""

import shutil
import subprocess
from pathlib import Path

from src.model.normalization.canonical_vocabulary import (
    LANGUAGES_VOCABULARY,
    FRAMEWORKS_VOCABULARY,
    DATABASES_VOCABULARY,
    TOOLS_VOCABULARY,
    OTHER_VOCABULARY,
    ACADEMIC_VOCABULARY,
)
from src.model.normalization.fst_builder import (
    END_MARKER,
    FINAL_STATE,
    INITIAL_STATE,
    build_dictionary_fst,
    build_experience_fst,
)


ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS_DIR = ROOT / "diagrams" / "fst"
DOC_FILE = ROOT / "docs" / "06a_fst_formal_definitions.md"

SPACE = "␣"
EPSILON = "ε"


# Name, title and vocabulary of every dictionary transducer.
DICTIONARY_TRANSDUCERS = [
    ("M_LANG", "Programming languages", LANGUAGES_VOCABULARY),
    ("M_FW", "Frameworks and libraries", FRAMEWORKS_VOCABULARY),
    ("M_DB", "Databases", DATABASES_VOCABULARY),
    ("M_TOOLS", "Tools and technologies", TOOLS_VOCABULARY),
    ("M_OTHER", "Other qualifications", OTHER_VOCABULARY),
    ("M_ACAD", "Academic qualifications", ACADEMIC_VOCABULARY),
]

# Meaning of the states of M_EXP (see build_experience_fst).
EXPERIENCE_STATE_MEANING = {
    "q0": "nothing has been read",
    "q1": "reading the number of years (digits are copied)",
    "plus": "\"+\" after the number",
    "sp": "space after the number",
    "y1": "\"y\"",
    "y2": "\"ye\"",
    "y3": "\"yea\"",
    "unit": "\"year\" or \"yr\"",
    "units": "\"years\" or \"yrs\"",
    "b1": "space after the unit",
    "o1": "\"o\" of \"of\"",
    "of": "\"of\"",
    "b2": "space after \"of\"",
    "prof": "\"professional\"",
    "b3": "space after \"professional\"",
    "exp": "\"experience\"",
    FINAL_STATE: "accepting state (end marker read)",
}


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _show(symbol: str) -> str:
    """Make a symbol visible (the space is drawn as ␣)."""

    return SPACE if symbol == " " else symbol


def _output_text(output: list[str]) -> str:
    """Output of a transition as text (ε if it is empty)."""

    return " ".join(output) if output else EPSILON


def _state_key(state: str):
    """Order q0, q1, q2, ..., qN and finally qf."""

    if state == FINAL_STATE:
        return (2, 0, state)

    if state[0] == "q" and state[1:].isdigit():
        return (0, int(state[1:]), state)

    return (1, 0, state)


def _ordered_states(fst) -> list[str]:
    """States in order of appearance (initial state first, qf last)."""

    seen = [INITIAL_STATE]

    for s_from, _, s_to, _ in fst.transition_list:
        for state in (s_from, s_to):
            if state not in seen and state != FINAL_STATE:
                seen.append(state)

    return seen + [FINAL_STATE]


def _prefix_of_states(fst) -> dict[str, str]:
    """
    Prefix read to reach each state of a dictionary transducer.
    (In a prefix tree there is only one path to each state.)
    """

    prefix = {INITIAL_STATE: ""}

    for s_from, symbol, s_to, _ in fst.transition_list:
        if symbol != END_MARKER:
            prefix[s_to] = prefix[s_from] + symbol

    return prefix


def _input_alphabet(fst) -> list[str]:
    symbols = {symbol for _, symbol, _, _ in fst.transition_list}
    symbols.discard(END_MARKER)

    return sorted(symbols) + [END_MARKER]


def _output_alphabet(fst) -> list[str]:
    tokens = []

    for _, _, _, output in fst.transition_list:
        for token in output:
            if token not in tokens:
                tokens.append(token)

    return tokens


# -------------------------------------------------------------------
# Graphical representation (DOT)
# -------------------------------------------------------------------

def _grouped_edges(fst) -> list[tuple[str, str, str]]:
    """
    Join the transitions that go between the same pair of states.

    - Ten transitions that copy a digit are drawn as one edge
      "0-9 / copy".
    - Several transitions with output ε are drawn as one edge
      "a, b / ε".
    """

    groups: dict[tuple[str, str], list[tuple[str, list[str]]]] = {}

    for s_from, symbol, s_to, output in fst.transition_list:
        groups.setdefault((s_from, s_to), []).append((symbol, output))

    edges = []

    for (s_from, s_to), items in groups.items():
        symbols = [symbol for symbol, _ in items]
        copies = all(output == [symbol] for symbol, output in items)

        if len(items) == 10 and copies and all(s.isdigit() for s in symbols):
            label = "0-9 / copy"
        elif all(not output for _, output in items):
            label = ", ".join(_show(s) for s in symbols) + f" / {EPSILON}"
        else:
            label = "\\n".join(
                f"{_show(symbol)} / {_output_text(output)}"
                for symbol, output in items
            )

        edges.append((s_from, s_to, label))

    return edges


def to_dot(fst, name: str) -> str:
    """Graphviz DOT description of a transducer."""

    lines = [
        f'digraph {name} {{',
        '    rankdir=LR;',
        '    node [shape=circle, fontname="Helvetica", fontsize=11];',
        '    edge [fontname="Helvetica", fontsize=10];',
        '    start [shape=point];',
        f'    {FINAL_STATE} [shape=doublecircle];',
        f'    start -> {INITIAL_STATE};',
    ]

    for s_from, s_to, label in _grouped_edges(fst):
        label = label.replace('"', '\\"')
        lines.append(f'    "{s_from}" -> "{s_to}" [label="{label}"];')

    lines.append("}")

    return "\n".join(lines) + "\n"


def write_diagrams(transducers: list[tuple[str, str, object]]) -> list[Path]:
    """Write the .dot files and render them as .svg when possible."""

    DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)
    dot_program = shutil.which("dot")
    written = []

    for name, _, fst in transducers:
        dot_file = DIAGRAMS_DIR / f"{name.lower()}.dot"
        dot_file.write_text(to_dot(fst, name), encoding="utf-8")
        written.append(dot_file)

        if dot_program:
            svg_file = dot_file.with_suffix(".svg")
            subprocess.run(
                [dot_program, "-Tsvg", str(dot_file), "-o", str(svg_file)],
                check=True,
            )
            written.append(svg_file)

    return written


# -------------------------------------------------------------------
# Formal definitions (Markdown)
# -------------------------------------------------------------------

def _symbols_set(symbols: list[str]) -> str:
    return "{ " + ", ".join(_show(s) for s in symbols) + " }"


def formal_definition(name: str, title: str, fst, is_dictionary: bool) -> str:
    """Complete 7-tuple of a transducer, as Markdown."""

    states = _ordered_states(fst)
    sigma = _input_alphabet(fst)
    gamma = _output_alphabet(fst)

    if is_dictionary:
        states = sorted(states, key=_state_key)
        prefix = _prefix_of_states(fst)
        meaning = {
            state: (f"prefix `{prefix[state].replace(' ', SPACE)}`"
                    if prefix.get(state) else "prefix ε (nothing read)")
            for state in states
        }
        meaning[FINAL_STATE] = "accepting state (end marker read)"
    else:
        meaning = {
            state: EXPERIENCE_STATE_MEANING.get(state, "")
            for state in states
        }
        for state in states:
            if not meaning[state]:
                meaning[state] = "reading a word of the expression"

    lines = [
        f"## {name} — {title}",
        "",
        "```text",
        f"{name} = (Q, Σ, Γ, δ, ω, q0, F)",
        "",
        f"Q  = {{ {', '.join(states)} }}",
        f"     |Q| = {len(states)}",
        f"Σ  = {_symbols_set(sigma)}",
        f"     |Σ| = {len(sigma)}",
        f"Γ  = {{ {', '.join(gamma)} }}",
        f"     |Γ| = {len(gamma)}",
        f"q0 = {INITIAL_STATE}",
        f"F  = {{ {FINAL_STATE} }}",
        "```",
        "",
        f"Number of transitions: {len(fst.transition_list)}.",
        "",
        f"Diagram: `diagrams/fst/{name.lower()}.svg` "
        f"(source: `diagrams/fst/{name.lower()}.dot`).",
        "",
        "### States",
        "",
        "| State | Meaning |",
        "| :--- | :--- |",
    ]

    lines += [f"| `{state}` | {meaning[state]} |" for state in states]

    lines += [
        "",
        "### Transition relation δ and output relation ω",
        "",
        "`δ(state, input)` is the column *To*, "
        "and `ω(state, input)` is the column *Output*.",
        "",
        "| From | Input | To | Output |",
        "| :--- | :---: | :--- | :--- |",
    ]

    for s_from, symbol, s_to, output in fst.transition_list:
        lines.append(
            f"| `{s_from}` | `{_show(symbol)}` | `{s_to}` "
            f"| `{_output_text(output)}` |"
        )

    lines += [
        "",
        "Any pair (state, input) that is not in the table has no "
        "transition, so the input is rejected.",
        "",
    ]

    return "\n".join(lines)


def summary_table(transducers) -> str:
    lines = [
        "| Transducer | States (size of Q) | Input symbols (size of Σ) "
        "| Output symbols (size of Γ) | Transitions |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]

    for name, _, fst in transducers:
        lines.append(
            f"| `{name}` | {len(fst.states)} | {len(_input_alphabet(fst))} "
            f"| {len(_output_alphabet(fst))} | {len(fst.transition_list)} |"
        )

    return "\n".join(lines)


def write_formal_definitions(transducers) -> Path:
    parts = [
        "# ResumeLens – Formal Definitions of the Transducers",
        "",
        "> This file is generated automatically by "
        "`python -m src.visualization.fst_export`. Do not edit it by hand: "
        "change `canonical_vocabulary.py` or `fst_builder.py` and run the "
        "script again.",
        "",
        "It contains the complete 7-tuple `M = (Q, Σ, Γ, δ, ω, q0, F)` of "
        "every transducer of the normalization stage. The design and the "
        "construction method are explained in `06_fst_design.md`.",
        "",
        "Notation:",
        "",
        f"- `{SPACE}` is the space character.",
        f"- `{END_MARKER}` is the end-of-input marker appended to every input.",
        f"- `{EPSILON}` is the empty output.",
        "",
        "## Summary",
        "",
        summary_table(transducers),
        "",
    ]

    for name, title, fst in transducers:
        parts.append(formal_definition(name, title, fst, name != "M_EXP"))

    DOC_FILE.write_text("\n".join(parts), encoding="utf-8")

    return DOC_FILE


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def build_all() -> list[tuple[str, str, object]]:
    transducers = [
        (name, title, build_dictionary_fst(vocabulary))
        for name, title, vocabulary in DICTIONARY_TRANSDUCERS
    ]
    transducers.append(
        ("M_EXP", "Professional experience", build_experience_fst())
    )

    return transducers


def main() -> None:
    transducers = build_all()

    for path in write_diagrams(transducers):
        print(f"written: {path.relative_to(ROOT)}")

    print(f"written: {write_formal_definitions(transducers).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
