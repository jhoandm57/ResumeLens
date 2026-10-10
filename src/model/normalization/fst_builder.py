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
# Prefix tree
# -------------------------------------------------------------------

def _add_prefix_tree(
    fst: FST,
    root: str,
    words: dict[str, list[str]],
    state_name: str,
) -> None:
    """
    Add a prefix tree of words to a transducer, starting at root.

    There is one state for each prefix of the words, so words that
    start the same way share states. Every character writes ε, and
    the end marker writes the output associated with the word.

    Args:
        fst: Transducer being built.
        root: State where the tree starts.
        words: Dictionary word -> output written when "#" is read.
        state_name: Prefix used to name the new states.
    """

    state_of_prefix = {"": root}

    for word, output in words.items():
        prefix = ""

        for char in word:
            next_prefix = prefix + char

            if next_prefix not in state_of_prefix:
                state_of_prefix[next_prefix] = f"{state_name}{len(state_of_prefix)}"

                # Reading a normal character writes ε.
                fst.add_transition(
                    state_of_prefix[prefix],
                    char,
                    state_of_prefix[next_prefix],
                    []
                )

            prefix = next_prefix

        # Reading the end marker writes the output of the word.
        fst.add_transition(
            state_of_prefix[prefix],
            END_MARKER,
            FINAL_STATE,
            output
        )


# -------------------------------------------------------------------
# Dictionary transducers
# -------------------------------------------------------------------

def build_dictionary_fst(vocabulary: dict[str, str]) -> FST:
    """
    Build a prefix-tree transducer from a vocabulary table.

    Every character produces ε, and the end marker produces
    the canonical token of the variant.

    Args:
        vocabulary: Dictionary variant -> canonical token.

    Returns:
        Deterministic finite-state transducer.
    """

    fst = FST()
    fst.add_start_state(INITIAL_STATE)
    fst.add_final_state(FINAL_STATE)

    words = {variant: [token] for variant, token in vocabulary.items()}
    _add_prefix_tree(fst, INITIAL_STATE, words, "q")

    return fst


# -------------------------------------------------------------------
# Experience transducer
# -------------------------------------------------------------------

DIGITS = string.digits


def _add_word(
    fst: FST,
    sources: list[str],
    word: str,
    target: str,
    state_name: str,
) -> None:
    """
    Add a chain of states that reads a word and writes ε.

    The chain starts at every state of sources (they all share the
    same chain) and ends at target.

    Example:
        _add_word(fst, ["b1", "b2"], "of", "of", "o")
        b1 --o/ε--> o1 --f/ε--> of
        b2 --o/ε--> o1
    """

    first = target if len(word) == 1 else f"{state_name}1"

    for source in sources:
        fst.add_transition(source, word[0], first, [])

    previous = first

    for position, char in enumerate(word[1:], start=2):
        following = target if position == len(word) else f"{state_name}{position}"
        fst.add_transition(previous, char, following, [])
        previous = following


def build_experience_fst() -> FST:
    """
    Build the transducer M_EXP.

    It copies the digits of the number of years and erases the rest
    of the expression. The rest must have the same structure accepted
    by EXPERIENCE_PATTERN in the extraction stage (after preprocessing):

        digits (+)? (space)? (year | years | yr | yrs) ( of)? ( professional)? experience

    so inputs such as "3 bananas" are rejected.

    States (37):
        q0, q1            start / reading the number (copies digits)
        plus, sp          optional "+" and optional space
        y1, y2, y3        "y", "ye", "yea"
        unit, units       "year" or "yr" / "years" or "yrs"
        b1                space after the unit
        o1, of, b2        "of" and the space after it
        p1..p11, prof, b3 "professional" and the space after it
        x1..x9, exp       "experience"
        qf                accepting state (reached with "#")

    Example:
        "5+ yrs of experience#" -> "5"
    """

    fst = FST()
    fst.add_start_state("q0")
    fst.add_final_state(FINAL_STATE)

    # Number of years: the digits are copied to the output.
    for digit in DIGITS:
        fst.add_transition("q0", digit, "q1", [digit])
        fst.add_transition("q1", digit, "q1", [digit])

    # Optional "+" and optional space.
    fst.add_transition("q1", "+", "plus", [])
    fst.add_transition("q1", " ", "sp", [])
    fst.add_transition("plus", " ", "sp", [])

    # year | years | yr | yrs
    _add_word(fst, ["q1", "plus", "sp"], "year", "unit", "y")
    fst.add_transition("y1", "r", "unit", [])
    fst.add_transition("unit", "s", "units", [])
    fst.add_transition("unit", " ", "b1", [])
    fst.add_transition("units", " ", "b1", [])

    # Optional " of"
    _add_word(fst, ["b1"], "of", "of", "o")
    fst.add_transition("of", " ", "b2", [])

    # Optional " professional"
    _add_word(fst, ["b1", "b2"], "professional", "prof", "p")
    fst.add_transition("prof", " ", "b3", [])

    # "experience" and the end marker
    _add_word(fst, ["b1", "b2", "b3"], "experience", "exp", "x")
    fst.add_transition("exp", END_MARKER, FINAL_STATE, [])

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
