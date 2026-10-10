from src.model.classification.classification_result import ACCEPTED, REJECTED
from src.model.classification.resume_classifier import (
    classify_sequence,
    classify_tokens,
    classify_resume,
)
from src.model.extraction.resume_extractor import extract_resume_information
from src.model.normalization.resume_normalizer import normalize_resume
from src.model.normalization.profile_order import (
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
)
from src.model.pipeline import run_pipeline


# -------------------------------------------------------------------
# ACCEPTED sequences
# -------------------------------------------------------------------

ACCEPTED_CASES = [
    # Full Stack: example of the statement
    (FULL_STACK_DEVELOPER, ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]),
    # Full Stack: several tokens per group and the optional REST_API
    (FULL_STACK_DEVELOPER, ["TYPESCRIPT", "ANGULAR", "VUE", "SPRING_BOOT",
                            "REST_API", "SQL", "NOSQL", "GIT"]),
    # Machine Learning: example of Stage 3 of the statement
    (MACHINE_LEARNING_ENGINEER, ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]),
    # Machine Learning: optional ML development present
    (MACHINE_LEARNING_ENGINEER, ["PYTHON", "NUMPY", "PYTORCH",
                                 "ML_MODEL_DEVELOPMENT", "SQL", "GIT"]),
    # Cybersecurity: Peter Parker
    (CYBERSECURITY_ENGINEER, ["PYTHON", "LINUX", "TCP_IP", "NMAP", "DOCKER", "GIT"]),
    # Cybersecurity: without the optional Containers group
    (CYBERSECURITY_ENGINEER, ["BASH", "LINUX", "NETWORKING",
                              "VULNERABILITY_ASSESSMENT", "GIT"]),
    # Data Engineer: Clark Kent
    (DATA_ENGINEER, ["PYTHON", "SQL", "SPARK", "AIRFLOW", "ETL", "POSTGRESQL", "GIT"]),
    # Data Engineer: without the optional Orchestration group
    (DATA_ENGINEER, ["SQL", "SPARK", "ELT", "DATA_PIPELINE", "DATA_WAREHOUSING", "GIT"]),
]


# -------------------------------------------------------------------
# REJECTED sequences (incomplete or wrong) and the missing groups
# -------------------------------------------------------------------

REJECTED_CASES = [
    (FULL_STACK_DEVELOPER, ["JAVASCRIPT", "REACT", "POSTGRESQL", "GIT"], ["Backend"]),
    (FULL_STACK_DEVELOPER, ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL"],
     ["Version control"]),
    (FULL_STACK_DEVELOPER, [], ["Frontend language", "Frontend framework",
                                "Backend", "Database", "Version control"]),
    (MACHINE_LEARNING_ENGINEER, ["PYTHON", "PANDAS", "NUMPY", "SQL", "GIT"],
     ["ML libraries"]),
    (MACHINE_LEARNING_ENGINEER, ["PANDAS", "SCIKIT_LEARN", "SQL", "GIT"], ["Language"]),
    (CYBERSECURITY_ENGINEER, ["PYTHON", "LINUX", "NMAP", "DOCKER", "GIT"],
     ["Networking"]),
    (CYBERSECURITY_ENGINEER, ["PYTHON", "LINUX", "TCP_IP", "DOCKER", "GIT"],
     ["Security"]),
    (DATA_ENGINEER, ["PYTHON", "SQL", "AIRFLOW", "ETL", "POSTGRESQL", "GIT"],
     ["Processing"]),
    (DATA_ENGINEER, ["PYTHON", "SPARK", "AIRFLOW", "ETL", "GIT"], ["Storage"]),
]


def test_accepted_sequences():
    for profile, sequence in ACCEPTED_CASES:
        decision = classify_sequence(profile, sequence)

        assert decision.result == ACCEPTED, (profile, sequence)
        assert decision.missing_groups == []


def test_rejected_sequences():
    for profile, sequence, missing in REJECTED_CASES:
        decision = classify_sequence(profile, sequence)

        assert decision.result == REJECTED, (profile, sequence)
        assert decision.missing_groups == missing


def test_wrong_order_is_rejected_but_classify_tokens_sorts_first():
    unsorted = ["GIT", "POSTGRESQL", "TENSORFLOW", "PANDAS", "PYTHON"]

    assert classify_sequence(MACHINE_LEARNING_ENGINEER, unsorted).result == REJECTED
    assert classify_tokens(unsorted, MACHINE_LEARNING_ENGINEER).result == ACCEPTED


def test_decision_keeps_the_run():
    decision = classify_sequence(
        FULL_STACK_DEVELOPER,
        ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
    )

    assert decision.automaton == "A_FS"
    assert decision.final_state == "q13"
    assert len(decision.trace) == 5


def test_rejection_in_trap_state():
    decision = classify_sequence(DATA_ENGINEER, ["POSTGRESQL", "GIT"])

    assert decision.final_state == "q_trap"
    assert decision.result == REJECTED


# -------------------------------------------------------------------
# Complete pipeline (regex -> FST -> DFA)
# -------------------------------------------------------------------

WEDNESDAY = """Wednesday Addams
3 years of experience developing web applications.
Technical Skills:
JS, React.js, NodeJS, Postgres, Git.
"""

MARY_JANE = """Mary Jane Watson
2 years of experience developing predictive models and data-processing pipelines.
Technical Skills:
Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.
"""

PETER = """Peter Parker
2 years of experience in infrastructure security and security automation.
Technical Skills:
Python, Linux, TCP/IP, Docker, Nmap, Git.
"""

CLARK = """Clark Kent
3 years of experience developing data pipelines and data-processing systems.
Technical Skills:
Python, SQL, Spark, Airflow, PostgreSQL, ETL, Git.
"""


def test_reference_resumes_are_accepted_by_their_profile():
    cases = [
        (WEDNESDAY, FULL_STACK_DEVELOPER),
        (MARY_JANE, MACHINE_LEARNING_ENGINEER),
        (PETER, CYBERSECURITY_ENGINEER),
        (CLARK, DATA_ENGINEER),
    ]

    for text, profile in cases:
        result = run_pipeline(text)

        assert result.result_of(profile) == ACCEPTED, profile


def test_wednesday_is_accepted_only_as_full_stack():
    result = run_pipeline(WEDNESDAY)

    assert result.accepted_profiles == [FULL_STACK_DEVELOPER]


def test_classify_resume_receives_normalized_data():
    normalized = normalize_resume(extract_resume_information(MARY_JANE))

    result = classify_resume(normalized)

    assert result.normalized is normalized
    assert list(result.decisions) == [
        FULL_STACK_DEVELOPER,
        MACHINE_LEARNING_ENGINEER,
        CYBERSECURITY_ENGINEER,
        DATA_ENGINEER,
    ]


def test_resume_without_qualifications_is_rejected_by_all_profiles():
    result = run_pipeline("John Smith\nI like football and music.")

    assert result.accepted_profiles == []
