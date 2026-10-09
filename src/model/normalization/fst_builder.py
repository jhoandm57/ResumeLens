"""
Finite-state transducers of the ResumeLens normalization stage.

Every transducer reads its input one character at a time.
The end marker "#" is appended to every input, and the
canonical token is written only when "#" is read.

Formal definition of the dictionary transducers
(see docs/06_fst_design.md, Section 5):

    Q   = { q_p | p is a prefix of a variant } ∪ { qf }
    Σ   = characters of the variants ∪ { # }
    Γ   = canonical tokens
    δ(q_p, a) = q_pa        ω(q_p, a) = ε
    δ(q_w, #) = qf          ω(q_w, #) = T(w)
    q0  = q_ε
    F   = { qf }
"""

import string

from pyformlang.fst import FST


END_MARKER = "#"
INITIAL_STATE = "q0"
FINAL_STATE = "qf"


# -------------------------------------------------------------------
# Preprocessing
# -------------------------------------------------------------------

def preprocess(text: str) -> str:
    """
    Prepare an extracted string before it enters a transducer.

    - Converts to lowercase.
    - Replaces the typographic apostrophe ’ with '.
    - Removes spaces at the beginning and end and replaces
      any sequence of whitespace with a single space.

    Example:
        "  Tensor   Flow " -> "tensor flow"
    """

    text = text.lower().replace("’", "'")

    return " ".join(text.split())


# -------------------------------------------------------------------
# Dictionary transducers (prefix tree)
# -------------------------------------------------------------------

def build_dictionary_fst(vocabulary: dict[str, str]) -> FST:
    """
    Build a prefix-tree transducer from a vocabulary table.

    There is one state for each prefix of the variants, so variants
    that start the same way share states. Every character produces ε,
    and the end marker produces the canonical token.

    Args:
        vocabulary: Dictionary variant -> canonical token.

    Returns:
        Deterministic finite-state transducer.
    """

    fst = FST()
    fst.add_start_state(INITIAL_STATE)
    fst.add_final_state(FINAL_STATE)

    state_of_prefix = {"": INITIAL_STATE}

    for variant, token in vocabulary.items():
        prefix = ""

        for char in variant:
            next_prefix = prefix + char

            if next_prefix not in state_of_prefix:
                state_of_prefix[next_prefix] = f"q{len(state_of_prefix)}"

                # Reading a normal character writes ε.
                fst.add_transition(
                    state_of_prefix[prefix],
                    char,
                    state_of_prefix[next_prefix],
                    []
                )

            prefix = next_prefix

        # Reading the end marker writes the canonical token.
        fst.add_transition(
            state_of_prefix[prefix],
            END_MARKER,
            FINAL_STATE,
            [token]
        )

    return fst


# -------------------------------------------------------------------
# Experience transducer
# -------------------------------------------------------------------

DIGITS = string.digits
EXPERIENCE_OTHER_SYMBOLS = string.ascii_lowercase + "+ "


def build_experience_fst() -> FST:
    """
    Build the transducer M_EXP.

    It copies the digits of the number of years and erases
    the rest of the expression.

        Q = { q0, q1, q2, qf }
        q0 --d/d--> q1      q1 --d/d--> q1
        q1 --c/ε--> q2      q2 --c/ε--> q2
        q2 --d/ε--> q2      q2 --#/ε--> qf

    where d is a digit and c is a non-digit symbol.

    Example:
        "5+ yrs experience#" -> "5"
    """

    fst = FST()
    fst.add_start_state("q0")
    fst.add_final_state(FINAL_STATE)

    for digit in DIGITS:
        fst.add_transition("q0", digit, "q1", [digit])
        fst.add_transition("q1", digit, "q1", [digit])
        fst.add_transition("q2", digit, "q2", [])

    for symbol in EXPERIENCE_OTHER_SYMBOLS:
        fst.add_transition("q1", symbol, "q2", [])
        fst.add_transition("q2", symbol, "q2", [])

    fst.add_transition("q2", END_MARKER, FINAL_STATE, [])

    return fst


# -------------------------------------------------------------------
# Translation
# -------------------------------------------------------------------

def translate(fst: FST, text: str) -> str | None:
    """
    Translate a string with a transducer.

    The string is preprocessed, split into characters, and the
    end marker is appended.

    Args:
        fst: Transducer to use.
        text: String extracted from the résumé.

    Returns:
        The output of the transducer, or None if the input
        is rejected.
    """

    input_word = list(preprocess(text)) + [END_MARKER]

    for output in fst.translate(input_word):
        # The transducers are deterministic: there is at most one output.
        return "".join(str(symbol) for symbol in output)

    return None
