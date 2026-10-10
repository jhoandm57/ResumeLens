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

    # The name and the contact information are not normalized. It is copied from
    # ExtractedData so that the next stages (candidate profile)
    # receive all the candidate information in one object.
    name: str | None = None

    emails: list[str] = field(default_factory=list)

    phones: list[str] = field(default_factory=list)

    programming_languages: list[str] = field(default_factory=list)

    frameworks_libraries: list[str] = field(default_factory=list)

    databases: list[str] = field(default_factory=list)

    tools_technologies: list[str] = field(default_factory=list)

    other_qualifications: list[str] = field(default_factory=list)

    academic_qualifications: list[str] = field(default_factory=list)

    experience_years: int | None = None

    # All technical qualification tokens without duplicates.
    # They are grouped by category (languages, frameworks, databases,
    # tools, other) and, inside each category, follow the order of
    # the résumé. The recognition stage does not use this order:
    # it uses profile_sequences.
    qualifications: list[str] = field(default_factory=list)

    # One sorted sequence per profile (input of the automata).
    profile_sequences: dict[str, list[str]] = field(default_factory=dict)
