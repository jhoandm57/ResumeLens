"""
Finite-state transducers of the ResumeLens normalization stage.

Every transducer reads its input one character at a time.
The end marker "#" is appended to every input.

There are two kinds of transducers:

1. Dictionary transducers (M_LANG, M_FW, M_DB, M_TOOLS, M_OTHER, M_ACAD):
   one state per prefix of the variants; every character writes ε and
   the end marker writes the canonical token.

       Q   = { q_p | p is a prefix of a variant } ∪ { qf }
       Σ   = characters of the variants ∪ { # }
       Γ   = canonical tokens
       δ(q_p, a) = q_pa        ω(q_p, a) = ε
       δ(q_w, #) = qf          ω(q_w, #) = T(w)
       q0  = q_ε,  F = { qf }

2. Experience transducer (M_EXP): 4 states; it copies the digits of
   the number of years and erases the rest of the expression.

See docs/06_fst_design.md, Sections 5 and 6.
"""

import string

from pyformlang.fst import FST

from .normalization_vocabulary import NormalizationVocabulary as V


END_MARKER = "#"
INITIAL_STATE = "q0"
FINAL_STATE = "qf"

DIGITS = string.digits                  # 0 1 2 ... 9
LETTERS = string.ascii_lowercase        # a b c ... z


class NormalizationTransducers:
    """
    Builds the seven transducers of the stage and translates strings.
    """

    def __init__(self):
        self.languages = self.build_dictionary_fst(V.LANGUAGES)        # M_LANG
        self.frameworks = self.build_dictionary_fst(V.FRAMEWORKS)      # M_FW
        self.databases = self.build_dictionary_fst(V.DATABASES)        # M_DB
        self.tools = self.build_dictionary_fst(V.TOOLS)                # M_TOOLS
        self.other = self.build_dictionary_fst(V.OTHER)                # M_OTHER
        self.academic = self.build_dictionary_fst(V.ACADEMIC)          # M_ACAD
        self.experience = self.build_experience_fst()                  # M_EXP

    # ---------------------------------------------------------------
    # Dictionary transducers (prefix tree)
    # ---------------------------------------------------------------

    @staticmethod
    def build_dictionary_fst(vocabulary: dict[str, str]) -> FST:
        """
        Build a prefix-tree transducer from a vocabulary table.

        There is one state for each prefix of the variants, so variants
        that start the same way share states (react, react.js, reactjs).
        Every character writes ε, and the end marker writes the
        canonical token of the variant.

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

                # A new prefix creates a new state: q1, q2, q3, ...
                if next_prefix not in state_of_prefix:
                    state_of_prefix[next_prefix] = f"q{len(state_of_prefix)}"

                    # Reading a normal character writes ε.
                    fst.add_transition(
                        state_of_prefix[prefix],
                        char,
                        state_of_prefix[next_prefix],
                        [],
                    )

                prefix = next_prefix

            # Reading the end marker writes the canonical token.
            fst.add_transition(
                state_of_prefix[prefix],
                END_MARKER,
                FINAL_STATE,
                [token],
            )

        return fst

    # ---------------------------------------------------------------
    # Experience transducer
    # ---------------------------------------------------------------

    @staticmethod
    def build_experience_fst() -> FST:
        """
        Build the transducer M_EXP.

        It copies the digits of the number of years and erases the rest
        of the expression. The structure of the expression ("years",
        "of", "experience") is already guaranteed by EXPERIENCE_PATTERN
        in the extraction stage.

        States:
            q0  nothing has been read
            q1  reading the number of years (digits are copied)
            q2  reading the rest of the expression (everything is erased)
            qf  end marker read (accepting state)

        Example:
            "5+ yrs of experience#" -> "5"
        """

        fst = FST()
        fst.add_start_state(INITIAL_STATE)
        fst.add_final_state(FINAL_STATE)

        # Symbols of the rest of the expression: letters, "+" and space.
        other_symbols = list(LETTERS) + ["+", " "]

        for digit in DIGITS:
            fst.add_transition("q0", digit, "q1", [digit])     # first digit
            fst.add_transition("q1", digit, "q1", [digit])     # more digits
            fst.add_transition("q2", digit, "q2", [])          # digits after the number

        for symbol in other_symbols:
            fst.add_transition("q1", symbol, "q2", [])         # end of the number
            fst.add_transition("q2", symbol, "q2", [])         # rest of the expression

        fst.add_transition("q2", END_MARKER, FINAL_STATE, [])

        return fst

    # ---------------------------------------------------------------
    # Translation
    # ---------------------------------------------------------------

    @staticmethod
    def preprocess(text: str) -> str:
        """
        Prepare an extracted string before it enters a transducer.

        - Converts to lowercase.
        - Replaces the typographic apostrophe ’ with '.
        - Replaces any sequence of whitespace with a single space.

        Example:
            "  Tensor   Flow " -> "tensor flow"
        """

        text = text.lower().replace("’", "'")

        return " ".join(text.split())

    def translate(self, fst: FST, text: str) -> str | None:
        """
        Translate a string with a transducer.

        The string is preprocessed, split into characters, and the
        end marker is appended.

        Returns:
            The output of the transducer, or None if the input
            is rejected.
        """

        input_word = list(self.preprocess(text)) + [END_MARKER]

        for output in fst.translate(input_word):
            # The transducers are deterministic: there is at most one output.
            return "".join(str(symbol) for symbol in output)

        return None
