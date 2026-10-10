"""
Résumé classification logic for ResumeLens.

This module runs the finite automata defined in automata_builder.py
on the sorted sequences produced by the normalization stage and
decides, for every profile, whether the résumé satisfies an accepted
qualification pattern (ACCEPTED) or not (REJECTED).

A résumé may be accepted by several profiles, by one, or by none.
This stage does not rank candidates nor make hiring decisions.
"""

from src.model.normalization.normalized_data import NormalizedData
from src.model.normalization.profile_order import sort_for_profile

from .automata_builder import (
    TRAP_STATE,
    INITIAL_STATE,
    ResumeLensDFA,
    accepts,
    build_all_profile_dfas,
    run_trace,
)
from .classification_result import (
    ACCEPTED,
    REJECTED,
    ClassificationResult,
    ProfileDecision,
)
from .profile_patterns import AUTOMATON_NAMES, PROFILE_PATTERNS


# The automata are built only once, when the module is imported.
PROFILE_DFAS: dict[str, ResumeLensDFA] = build_all_profile_dfas()


def missing_mandatory_groups(profile: str, sequence: list[str]) -> list[str]:
    """
    Names of the mandatory groups of a profile without any token
    in the sequence.

    It is used only to explain a rejection; the decision is always
    taken by the automaton.
    """

    present = set(sequence)

    return [
        group.name
        for group in PROFILE_PATTERNS[profile]
        if group.mandatory and not present.intersection(group.tokens)
    ]


def classify_sequence(profile: str, sequence: list[str]) -> ProfileDecision:
    """
    Run the automaton of one profile on a sorted token sequence.

    Args:
        profile: Name of the profile (key of PROFILE_DFAS).
        sequence: Sorted sequence (output of sort_for_profile).

    Returns:
        ProfileDecision with the result and the run of the automaton.
    """

    dfa = PROFILE_DFAS[profile]
    trace = run_trace(dfa, sequence)
    final_state = trace[-1][2] if trace else INITIAL_STATE

    is_accepted = accepts(dfa, sequence)

    return ProfileDecision(
        profile=profile,
        automaton=AUTOMATON_NAMES[profile],
        sequence=list(sequence),
        result=ACCEPTED if is_accepted else REJECTED,
        trace=trace,
        final_state=final_state,
        missing_groups=(
            [] if is_accepted else missing_mandatory_groups(profile, sequence)
        ),
    )


def classify_tokens(tokens: list[str], profile: str) -> ProfileDecision:
    """
    Sort a list of normalized tokens for a profile and classify it.

    Useful when the tokens are not already sorted, e.g.:
        classify_tokens(["GIT", "PYTHON", ...], MACHINE_LEARNING_ENGINEER)
    """

    return classify_sequence(profile, sort_for_profile(tokens, profile))


def classify_resume(normalized: NormalizedData) -> ClassificationResult:
    """
    Classify a normalized résumé with the four profile automata.

    This function is the main entry point of the classification stage.

    Args:
        normalized: Result of the normalization stage.

    Returns:
        ClassificationResult with one decision per profile.
    """

    decisions = {}

    for profile in PROFILE_PATTERNS:
        sequence = normalized.profile_sequences.get(
            profile,
            sort_for_profile(normalized.qualifications, profile),
        )
        decisions[profile] = classify_sequence(profile, sequence)

    return ClassificationResult(normalized=normalized, decisions=decisions)


__all__ = [
    "ACCEPTED",
    "REJECTED",
    "TRAP_STATE",
    "PROFILE_DFAS",
    "classify_sequence",
    "classify_tokens",
    "classify_resume",
    "missing_mandatory_groups",
]
