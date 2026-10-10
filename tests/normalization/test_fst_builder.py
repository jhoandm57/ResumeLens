from src.model.normalization.canonical_vocabulary import (
    LANGUAGES_VOCABULARY,
    FRAMEWORKS_VOCABULARY,
    DATABASES_VOCABULARY,
    TOOLS_VOCABULARY,
    OTHER_VOCABULARY,
    ACADEMIC_VOCABULARY,
)
from src.model.normalization.fst_builder import (
    preprocess,
    build_dictionary_fst,
    build_experience_fst,
    translate,
)


LANGUAGES_FST = build_dictionary_fst(LANGUAGES_VOCABULARY)
FRAMEWORKS_FST = build_dictionary_fst(FRAMEWORKS_VOCABULARY)
DATABASES_FST = build_dictionary_fst(DATABASES_VOCABULARY)
TOOLS_FST = build_dictionary_fst(TOOLS_VOCABULARY)
OTHER_FST = build_dictionary_fst(OTHER_VOCABULARY)
ACADEMIC_FST = build_dictionary_fst(ACADEMIC_VOCABULARY)
EXPERIENCE_FST = build_experience_fst()


def test_preprocess():
    assert preprocess("  Tensor   Flow ") == "tensor flow"
    assert preprocess("Bachelor’s") == "bachelor's"


def test_languages_fst():
    assert translate(LANGUAGES_FST, "JS") == "JAVASCRIPT"
    assert translate(LANGUAGES_FST, "Javascript") == "JAVASCRIPT"
    assert translate(LANGUAGES_FST, "JavaScript") == "JAVASCRIPT"
    assert translate(LANGUAGES_FST, "TypeScript") == "TYPESCRIPT"
    assert translate(LANGUAGES_FST, "Python") == "PYTHON"
    assert translate(LANGUAGES_FST, "SQL") == "SQL"
    assert translate(LANGUAGES_FST, "Bash") == "BASH"


def test_frameworks_fst():
    assert translate(FRAMEWORKS_FST, "React") == "REACT"
    assert translate(FRAMEWORKS_FST, "React.js") == "REACT"
    assert translate(FRAMEWORKS_FST, "ReactJS") == "REACT"
    assert translate(FRAMEWORKS_FST, "NodeJS") == "NODE_JS"
    assert translate(FRAMEWORKS_FST, "Node.js") == "NODE_JS"
    assert translate(FRAMEWORKS_FST, "Spring Boot") == "SPRING_BOOT"
    assert translate(FRAMEWORKS_FST, "Scikit-learn") == "SCIKIT_LEARN"
    assert translate(FRAMEWORKS_FST, "scikit learn") == "SCIKIT_LEARN"
    assert translate(FRAMEWORKS_FST, "sklearn") == "SCIKIT_LEARN"
    assert translate(FRAMEWORKS_FST, "Tensor Flow") == "TENSORFLOW"
    assert translate(FRAMEWORKS_FST, "  Tensor   Flow ") == "TENSORFLOW"
    assert translate(FRAMEWORKS_FST, "PyTorch") == "PYTORCH"
    assert translate(FRAMEWORKS_FST, "Py Torch") == "PYTORCH"
    assert translate(FRAMEWORKS_FST, "Apache Spark") == "SPARK"
    assert translate(FRAMEWORKS_FST, "Airflow") == "AIRFLOW"


def test_databases_fst():
    assert translate(DATABASES_FST, "Postgres") == "POSTGRESQL"
    assert translate(DATABASES_FST, "PostgreSQL") == "POSTGRESQL"
    assert translate(DATABASES_FST, "NoSQL") == "NOSQL"
    assert translate(DATABASES_FST, "SQL") == "SQL"


def test_tools_fst():
    assert translate(TOOLS_FST, "Git") == "GIT"
    assert translate(TOOLS_FST, "Linux") == "LINUX"
    assert translate(TOOLS_FST, "TCP/IP") == "TCP_IP"
    assert translate(TOOLS_FST, "TCP / IP") == "TCP_IP"
    assert translate(TOOLS_FST, "TCP IP") == "TCP_IP"
    assert translate(TOOLS_FST, "Network") == "NETWORKING"
    assert translate(TOOLS_FST, "Data Pipelines") == "DATA_PIPELINE"
    assert translate(TOOLS_FST, "Data Warehouse") == "DATA_WAREHOUSING"


def test_other_fst():
    assert translate(OTHER_FST, "Machine Learning") == "MACHINE_LEARNING"
    assert translate(OTHER_FST, "Machine-Learning") == "MACHINE_LEARNING"
    assert translate(OTHER_FST, "Machine Learning Model Development") == "ML_MODEL_DEVELOPMENT"
    assert translate(OTHER_FST, "REST APIs") == "REST_API"
    assert translate(OTHER_FST, "Cyber Security") == "CYBERSECURITY"


def test_academic_fst():
    assert translate(ACADEMIC_FST, "Bachelor’s") == "BACHELOR"
    assert translate(ACADEMIC_FST, "B.Sc.") == "BACHELOR"
    assert translate(ACADEMIC_FST, "MSc") == "MASTER"
    assert translate(ACADEMIC_FST, "Ph.D.") == "PHD"
    assert translate(ACADEMIC_FST, "Computer Science") == "COMPUTER_SCIENCE"


def test_experience_fst():
    assert translate(EXPERIENCE_FST, "3 years of experience") == "3"
    assert translate(EXPERIENCE_FST, "5+ yrs experience") == "5"
    assert translate(EXPERIENCE_FST, "2 yrs of experience") == "2"
    assert translate(EXPERIENCE_FST, "10 years experience") == "10"
    assert translate(EXPERIENCE_FST, "3years experience") == "3"
    assert translate(EXPERIENCE_FST, "4 years of professional experience") == "4"
    assert translate(EXPERIENCE_FST, "3 YEARS OF EXPERIENCE") == "3"


def test_rejected_inputs():
    assert translate(DATABASES_FST, "mysql") is None
    assert translate(FRAMEWORKS_FST, "Node") is None
    assert translate(LANGUAGES_FST, "") is None
    assert translate(EXPERIENCE_FST, "years of experience") is None


def test_number_of_states():
    # Must match the table of docs/06_fst_design.md, Section 6.8
    assert len(LANGUAGES_FST.states) == 36
    assert len(FRAMEWORKS_FST.states) == 140
    assert len(DATABASES_FST.states) == 20
    assert len(TOOLS_FST.states) == 89
    assert len(OTHER_FST.states) == 137
    assert len(ACADEMIC_FST.states) == 107
    assert len(EXPERIENCE_FST.states) == 37


def test_experience_fst_rejects_text_that_is_not_experience():
    assert translate(EXPERIENCE_FST, "3 bananas") is None
    assert translate(EXPERIENCE_FST, "3 years of experience.") is None
    assert translate(EXPERIENCE_FST, "3 of experience") is None
    assert translate(EXPERIENCE_FST, "No professional experience") is None
