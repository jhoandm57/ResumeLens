from src.model.normalization.profile_order import (
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
