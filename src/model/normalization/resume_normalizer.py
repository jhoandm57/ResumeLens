"""
Résumé normalization logic for ResumeLens.

ResumeNormalizer applies the finite-state transducers to the
information extracted by the regular-expression stage and organizes
the canonical tokens in the order of each professional profile.

This stage only transforms and organizes the information.
Profile classification is performed in the next stage.

See docs/06_fst_design.md.
"""

from src.model.classification.profile_vocabulary import ProfileVocabulary
from src.model.extraction.extracted_data import ExtractedData

from .normalization_transducers import NormalizationTransducers
from .normalized_data import NormalizedData


class ResumeNormalizer:
    """
    Normalizes the extracted data of a résumé (stage 2).
    """

    def __init__(self):
        # The seven transducers are built only once.
        self.transducers = NormalizationTransducers()

    # ---------------------------------------------------------------
    # Normalization with the transducers
    # ---------------------------------------------------------------

    def normalize_list(self, fst, values: list[str]) -> list[str]:
        """
        Translate every extracted string with a transducer.

        Rejected strings are ignored and duplicates are removed,
        keeping the order of the first appearance.
        """

        tokens = [self.transducers.translate(fst, value) for value in values]

        return _unique([token for token in tokens if token is not None])

    def normalize_experience(self, values: list[str]) -> int | None:
        """
        Obtain the number of years of experience with M_EXP.

        If there are several experience expressions,
        the maximum value is kept.
        """

        years = []

        for value in values:
            output = self.transducers.translate(self.transducers.experience, value)

            if output:
                years.append(int(output))

        return max(years) if years else None

    def experience_entries(self, values: list[str]) -> list[str]:
        """
        Keep the experience expressions as they were written in the
        résumé (not normalized), without duplicates.

        Only the expressions accepted by M_EXP are kept, so every entry
        corresponds to a number of years.

        Example:
            ["3 years of experience", "5+ yrs experience"]
            -> ["3 years of experience", "5+ yrs experience"]
        """

        accepted = [
            value
            for value in values
            if self.transducers.translate(self.transducers.experience, value)
        ]

        return _unique(accepted)

    # ---------------------------------------------------------------
    # Sorting by profile (canonical order)
    # ---------------------------------------------------------------

    @staticmethod
    def sort_for_profile(tokens: list[str], profile: str) -> list[str]:
        """
        Organize the tokens in the canonical order of a profile.

        - Only the tokens of the profile are kept.
        - Each token appears at most once.
        - The tokens follow the order of the groups of the profile
          (ProfileVocabulary.GROUPS). If several tokens belong to the
          same group, all of them are kept.

        Example (Full Stack):
            GIT, NODE_JS, JAVASCRIPT, POSTGRESQL, REACT
            -> JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
        """

        order = [
            token
            for group in ProfileVocabulary.GROUPS[profile]
            for token in group
        ]
        kept = {token for token in tokens if token in order}

        return sorted(kept, key=order.index)

    # ---------------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------------

    def normalize(self, extracted: ExtractedData) -> NormalizedData:
        """
        Normalize all the information extracted from a résumé.

        This is the main entry point of the normalization stage.

        Args:
            extracted: Result of the extraction stage.

        Returns:
            NormalizedData with the canonical tokens and the sorted
            sequence of each profile (input of the automata).
        """

        t = self.transducers

        languages = self.normalize_list(t.languages, extracted.programming_languages)
        frameworks = self.normalize_list(t.frameworks, extracted.frameworks_libraries)
        databases = self.normalize_list(t.databases, extracted.databases)
        tools = self.normalize_list(t.tools, extracted.tools_technologies)
        other = self.normalize_list(t.other, extracted.other_qualifications)
        academic = self.normalize_list(t.academic, extracted.academic_qualifications)

        # SQL can appear as a language and as a database;
        # _unique keeps only one occurrence.
        qualifications = _unique(languages + frameworks + databases + tools + other)

        profile_sequences = {
            profile: self.sort_for_profile(qualifications, profile)
            for profile in ProfileVocabulary.GROUPS
        }

        return NormalizedData(
            name=extracted.name,
            emails=list(extracted.emails),
            phones=list(extracted.phones),
            programming_languages=languages,
            frameworks_libraries=frameworks,
            databases=databases,
            tools_technologies=tools,
            other_qualifications=other,
            academic_qualifications=academic,
            experience_years=self.normalize_experience(extracted.professional_experience),
            experience_entries=self.experience_entries(extracted.professional_experience),
            qualifications=qualifications,
            profile_sequences=profile_sequences,
        )


def _unique(items: list[str]) -> list[str]:
    """Remove duplicates keeping the order of the first appearance."""

    return list(dict.fromkeys(items))
