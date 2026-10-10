"""
Documentation generator for the ResumeLens profile automata.

It builds the four automata of the classification stage (the same
objects used by resume_classifier.py) and generates:

1. diagrams/dfa/<name>.dot   transition diagram (Graphviz DOT)
   diagrams/dfa/<name>.svg   rendered diagram (only if Graphviz "dot"
                             is installed)
2. On the console (option --markdown): the formal definition of
   every automaton (5-tuple, state table, δ table and transition
   matrix) in Markdown, as used in docs/07_automata_design.md.

Because everything is generated from the automata themselves,
the diagrams and the tables always match the implementation.

Usage (from the root of the project):

    python -m src.visualization.dfa_export
    python -m src.visualization.dfa_export --markdown A_FS
"""

import shutil
import subprocess
import sys
from pathlib import Path

from src.model.classification.automata_builder import (
    INITIAL_STATE,
    ResumeLensDFA,
    build_all_profile_dfas,
)
from src.model.classification.profile_patterns import AUTOMATON_NAMES


ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS_DIR = ROOT / "diagrams" / "dfa"

EMPTY = "∅"


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def ordered_states(dfa: ResumeLensDFA) -> list[str]:
    """q0, q1, ..., qn (order of the canonical tokens)."""

    return sorted(dfa.state_token, key=lambda state: int(state[1:]))


def alphabet(dfa: ResumeLensDFA) -> list[str]:
    """Σ in canonical order."""

    return [token for group in dfa.groups for token in group.tokens]


def _group_regex(tokens: tuple[str, ...]) -> str:
    """
    Regular expression of a non-empty ordered selection of the
    tokens of a group:  t1 t2? ... tk? | t2 t3? ... tk? | ... | tk
    """

    if len(tokens) == 1:
        return tokens[0]

    options = []

    for i, token in enumerate(tokens):
        rest = " ".join(f"{other}?" for other in tokens[i + 1:])
        options.append(f"{token} {rest}".strip())

    return "(" + " | ".join(options) + ")"


def language_regex(dfa: ResumeLensDFA) -> str:
    """Regular expression of the language recognized by the DFA."""

    parts = []

    for group in dfa.groups:
        regex = _group_regex(group.tokens)
        parts.append(regex if group.mandatory else f"({regex})?")

    return "\n    ".join(parts)


# -------------------------------------------------------------------
# Graphical representation (DOT)
# -------------------------------------------------------------------

def to_dot(dfa: ResumeLensDFA, name: str) -> str:
    """
    Graphviz DOT description of an automaton.

    The states of each group are drawn inside a box labeled with the
    group and whether it is mandatory or optional.
    """

    finals = set(dfa.final_state_names)

    lines = [
        f"digraph {name} {{",
        "    rankdir=LR;",
        "    nodesep=0.5;",
        "    ranksep=1.4;",
        "    splines=true;",
        '    node [shape=circle, fontname="Helvetica", fontsize=11];',
        '    edge [fontname="Helvetica", fontsize=9];',
        "    start [shape=point];",
        f"    start -> {INITIAL_STATE};",
    ]

    if INITIAL_STATE in finals:
        lines.append(f"    {INITIAL_STATE} [shape=doublecircle];")

    for number, group in enumerate(dfa.groups, start=1):
        kind = "mandatory" if group.mandatory else "optional"
        style = "solid" if group.mandatory else "dashed"

        lines += [
            f"    subgraph cluster_g{number} {{",
            f'        label="G{number}: {group.name} ({kind})";',
            '        fontname="Helvetica"; fontsize=10;',
            f"        style={style}; color=gray50;",
        ]

        for state in ordered_states(dfa):
            if dfa.state_group[state] == number:
                shape = "doublecircle" if state in finals else "circle"
                lines.append(f"        {state} [shape={shape}];")

        lines.append("    }")

    for s_from, symbol, s_to in dfa.transition_list:
        lines.append(f'    {s_from} -> {s_to} [label="{symbol}"];')

    lines.append("}")

    return "\n".join(lines) + "\n"


