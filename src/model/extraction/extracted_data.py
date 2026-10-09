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

    emails: list[str] = field(default_factory=list)

    phones: list[str] = field(default_factory=list)

    programming_languages: list[str] = field(default_factory=list)

    frameworks_libraries: list[str] = field(default_factory=list)

    databases: list[str] = field(default_factory=list)

    academic_qualifications: list[str] = field(default_factory=list)

    professional_experience: list[str] = field(default_factory=list)

    tools_technologies: list[str] = field(default_factory=list)

    other_qualifications: list[str] = field(default_factory=list)