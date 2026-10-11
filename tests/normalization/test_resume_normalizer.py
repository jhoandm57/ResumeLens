from src.model.extraction.extracted_data import ExtractedData
from src.model.extraction.resume_extractor import extract_resume_information
from src.model.normalization.normalized_data import NormalizedData
from src.model.classification.profile_vocabulary import (
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
)
from src.model.normalization.resume_normalizer import ResumeNormalizer


NORMALIZER = ResumeNormalizer()
sort_for_profile = ResumeNormalizer.sort_for_profile


def test_returns_expected_type():
    result = NORMALIZER.normalize(ExtractedData())

    assert isinstance(result, NormalizedData)


def test_full_stack_example_from_statement():
    resume = """
    Wednesday Addams
    3 years of experience developing web applications.
    Technical Skills:
    JS, React.js, NodeJS, Postgres, Git.
    """

    result = NORMALIZER.normalize(extract_resume_information(resume))

    assert result.programming_languages == ["JAVASCRIPT"]
    assert result.frameworks_libraries == ["REACT", "NODE_JS"]
    assert result.databases == ["POSTGRESQL"]
    assert result.tools_technologies == ["GIT"]
    assert result.experience_years == 3

    assert result.profile_sequences[FULL_STACK_DEVELOPER] == [
        "JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT",
    ]
    assert result.profile_sequences[MACHINE_LEARNING_ENGINEER] == [
        "POSTGRESQL", "GIT",
    ]
    assert result.profile_sequences[CYBERSECURITY_ENGINEER] == ["GIT"]
    assert result.profile_sequences[DATA_ENGINEER] == ["POSTGRESQL", "GIT"]


def test_order_does_not_depend_on_resume():
    resume = "Skills: Git, NodeJS, JS, Postgres, React.js"

    result = NORMALIZER.normalize(extract_resume_information(resume))

    assert result.profile_sequences[FULL_STACK_DEVELOPER] == [
        "JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT",
    ]


def test_machine_learning_example_from_statement():
    resume = """
    Mary Jane Watson
    2 years of experience developing predictive models.
    Technical Skills:
    Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.
    """

    result = NORMALIZER.normalize(extract_resume_information(resume))

    assert result.experience_years == 2
    assert result.profile_sequences[MACHINE_LEARNING_ENGINEER] == [
        "PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT",
    ]


def test_duplicates_and_sql_appear_once():
    extracted = ExtractedData(
        programming_languages=["JS", "JavaScript", "SQL"],
        databases=["SQL"],
    )

    result = NORMALIZER.normalize(extracted)

    assert result.programming_languages == ["JAVASCRIPT", "SQL"]
    assert result.qualifications.count("SQL") == 1
    assert result.qualifications.count("JAVASCRIPT") == 1


def test_maximum_experience_is_kept():
    extracted = ExtractedData(
        professional_experience=["2 years of experience", "4 years experience"],
    )

    assert NORMALIZER.normalize(extracted).experience_years == 4


def test_experience_entries_are_kept_as_written():
    extracted = ExtractedData(
        professional_experience=[
            "2 years of experience",
            "4 years experience",
            "2 years of experience",       # duplicate
        ],
    )

    result = NORMALIZER.normalize(extracted)

    assert result.experience_entries == ["2 years of experience", "4 years experience"]
    assert result.experience_years == 4


def test_experience_entries_from_resume_text():
    resume = "4 years of professional experience in Python. Also 5+ yrs experience with Git."

    result = NORMALIZER.normalize(extract_resume_information(resume))

    assert result.experience_entries == [
        "4 years of professional experience",
        "5+ yrs experience",
    ]
    assert result.experience_years == 5


def test_unknown_values_are_ignored():
    extracted = ExtractedData(databases=["MySQL", "Postgres"])

    assert NORMALIZER.normalize(extracted).databases == ["POSTGRESQL"]


def test_empty_resume():
    result = NORMALIZER.normalize(ExtractedData())

    assert result.qualifications == []
    assert result.experience_years is None
    assert result.experience_entries == []
    assert all(sequence == [] for sequence in result.profile_sequences.values())


def test_contact_information_is_kept():
    resume = "Peter Parker peter@mail.com +57 300 123 4567"

    result = NORMALIZER.normalize(extract_resume_information(resume))

    assert result.emails == ["peter@mail.com"]
    assert result.phones == ["+57 300 123 4567"]


def test_cybersecurity_example_of_the_profiles():
    # Example of docs/04_profiles.md (Peter Parker)
    resume = """
    Peter Parker
    2 years of experience in infrastructure security and security automation.
    Technical Skills:
    Python, Linux, TCP/IP, Docker, Nmap, Git.
    """

    result = NORMALIZER.normalize(extract_resume_information(resume))

    assert result.profile_sequences[CYBERSECURITY_ENGINEER] == [
        "PYTHON", "LINUX", "TCP_IP", "NMAP", "SECURITY_AUTOMATION", "DOCKER", "GIT",
    ]


def test_everything_extracted_by_stage_1_is_normalized():
    # If a variant is added to the regular expressions but not to the
    # vocabulary, this test fails instead of losing the value silently.
    resume = """
    JavaScript, Javascript, JS, TypeScript, Python, SQL, Bash.
    React, React.js, ReactJS, Angular, Vue, Node.js, NodeJS, Django,
    Spring Boot, Pandas, NumPy, Scikit-learn, Scikit learn, Scikitlearn,
    sklearn, TensorFlow, Tensor Flow, PyTorch, Py Torch, Apache Spark,
    Spark, Apache Airflow, Airflow.
    PostgreSQL, Postgres, NoSQL.
    Git, Docker, Kubernetes, Nmap, Linux, TCP/IP, TCP IP, TCP / IP, TCPIP,
    Networking, Network, ETL, ELT, Data Pipeline, Data Pipelines,
    Data Warehouse, Data Warehousing.
    Machine Learning Model Development, Machine-Learning, REST API, REST APIs,
    Vulnerability Assessment, Cybersecurity, Cyber Security, Security Automation.
    Bachelor's, Bachelor’s, B.Sc., BSc, Master's, M.Sc., MSc, Ph.D., PhD,
    Computer Science, Software Engineering, Systems Engineering, Data Science.
    3 years of experience, 5+ yrs experience, 4 years of professional experience.
    """

    extracted = extract_resume_information(resume)

    t = NORMALIZER.transducers
    categories = [
        (t.languages, extracted.programming_languages),
        (t.frameworks, extracted.frameworks_libraries),
        (t.databases, extracted.databases),
        (t.tools, extracted.tools_technologies),
        (t.other, extracted.other_qualifications),
        (t.academic, extracted.academic_qualifications),
        (t.experience, extracted.professional_experience),
    ]

    for fst, values in categories:
        assert values != []

        for value in values:
            assert t.translate(fst, value) is not None, value


def test_name_is_copied_without_changes():
    extracted = ExtractedData(name="Wednesday Addams", programming_languages=["JS"])

    result = NORMALIZER.normalize(extracted)

    assert result.name == "Wednesday Addams"
    assert NORMALIZER.normalize(ExtractedData()).name is None


# -------------------------------------------------------------------
# Sorting by profile (canonical order)
# -------------------------------------------------------------------

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
