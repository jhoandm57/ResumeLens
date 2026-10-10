"""
Qualification patterns of the ResumeLens professional profiles.

A profile pattern is built on top of the groups defined in
src/model/normalization/profile_order.py (PROFILE_GROUPS), so the
order used to sort the tokens and the order recognized by the
automata always come from the same definition.

Each group of a profile is marked as:

- MANDATORY: the candidate must have AT LEAST ONE token of the group.
- OPTIONAL:  the group may be missing.

Accepted profile pattern (informal regular description):

    G1 G2 ... Gk

where each Gi is a non-empty ordered selection of the tokens of the
group (if the group is mandatory) or a possibly empty one (if it is
optional). See docs/07_automata_design.md, Section 4.

This module only defines data. It does not build automata.
"""

from dataclasses import dataclass

from src.model.normalization.profile_order import (
    PROFILE_GROUPS,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
)


MANDATORY = True
OPTIONAL = False


@dataclass(frozen=True)
class PatternGroup:
    """
    One group of a profile pattern.

    Attributes:
        name: Readable name of the group (for documentation).
        tokens: Canonical tokens of the group, in canonical order.
        mandatory: True if at least one token of the group is required.
    """

    name: str
    tokens: tuple[str, ...]
    mandatory: bool


# -------------------------------------------------------------------
# Requirement of every group (same order as PROFILE_GROUPS)
# -------------------------------------------------------------------

# (group name, mandatory?) for each group of the profile.
# The tokens of each group are taken from PROFILE_GROUPS.

FULL_STACK_REQUIREMENTS = [
    ("Frontend language", MANDATORY),
    ("Frontend framework", MANDATORY),
    ("Backend", MANDATORY),
    ("API", OPTIONAL),
    ("Database", MANDATORY),
    ("Version control", MANDATORY),
]

MACHINE_LEARNING_REQUIREMENTS = [
    ("Language", MANDATORY),
    ("Data libraries", MANDATORY),
    ("ML libraries", MANDATORY),
    ("ML development", OPTIONAL),
    ("Database", MANDATORY),
    ("Version control", MANDATORY),
]

CYBERSECURITY_REQUIREMENTS = [
    ("Scripting", MANDATORY),
    ("Operating system", MANDATORY),
    ("Networking", MANDATORY),
    ("Security", MANDATORY),
    ("Containers", OPTIONAL),
    ("Version control", MANDATORY),
]

DATA_ENGINEER_REQUIREMENTS = [
    ("Language", MANDATORY),
    ("Processing", MANDATORY),
    ("Orchestration", OPTIONAL),
    ("Data integration", MANDATORY),
    ("Storage", MANDATORY),
    ("Version control", MANDATORY),
]


PROFILE_REQUIREMENTS = {
    FULL_STACK_DEVELOPER: FULL_STACK_REQUIREMENTS,
    MACHINE_LEARNING_ENGINEER: MACHINE_LEARNING_REQUIREMENTS,
    CYBERSECURITY_ENGINEER: CYBERSECURITY_REQUIREMENTS,
    DATA_ENGINEER: DATA_ENGINEER_REQUIREMENTS,
}


# Name of the automaton of each profile (used in docs and diagrams).
AUTOMATON_NAMES = {
    FULL_STACK_DEVELOPER: "A_FS",
    MACHINE_LEARNING_ENGINEER: "A_ML",
    CYBERSECURITY_ENGINEER: "A_SEC",
    DATA_ENGINEER: "A_DE",
}


def _build_pattern(profile: str) -> list[PatternGroup]:
    groups = PROFILE_GROUPS[profile]
    requirements = PROFILE_REQUIREMENTS[profile]

    if len(groups) != len(requirements):
        raise ValueError(
            f"{profile}: {len(groups)} groups but "
            f"{len(requirements)} requirements"
        )

    return [
        PatternGroup(name=name, tokens=tuple(tokens), mandatory=mandatory)
        for tokens, (name, mandatory) in zip(groups, requirements)
    ]


PROFILE_PATTERNS: dict[str, list[PatternGroup]] = {
    profile: _build_pattern(profile) for profile in PROFILE_GROUPS
}
