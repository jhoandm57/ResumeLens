"""
Résumé extraction logic for ResumeLens.

This module applies the regular expressions defined in
regex_patterns.py and stores the results in ExtractedData.

This stage only extracts information.
Normalization and profile classification are performed
in later stages.
"""

import re

from .regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    PROGRAMMING_LANGUAGES_PATTERN,
    FRAMEWORKS_LIBRARIES_PATTERN,
    DATABASES_PATTERN,
    ACADEMIC_QUALIFICATIONS_PATTERN,
    EXPERIENCE_PATTERN,
    TOOLS_TECHNOLOGIES_PATTERN,
    OTHER_QUALIFICATIONS_PATTERN,
)

from .extracted_data import ExtractedData


def _find_matches(pattern: str, text: str) -> list[str]:
    """
    Find all matches for a regular expression.

    Matching is case-insensitive because résumés may use
    different capitalization styles.

    Args:
        pattern: Regular expression to apply.
        text: Résumé text.

    Returns:
        List containing the matched text.
    """

    return re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )


def extract_contact_information(text: str) -> tuple[list[str], list[str]]:
    """
    Extract email addresses and phone numbers.

    Args:
        text: Résumé text.

    Returns:
        Tuple containing:
        - list of emails
        - list of phone numbers
    """

    emails = _find_matches(EMAIL_PATTERN, text)
    phones = _find_matches(PHONE_PATTERN, text)

    return emails, phones


def extract_programming_languages(text: str) -> list[str]:
    """
    Extract programming languages from résumé text.
    """

    return _find_matches(
        PROGRAMMING_LANGUAGES_PATTERN,
        text
    )


def extract_frameworks_libraries(text: str) -> list[str]:
    """
    Extract frameworks and libraries from résumé text.
    """

    return _find_matches(
        FRAMEWORKS_LIBRARIES_PATTERN,
        text
    )


def extract_databases(text: str) -> list[str]:
    """
    Extract databases from résumé text.
    """

    return _find_matches(
        DATABASES_PATTERN,
        text
    )


def extract_academic_qualifications(text: str) -> list[str]:
    """
    Extract academic qualifications from résumé text.
    """

    return _find_matches(
        ACADEMIC_QUALIFICATIONS_PATTERN,
        text
    )


def extract_professional_experience(text: str) -> list[str]:
    """
    Extract explicit professional experience expressions.
    """

    return _find_matches(
        EXPERIENCE_PATTERN,
        text
    )


def extract_tools_technologies(text: str) -> list[str]:
    """
    Extract tools and technologies from résumé text.
    """

    return _find_matches(
        TOOLS_TECHNOLOGIES_PATTERN,
        text
    )


def extract_other_qualifications(text: str) -> list[str]:
    """
    Extract other relevant qualifications from résumé text.
    """

    return _find_matches(
        OTHER_QUALIFICATIONS_PATTERN,
        text
    )


def extract_resume_information(text: str) -> ExtractedData:
    """
    Extract all relevant information from a résumé.

    This function is the main entry point of the extraction stage.

    Args:
        text: Complete résumé text.

    Returns:
        ExtractedData object containing all extracted information.
    """

    emails, phones = extract_contact_information(text)

    return ExtractedData(
        emails=emails,
        phones=phones,
        programming_languages=extract_programming_languages(text),
        frameworks_libraries=extract_frameworks_libraries(text),
        databases=extract_databases(text),
        academic_qualifications=extract_academic_qualifications(text),
        professional_experience=extract_professional_experience(text),
        tools_technologies=extract_tools_technologies(text),
        other_qualifications=extract_other_qualifications(text),
    )