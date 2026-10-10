"""
Finite automata of the ResumeLens qualification-pattern recognition stage.

Every profile has one deterministic finite automaton (DFA). The input
of the automaton is the sorted sequence of canonical tokens produced
by the normalization stage (NormalizedData.profile_sequences), so
every symbol of the alphabet is a complete token such as REACT or GIT
(not a character).

Formal definition of the automaton of a profile with tokens
t1, t2, ..., tn (canonical order) and groups g(1), ..., g(n)
(see docs/07_automata_design.md, Section 5):

    Q  = { q0 } ∪ { qi | 1 <= i <= n }
         qi means "the last token read was ti"
    Σ  = { t1, ..., tn }
    δ(qi, tj) = qj   iff  j > i  and every group strictly between
                          g(i) and g(j) is optional
                          (for q0, g(0) = 0: every group before g(j)
                          must be optional)
    q0 = q0
    F  = { qi | every group after g(i) is optional }
         (q0 ∈ F only if every group of the profile is optional)

δ is a partial function: a pair (state, symbol) without transition
goes to an implicit trap state, so the input is rejected.
"""

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)

from .profile_patterns import PROFILE_PATTERNS, PatternGroup


INITIAL_STATE = "q0"
TRAP_STATE = "q_trap"


# -------------------------------------------------------------------
# Automaton class
# -------------------------------------------------------------------

class ResumeLensDFA(DeterministicFiniteAutomaton):
    """
    pyformlang DFA that also keeps:

    - transition_list: the transitions in the order they were added.
    - state_token:     the token associated with each state
                       (the last token read to reach the state).
    - state_group:     the group number (1..k) of each state
                       (0 for the initial state).
    - groups:          the pattern groups of the profile.

    This information is used only to document the automata
    (formal tables and diagrams, see src/visualization/dfa_export.py)
    and to show the run of the automaton step by step.
    Recognition is done by pyformlang without any change.
    """

    def __init__(self):
        super().__init__()
        self.transition_list: list[tuple[str, str, str]] = []
        self.state_token: dict[str, str | None] = {}
        self.state_group: dict[str, int] = {}
        self.groups: list[PatternGroup] = []

    def add_transition(self, s_from, symbol, s_to):
        super().add_transition(State(s_from), Symbol(symbol), State(s_to))
        self.transition_list.append((s_from, symbol, s_to))

    def next_state(self, state: str, symbol: str) -> str | None:
        """
        δ(state, symbol), or None if the transition is not defined
        (the run goes to the trap state).
        """

        for s_from, s_symbol, s_to in self.transition_list:
            if s_from == state and s_symbol == symbol:
                return s_to

        return None

    @property
    def final_state_names(self) -> list[str]:
        return [str(state.value) for state in self.final_states]


# -------------------------------------------------------------------
# Construction
# -------------------------------------------------------------------

def _only_optional(groups: list[PatternGroup], first: int, last: int) -> bool:
    """
    True if every group with number in [first, last] is optional.
    Groups are numbered from 1. An empty range returns True.
    """

    return all(not groups[number - 1].mandatory
               for number in range(first, last + 1))


def build_profile_dfa(groups: list[PatternGroup]) -> ResumeLensDFA:
    """
    Build the DFA that recognizes the accepted pattern of a profile.

    Args:
        groups: Ordered pattern groups of the profile.

    Returns:
        Deterministic finite automaton (pyformlang).
    """

    dfa = ResumeLensDFA()
    dfa.groups = list(groups)

    # States: q0 and one state qi per token ti (canonical order).
    states = [INITIAL_STATE]
    dfa.state_token[INITIAL_STATE] = None
    dfa.state_group[INITIAL_STATE] = 0

    for group_number, group in enumerate(groups, start=1):
        for token in group.tokens:
            state = f"q{len(states)}"
            states.append(state)
            dfa.state_token[state] = token
            dfa.state_group[state] = group_number

    dfa.add_start_state(State(INITIAL_STATE))

    # Transitions: from qi with tj (j > i), when no mandatory group
    # is skipped between the group of ti and the group of tj.
    for i, s_from in enumerate(states):
        g_from = dfa.state_group[s_from]

        for j in range(i + 1, len(states)):
            s_to = states[j]
            g_to = dfa.state_group[s_to]

            if _only_optional(groups, g_from + 1, g_to - 1):
                dfa.add_transition(s_from, dfa.state_token[s_to], s_to)

    # Accepting states: no mandatory group remains after the state.
    for state in states:
        if _only_optional(groups, dfa.state_group[state] + 1, len(groups)):
            dfa.add_final_state(State(state))

    return dfa


def build_all_profile_dfas() -> dict[str, ResumeLensDFA]:
    """
    Build the automaton of every profile.

    Returns:
        Dictionary profile -> DFA.
    """

    return {
        profile: build_profile_dfa(groups)
        for profile, groups in PROFILE_PATTERNS.items()
    }


# -------------------------------------------------------------------
# Recognition
# -------------------------------------------------------------------

def accepts(dfa: ResumeLensDFA, sequence: list[str]) -> bool:
    """
    Decide whether a sorted token sequence belongs to the language
    of the automaton (pyformlang).
    """

    return dfa.accepts([Symbol(token) for token in sequence])


def run_trace(dfa: ResumeLensDFA, sequence: list[str]) -> list[tuple[str, str, str]]:
    """
    Run the automaton step by step.

    Args:
        dfa: Automaton of a profile.
        sequence: Sorted token sequence.

    Returns:
        List of steps (state, symbol read, next state). If a transition
        is not defined, the next state is TRAP_STATE and the run stops.
    """

    steps = []
    state = INITIAL_STATE

    for token in sequence:
        following = dfa.next_state(state, token)

        if following is None:
            steps.append((state, token, TRAP_STATE))
            return steps

        steps.append((state, token, following))
        state = following

    return steps
