"""
Data structure used to store information extracted from a résumé.
"""

from dataclasses import dataclass, field


@dataclass
class ExtractedData:
    """
    Stores the information extracted from a résumé
    during the regular-expression stage.
    """

    # Name of the candidate, or None if it was not found.
    # It is a single value (not a list) because a résumé
    # belongs to only one candidate.
    name: str | None = None

    emails: list[str] = field(default_factory=list)

    phones: list[str] = field(default_factory=list)

    programming_languages: list[str] = field(default_factory=list)

    frameworks_libraries: list[str] = field(default_factory=list)

    databases: list[str] = field(default_factory=list)

    academic_qualifications: list[str] = field(default_factory=list)

    professional_experience: list[str] = field(default_factory=list)

    tools_technologies: list[str] = field(default_factory=list)

    other_qualifications: list[str] = field(default_factory=list)