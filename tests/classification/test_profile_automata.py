from src.model.classification.profile_automata import (
    ACCEPTED,
    REJECTED,
    ProfileAutomata,
)
from src.model.classification.profile_vocabulary import (
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
    ProfileVocabulary,
)
from src.model.extraction.resume_extractor import extract_resume_information
from src.model.normalization.normalization_vocabulary import NormalizationVocabulary
from src.model.normalization.resume_normalizer import ResumeNormalizer


AUTOMATA = ProfileAutomata()
NORMALIZER = ResumeNormalizer()

FS = FULL_STACK_DEVELOPER
ML = MACHINE_LEARNING_ENGINEER
SEC = CYBERSECURITY_ENGINEER
DE = DATA_ENGINEER


def classify_text(text):
    """Stages 1, 2 and 3 together."""
    return AUTOMATA.classify(NORMALIZER.normalize(extract_resume_information(text)))


# -------------------------------------------------------------------
# Connection with stage 2
# -------------------------------------------------------------------

def test_every_token_can_be_produced_by_stage_2():
    tokens_of_stage_2 = set()
    for vocabulary in (NormalizationVocabulary.LANGUAGES, NormalizationVocabulary.FRAMEWORKS,
                       NormalizationVocabulary.DATABASES, NormalizationVocabulary.TOOLS,
                       NormalizationVocabulary.OTHER):
        tokens_of_stage_2 |= set(vocabulary.values())

    for groups in ProfileVocabulary.GROUPS.values():
        for group in groups:
            assert set(group) <= tokens_of_stage_2


def test_sequence_of_stage_2_follows_the_groups_of_the_automaton():
    # Stage 2 sorts with ProfileVocabulary.GROUPS, the same groups used
    # to build the automata, so every sorted sequence follows the
    # order of the groups.
    tokens = [token for groups in ProfileVocabulary.GROUPS.values()
              for group in groups for token in group]

    for profile, groups in ProfileVocabulary.GROUPS.items():
        order = [token for group in groups for token in group]
        assert ResumeNormalizer.sort_for_profile(list(reversed(tokens)), profile) == order


def test_statement_example_full_stack():
    text = """
    Wednesday Addams
    3 years of experience developing web applications.
    Technical Skills:
    JS, React.js, NodeJS, Postgres, Git.
    """

    result = classify_text(text)

    assert result[FS] == ACCEPTED
    assert result[ML] == REJECTED


def test_statement_example_machine_learning():
    # Contains PANDAS and NUMPY, and SCIKIT_LEARN and TENSORFLOW:
    # the loops of q2 and q3 are needed to accept it.
    text = """
    Mary Jane Watson
    2 years of experience developing predictive models and data-processing pipelines.
    Technical Skills:
    Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.
    """

    result = classify_text(text)

    assert result[ML] == ACCEPTED
    assert result[FS] == REJECTED


def test_order_of_the_resume_does_not_matter():
    text = "Skills: Git, NodeJS, JS, Postgres, React.js"

    assert classify_text(text)[FS] == ACCEPTED


def test_cybersecurity_and_data_engineer_examples():
    sec = "Python, Linux, TCP/IP, Docker, Nmap, Git."
    de = "Python, SQL, Spark, Airflow, PostgreSQL, ETL, Git."

    assert classify_text(sec)[SEC] == ACCEPTED
    assert classify_text(de)[DE] == ACCEPTED


def test_classify_returns_the_four_profiles():
    result = classify_text("")

    assert set(result) == {FS, ML, SEC, DE}
    assert set(result.values()) == {REJECTED}


# -------------------------------------------------------------------
# Example of the guide (A_ML)
# -------------------------------------------------------------------

def test_guide_example():
    sequence = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]

    assert AUTOMATA.accepts(ML, sequence)


# -------------------------------------------------------------------
# Accepted and rejected patterns
# -------------------------------------------------------------------

def test_several_tokens_of_the_same_group_are_accepted():
    assert AUTOMATA.accepts(FS, ["JAVASCRIPT", "TYPESCRIPT", "REACT", "VUE",
                                 "NODE_JS", "DJANGO", "SQL", "NOSQL", "GIT"])


def test_optional_groups_present_or_missing():
    # Full Stack with and without REST_API
    assert AUTOMATA.accepts(FS, ["JAVASCRIPT", "REACT", "NODE_JS", "REST_API", "SQL", "GIT"])
    assert AUTOMATA.accepts(FS, ["JAVASCRIPT", "REACT", "NODE_JS", "SQL", "GIT"])

    # ML with and without ML development
    assert AUTOMATA.accepts(ML, ["PYTHON", "NUMPY", "PYTORCH", "MACHINE_LEARNING", "SQL", "GIT"])

    # Cybersecurity without containers
    assert AUTOMATA.accepts(SEC, ["BASH", "LINUX", "NETWORKING", "NMAP", "GIT"])

    # Data Engineer without Airflow
    assert AUTOMATA.accepts(DE, ["SQL", "SPARK", "ELT", "NOSQL", "GIT"])


def test_missing_mandatory_group_is_rejected():
    # Without backend
    assert not AUTOMATA.accepts(FS, ["JAVASCRIPT", "REACT", "SQL", "GIT"])
    # Without GIT
    assert not AUTOMATA.accepts(ML, ["PYTHON", "PANDAS", "TENSORFLOW", "SQL"])
    # Without LINUX
    assert not AUTOMATA.accepts(SEC, ["PYTHON", "TCP_IP", "NMAP", "GIT"])
    # Without SPARK
    assert not AUTOMATA.accepts(DE, ["PYTHON", "ETL", "POSTGRESQL", "GIT"])


def test_unsorted_or_foreign_tokens_are_rejected():
    # GIT must be the last group
    assert not AUTOMATA.accepts(ML, ["GIT", "PYTHON", "PANDAS", "TENSORFLOW", "SQL"])
    # REACT does not belong to the ML profile
    assert not AUTOMATA.accepts(ML, ["PYTHON", "PANDAS", "REACT", "TENSORFLOW", "SQL", "GIT"])


def test_empty_sequence_is_rejected():
    for profile in (FS, ML, SEC, DE):
        assert not AUTOMATA.accepts(profile, [])


# -------------------------------------------------------------------
# Structure of the automata (must match docs/07_automata_design.md)
# -------------------------------------------------------------------

def test_automata_are_deterministic():
    for transitions in AUTOMATA.transitions.values():
        pairs = [(source, token) for source, token, _ in transitions]
        assert len(pairs) == len(set(pairs))


def test_size_of_the_automata():
    expected_transitions = {FS: 27, ML: 22, SEC: 23, DE: 22}

    for profile, dfa in AUTOMATA.automata.items():
        assert len(dfa.states) == 7
        assert len(AUTOMATA.transitions[profile]) == expected_transitions[profile]
