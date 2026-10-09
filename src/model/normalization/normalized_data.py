"""
Data structure used to store the result of the normalization stage.
"""

from dataclasses import dataclass, field


@dataclass
class NormalizedData:
    """
    Stores the canonical tokens produced by the finite-state
    transducers and the sorted sequence of each profile.
    """

    programming_languages: list[str] = field(default_factory=list)

    frameworks_libraries: list[str] = field(default_factory=list)

    databases: list[str] = field(default_factory=list)

    tools_technologies: list[str] = field(default_factory=list)

    other_qualifications: list[str] = field(default_factory=list)

    academic_qualifications: list[str] = field(default_factory=list)

    experience_years: int | None = None

    # All technical qualification tokens without duplicates,
    # in the order in which they were found.
    qualifications: list[str] = field(default_factory=list)

    # One sorted sequence per profile (input of the automata).
    profile_sequences: dict[str, list[str]] = field(default_factory=dict)
