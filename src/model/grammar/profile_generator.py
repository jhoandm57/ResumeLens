"""
Generation of the candidate profile in the ResumeLens DSL (stage 4).

ProfileGenerator converts the result of stages 2 and 3 into a text
written in the candidate profile language (resume_lens.tx):

    NormalizedData + {profile: ACCEPTED / REJECTED}  ->  DSL text

The generated text is validated afterwards by ProfileValidator, so a
profile only reaches the visualization if it satisfies the grammar.

See docs/08_grammar_design.md.
"""

from src.model.classification.profile_vocabulary import ProfileVocabulary
from src.model.normalization.normalized_data import NormalizedData


# Name written when stage 1 did not find the name of the candidate
# (the grammar requires a name).
UNKNOWN_NAME = "Unknown candidate"

# Academic tokens that are degrees; the other academic tokens
# (COMPUTER_SCIENCE, DATA_SCIENCE, ...) are fields of study.
DEGREES = ["BACHELOR", "MASTER", "PHD"]

INDENT = "    "


class ProfileGenerator:
    """
    Writes the candidate profile of a résumé in the DSL.
    """

    def generate(self, normalized: NormalizedData, classification: dict[str, str]) -> str:
        """
        Build the DSL text of a candidate profile.

        Args:
            normalized: Result of the normalization stage (stage 2).
            classification: Result of ProfileAutomata.classify (stage 3),
                            profile -> ACCEPTED / REJECTED.

        Returns:
            Text of the profile in the candidate profile language.
        """

        name = normalized.name or UNKNOWN_NAME

        lines = [f"candidate {_quote(name)} {{"]
        lines += self._contact(normalized)
        lines += self._experience(normalized)
        lines += self._education(normalized)
        lines += self._skills(normalized)
        lines += self._classification(classification)
        lines.append("}")

        return "\n".join(lines) + "\n"

    # ---------------------------------------------------------------
    # Blocks
    # ---------------------------------------------------------------

    @staticmethod
    def _contact(normalized: NormalizedData) -> list[str]:
        """contact { email ... phone ... } (always present, may be empty)."""

        lines = [f"{INDENT}contact {{"]

        for email in normalized.emails:
            lines.append(f"{INDENT * 2}email {email}")

        for phone in normalized.phones:
            # A phone extracted across a line break is written in one line.
            lines.append(f"{INDENT * 2}phone {' '.join(phone.split())}")

        lines.append(f"{INDENT}}}")

        return lines

    @staticmethod
    def _experience(normalized: NormalizedData) -> list[str]:
        """experience { years N  entry "..." ... } (only if there are entries)."""

        if not normalized.experience_entries or normalized.experience_years is None:
            return []

        lines = [
            f"{INDENT}experience {{",
            f"{INDENT * 2}years {normalized.experience_years}",
        ]

        for entry in normalized.experience_entries:
            lines.append(f"{INDENT * 2}entry {_quote(entry)}")

        lines.append(f"{INDENT}}}")

        return lines

    @staticmethod
    def _education(normalized: NormalizedData) -> list[str]:
        """education { degree ... field ... } (only if there are academic tokens)."""

        if not normalized.academic_qualifications:
            return []

        lines = [f"{INDENT}education {{"]

        for token in normalized.academic_qualifications:
            kind = "degree" if token in DEGREES else "field"
            lines.append(f"{INDENT * 2}{kind} {token}")

        lines.append(f"{INDENT}}}")

        return lines

    @staticmethod
    def _skills(normalized: NormalizedData) -> list[str]:
        """skills { category: TOKEN, TOKEN ... } (only non-empty categories)."""

        categories = [
            ("languages", normalized.programming_languages),
            ("frameworks", normalized.frameworks_libraries),
            ("databases", normalized.databases),
            ("tools", normalized.tools_technologies),
            ("other", normalized.other_qualifications),
        ]

        category_lines = [
            f"{INDENT * 2}{category}: {', '.join(tokens)}"
            for category, tokens in categories
            if tokens
        ]

        if not category_lines:
            return []

        return [f"{INDENT}skills {{", *category_lines, f"{INDENT}}}"]

    @staticmethod
    def _classification(classification: dict[str, str]) -> list[str]:
        """classification { PROFILE: RESULT } for the four profiles, in order."""

        lines = [f"{INDENT}classification {{"]

        for profile in ProfileVocabulary.GROUPS:
            lines.append(f"{INDENT * 2}{profile}: {classification[profile]}")

        lines.append(f"{INDENT}}}")

        return lines


def _quote(text: str) -> str:
    """
    Write a text as a STRING of the grammar (between double quotes).

    Double quotes inside the text are replaced by single quotes,
    so the STRING always ends where it should.
    """

    return '"' + text.replace('"', "'") + '"'
