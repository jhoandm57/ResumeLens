from itertools import combinations

from src.model.classification.automata_builder import (
    INITIAL_STATE,
    TRAP_STATE,
    accepts,
    build_all_profile_dfas,
    run_trace,
)
from src.model.classification.profile_patterns import PROFILE_PATTERNS
from src.model.normalization.profile_order import (
    PROFILE_ORDERS,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
)


DFAS = build_all_profile_dfas()


# -------------------------------------------------------------------
# Structure of the automata (5-tuple)
# -------------------------------------------------------------------

def test_one_automaton_per_profile():
    assert set(DFAS) == {
        FULL_STACK_DEVELOPER,
        MACHINE_LEARNING_ENGINEER,
        CYBERSECURITY_ENGINEER,
        DATA_ENGINEER,
    }


def test_size_of_the_automata():
    # |Q|, |Σ| and number of transitions of docs/07, Section 7.
    expected = {
        FULL_STACK_DEVELOPER: (14, 13, 45),
        MACHINE_LEARNING_ENGINEER: (12, 11, 33),
        CYBERSECURITY_ENGINEER: (13, 12, 37),
        DATA_ENGINEER: (12, 11, 30),
    }

    for profile, (states, symbols, transitions) in expected.items():
        dfa = DFAS[profile]

        assert len(dfa.states) == states
        assert len(dfa.symbols) == symbols
        assert len(dfa.transition_list) == transitions


def test_alphabet_is_the_canonical_order_of_the_profile():
    for profile, dfa in DFAS.items():
        symbols = {str(symbol.value) for symbol in dfa.symbols}

        assert symbols == set(PROFILE_ORDERS[profile])


def test_one_state_per_token_plus_initial_state():
    for profile, dfa in DFAS.items():
        assert len(dfa.states) == len(PROFILE_ORDERS[profile]) + 1
        assert str(dfa.start_state.value) == INITIAL_STATE


def test_the_only_accepting_state_is_the_state_of_git():
    for dfa in DFAS.values():
        finals = dfa.final_state_names

        assert len(finals) == 1
        assert dfa.state_token[finals[0]] == "GIT"


def test_automata_are_deterministic():
    for dfa in DFAS.values():
        assert dfa.is_deterministic()

        pairs = [(s_from, symbol) for s_from, symbol, _ in dfa.transition_list]
        assert len(pairs) == len(set(pairs))


def test_every_transition_with_a_token_goes_to_the_state_of_that_token():
    for dfa in DFAS.values():
        for _, symbol, s_to in dfa.transition_list:
            assert dfa.state_token[s_to] == symbol


def test_automata_are_minimal():
    for dfa in DFAS.values():
        assert len(dfa.minimize().states) == len(dfa.states)


# -------------------------------------------------------------------
# Language of the automata
# -------------------------------------------------------------------

def _expected(profile: str, sequence: list[str]) -> bool:
    """Every mandatory group has at least one token in the sequence."""

    present = set(sequence)

    return all(
        present.intersection(group.tokens)
        for group in PROFILE_PATTERNS[profile]
        if group.mandatory
    )


def test_exhaustive_all_sorted_subsets():
    # Every sorted sequence without repetitions is a subset of the
    # tokens of the profile in canonical order. All of them are tested
    # (2^13 = 8192 sequences for Full Stack).
    for profile, dfa in DFAS.items():
        order = PROFILE_ORDERS[profile]

        for size in range(len(order) + 1):
            for sequence in combinations(order, size):
                assert accepts(dfa, list(sequence)) == _expected(
                    profile, list(sequence)
                ), (profile, sequence)


def test_unsorted_sequence_is_rejected():
    dfa = DFAS[FULL_STACK_DEVELOPER]

    assert not accepts(dfa, ["REACT", "JAVASCRIPT", "NODE_JS", "SQL", "GIT"])


def test_repeated_token_is_rejected():
    dfa = DFAS[FULL_STACK_DEVELOPER]

    assert not accepts(
        dfa, ["JAVASCRIPT", "JAVASCRIPT", "REACT", "NODE_JS", "SQL", "GIT"]
    )


def test_token_of_other_profile_is_rejected():
    dfa = DFAS[FULL_STACK_DEVELOPER]

    assert not accepts(dfa, ["JAVASCRIPT", "REACT", "PANDAS", "NODE_JS", "SQL", "GIT"])


# -------------------------------------------------------------------
# Run of the automaton
# -------------------------------------------------------------------

def test_trace_of_the_statement_example():
    dfa = DFAS[FULL_STACK_DEVELOPER]

    trace = run_trace(dfa, ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])

    assert trace == [
        ("q0", "JAVASCRIPT", "q1"),
        ("q1", "REACT", "q3"),
        ("q3", "NODE_JS", "q6"),
        ("q6", "POSTGRESQL", "q11"),
        ("q11", "GIT", "q13"),
    ]


def test_trace_stops_in_the_trap_state():
    dfa = DFAS[FULL_STACK_DEVELOPER]

    trace = run_trace(dfa, ["JAVASCRIPT", "REACT", "POSTGRESQL", "GIT"])

    assert trace[-1] == ("q3", "POSTGRESQL", TRAP_STATE)
    assert len(trace) == 3


def test_trace_of_empty_sequence():
    assert run_trace(DFAS[DATA_ENGINEER], []) == []
