from src.model.normalization.profile_order import (
    PROFILE_GROUPS,
    PROFILE_ORDERS,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
    sort_for_profile,
)


def test_full_stack_order_from_statement():
    tokens = ["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]

    result = sort_for_profile(tokens, FULL_STACK_DEVELOPER)

    assert result == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]


def test_machine_learning_order():
    tokens = ["GIT", "SQL", "TENSORFLOW", "PANDAS", "PYTHON"]

    result = sort_for_profile(tokens, MACHINE_LEARNING_ENGINEER)

    assert result == ["PYTHON", "PANDAS", "TENSORFLOW", "SQL", "GIT"]


def test_tokens_of_other_profiles_are_discarded():
    tokens = ["PANDAS", "REACT", "GIT"]

    assert sort_for_profile(tokens, FULL_STACK_DEVELOPER) == ["REACT", "GIT"]
    assert sort_for_profile(tokens, CYBERSECURITY_ENGINEER) == ["GIT"]


def test_duplicates_are_removed():
    tokens = ["SQL", "PYTHON", "SQL"]

    assert sort_for_profile(tokens, DATA_ENGINEER) == ["PYTHON", "SQL"]


def test_empty_sequence():
    assert sort_for_profile([], DATA_ENGINEER) == []


def test_order_is_built_from_groups():
    for profile, groups in PROFILE_GROUPS.items():
        flattened = [token for group in groups for token in group]

        assert PROFILE_ORDERS[profile] == flattened


def test_example_sequence_of_the_statement_is_preserved():
    # Sequence of the automaton example of the statement (Stage 3)
    tokens = ["GIT", "POSTGRESQL", "TENSORFLOW", "PANDAS", "PYTHON"]

    result = sort_for_profile(tokens, MACHINE_LEARNING_ENGINEER)

    assert result == ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]


def test_several_tokens_of_the_same_group_are_kept_in_group_order():
    tokens = ["NUMPY", "PYTHON", "PANDAS"]

    result = sort_for_profile(tokens, MACHINE_LEARNING_ENGINEER)

    assert result == ["PYTHON", "PANDAS", "NUMPY"]


def test_linux_in_cybersecurity_order():
    tokens = ["GIT", "LINUX", "PYTHON", "TCP_IP"]

    result = sort_for_profile(tokens, CYBERSECURITY_ENGINEER)

    assert result == ["PYTHON", "LINUX", "TCP_IP", "GIT"]