def write_diagrams(automata: dict[str, ResumeLensDFA]) -> list[Path]:
    """Write the .dot files and render them as .svg when possible."""

    DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)
    dot_program = shutil.which("dot")
    written = []

    for profile, dfa in automata.items():
        name = AUTOMATON_NAMES[profile]
        dot_file = DIAGRAMS_DIR / f"{name.lower()}.dot"
        dot_file.write_text(to_dot(dfa, name), encoding="utf-8")
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
# Formal definition (Markdown)
# -------------------------------------------------------------------

def formal_definition(dfa: ResumeLensDFA, name: str) -> str:
    """5-tuple, state table, δ table and transition matrix."""

    states = ordered_states(dfa)
    sigma = alphabet(dfa)
    finals = [s for s in states if s in set(dfa.final_state_names)]

    lines = [
        "```text",
        f"{name} = (Q, Σ, δ, q0, F)",
        "",
        f"Q  = {{ {', '.join(states)} }}",
        f"     |Q| = {len(states)}",
        f"Σ  = {{ {', '.join(sigma)} }}",
        f"     |Σ| = {len(sigma)}",
        f"q0 = {INITIAL_STATE}",
        f"F  = {{ {', '.join(finals)} }}",
        f"δ  : Q × Σ → Q  (partial function, {len(dfa.transition_list)} transitions;",
        "     the missing pairs go to the trap state)",
        "```",
        "",
        "#### States",
        "",
        "| State | Meaning (last token read) | Group | Accepting |",
        "| :--- | :--- | :--- | :---: |",
    ]

    for state in states:
        token = dfa.state_token[state]
        number = dfa.state_group[state]

        if number == 0:
            meaning, group = "nothing has been read", "—"
        else:
            group_obj = dfa.groups[number - 1]
            kind = "M" if group_obj.mandatory else "O"
            meaning = f"`{token}`"
            group = f"G{number} {group_obj.name} ({kind})"

        accepting = "yes" if state in finals else "no"
        lines.append(f"| `{state}` | {meaning} | {group} | {accepting} |")

    lines += [
        "",
        "#### Transition function δ",
        "",
        "| From | Input | To |",
        "| :--- | :--- | :--- |",
    ]

    for s_from, symbol, s_to in dfa.transition_list:
        lines.append(f"| `{s_from}` | `{symbol}` | `{s_to}` |")

    lines += [
        "",
        "#### Transition matrix",
        "",
        f"Rows are states, columns are input symbols. `{EMPTY}` means "
        "that δ is not defined (the automaton goes to the trap state "
        "and rejects). `→` marks the initial state and `*` the "
        "accepting states.",
        "",
        "| δ | " + " | ".join(f"`{s}`" for s in sigma) + " |",
        "| :--- |" + " :---: |" * len(sigma),
    ]

    for state in states:
        mark = ("→" if state == INITIAL_STATE else "") + (
            "*" if state in finals else "")
        cells = [dfa.next_state(state, symbol) or EMPTY for symbol in sigma]
        lines.append(f"| {mark}`{state}` | " + " | ".join(cells) + " |")

    lines += [
        "",
        "#### Regular expression of the recognized language",
        "",
        "```text",
        f"L({name}) = " + language_regex(dfa),
        "```",
        "",
    ]

    return "\n".join(lines)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:
    automata = build_all_profile_dfas()

    if len(sys.argv) == 3 and sys.argv[1] == "--markdown":
        wanted = sys.argv[2].upper()

        for profile, dfa in automata.items():
            if AUTOMATON_NAMES[profile] == wanted:
                print(formal_definition(dfa, wanted))
                return

        print(f"Unknown automaton: {wanted}")
        sys.exit(1)

    for path in write_diagrams(automata):
        print(f"written: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
