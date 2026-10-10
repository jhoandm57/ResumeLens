"""
Data structure used to store the result of the classification stage.
"""

from dataclasses import dataclass, field

from src.model.normalization.normalized_data import NormalizedData


ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"


@dataclass
class ProfileDecision:
    """
    Result of running the automaton of one profile.

    Attributes:
        profile: Name of the profile (for example FULL_STACK_DEVELOPER).
        automaton: Name of the automaton (for example A_FS).
        sequence: Sorted token sequence given to the automaton.
        result: ACCEPTED or REJECTED.
        trace: Run of the automaton (state, symbol, next state).
        final_state: State reached at the end of the run
                     (q_trap if a transition was missing).
        missing_groups: Mandatory groups of the profile without any
                        token in the sequence (explains a rejection).
    """

    profile: str
    automaton: str
    sequence: list[str]
    result: str
    trace: list[tuple[str, str, str]] = field(default_factory=list)
    final_state: str = "q0"
    missing_groups: list[str] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return self.result == ACCEPTED


@dataclass
class ClassificationResult:
    """
    Stores the decisions of the four automata for one résumé.

    The normalized data is kept so that the next stage (candidate
    profile DSL) receives all the candidate information in one object.
    """

    normalized: NormalizedData

    # One decision per profile, in the order of PROFILE_PATTERNS.
    decisions: dict[str, ProfileDecision] = field(default_factory=dict)

    @property
    def accepted_profiles(self) -> list[str]:
        """Profiles whose automaton accepted the sequence."""

        return [
            profile
            for profile, decision in self.decisions.items()
            if decision.accepted
        ]

    def result_of(self, profile: str) -> str:
        """ACCEPTED or REJECTED for one profile."""

        return self.decisions[profile].result
