"""
Résumé normalization logic for ResumeLens.

This module applies the finite-state transducers defined in
fst_builder.py to the information extracted by the regular
expression stage, and organizes the canonical tokens in the
order of each professional profile.

This stage only transforms and organizes the information.
Profile classification is performed in the next stage.
"""

from src.model.extraction.extracted_data import ExtractedData

from .canonical_vocabulary import (
    LANGUAGES_VOCABULARY,
    FRAMEWORKS_VOCABULARY,
    DATABASES_VOCABULARY,
    TOOLS_VOCABULARY,
    OTHER_VOCABULARY,
    ACADEMIC_VOCABULARY,
)
from .fst_builder import (
    build_dictionary_fst,
    build_experience_fst,
    translate,
)
from .normalized_data import NormalizedData
from .profile_order import PROFILE_ORDERS, sort_for_profile


# The transducers are built only once, when the module is imported.
LANGUAGES_FST = build_dictionary_fst(LANGUAGES_VOCABULARY)
FRAMEWORKS_FST = build_dictionary_fst(FRAMEWORKS_VOCABULARY)
DATABASES_FST = build_dictionary_fst(DATABASES_VOCABULARY)
TOOLS_FST = build_dictionary_fst(TOOLS_VOCABULARY)
OTHER_FST = build_dictionary_fst(OTHER_VOCABULARY)
ACADEMIC_FST = build_dictionary_fst(ACADEMIC_VOCABULARY)
EXPERIENCE_FST = build_experience_fst()


def _unique(items: list[str]) -> list[str]:
    """
    Remove duplicates keeping the order of the first appearance.
    """

    return list(dict.fromkeys(items))


def normalize_list(fst, values: list[str]) -> list[str]:
    """
    Translate every extracted string with a transducer.

    Rejected strings are ignored and duplicates are removed.

    Args:
        fst: Transducer of the category.
        values: Strings extracted from the résumé.

    Returns:
        List of canonical tokens without duplicates.
    """

    tokens = [translate(fst, value) for value in values]

    return _unique([token for token in tokens if token is not None])


def normalize_experience(values: list[str]) -> int | None:
    """
    Obtain the number of years of experience.

    If there are several experience expressions,
    the maximum value is kept.

    Args:
        values: Experience expressions extracted from the résumé.

    Returns:
        Number of years, or None if there is no valid expression.
    """

    years = []

    for value in values:
        output = translate(EXPERIENCE_FST, value)

        if output:
            years.append(int(output))

    return max(years) if years else None


def normalize_resume(extracted: ExtractedData) -> NormalizedData:
    """
    Normalize all the information extracted from a résumé.

    This function is the main entry point of the normalization stage.

    Args:
        extracted: Result of the extraction stage.

    Returns:
        NormalizedData object with canonical tokens and the sorted
        sequence of each profile.
    """

    languages = normalize_list(LANGUAGES_FST, extracted.programming_languages)
    frameworks = normalize_list(FRAMEWORKS_FST, extracted.frameworks_libraries)
    databases = normalize_list(DATABASES_FST, extracted.databases)
    tools = normalize_list(TOOLS_FST, extracted.tools_technologies)
    other = normalize_list(OTHER_FST, extracted.other_qualifications)
    academic = normalize_list(ACADEMIC_FST, extracted.academic_qualifications)

    # SQL can appear as a language and as a database;
    # _unique keeps only one occurrence.
    qualifications = _unique(languages + frameworks + databases + tools + other)

    profile_sequences = {
        profile: sort_for_profile(qualifications, profile)
        for profile in PROFILE_ORDERS
    }

    return NormalizedData(
        programming_languages=languages,
        frameworks_libraries=frameworks,
        databases=databases,
        tools_technologies=tools,
        other_qualifications=other,
        academic_qualifications=academic,
        experience_years=normalize_experience(extracted.professional_experience),
        qualifications=qualifications,
        profile_sequences=profile_sequences,
    )
