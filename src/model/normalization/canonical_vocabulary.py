"""
Canonical vocabulary used by the ResumeLens normalization stage.

Each dictionary maps an input variant (already preprocessed:
lowercase and single spaces) to its canonical token.

These tables are the single source of truth of the stage:
the finite-state transducers are generated automatically
from them (see fst_builder.py).

This module only defines data. It does not build transducers.
"""

# -------------------------------------------------------------------
# Programming languages
# -------------------------------------------------------------------

LANGUAGES_VOCABULARY = {
    "javascript": "JAVASCRIPT",
    "js": "JAVASCRIPT",
    "typescript": "TYPESCRIPT",
    "python": "PYTHON",
    "sql": "SQL",
    "bash": "BASH",
}


# -------------------------------------------------------------------
# Frameworks and libraries
# -------------------------------------------------------------------

FRAMEWORKS_VOCABULARY = {
    "react": "REACT",
    "react.js": "REACT",
    "reactjs": "REACT",
    "angular": "ANGULAR",
    "vue": "VUE",
    "node.js": "NODE_JS",
    "nodejs": "NODE_JS",
    "django": "DJANGO",
    "spring boot": "SPRING_BOOT",
    "pandas": "PANDAS",
    "numpy": "NUMPY",
    "scikit-learn": "SCIKIT_LEARN",
    "scikit learn": "SCIKIT_LEARN",
    "scikitlearn": "SCIKIT_LEARN",
    "sklearn": "SCIKIT_LEARN",
    "tensorflow": "TENSORFLOW",
    "tensor flow": "TENSORFLOW",
    "pytorch": "PYTORCH",
    "py torch": "PYTORCH",
    "apache spark": "SPARK",
    "spark": "SPARK",
    "apache airflow": "AIRFLOW",
    "airflow": "AIRFLOW",
}


# -------------------------------------------------------------------
# Databases
# -------------------------------------------------------------------

DATABASES_VOCABULARY = {
    "postgresql": "POSTGRESQL",
    "postgres": "POSTGRESQL",
    "nosql": "NOSQL",
    "sql": "SQL",
}


# -------------------------------------------------------------------
# Tools and technologies
# -------------------------------------------------------------------

TOOLS_VOCABULARY = {
    "git": "GIT",
    "docker": "DOCKER",
    "kubernetes": "KUBERNETES",
    "nmap": "NMAP",
    "linux": "LINUX",
    "tcp/ip": "TCP_IP",
    "tcp ip": "TCP_IP",
    "tcp / ip": "TCP_IP",
    "tcp /ip": "TCP_IP",
    "tcp/ ip": "TCP_IP",
    "tcpip": "TCP_IP",
    "networking": "NETWORKING",
    "network": "NETWORKING",
    "etl": "ETL",
    "elt": "ELT",
    "data pipeline": "DATA_PIPELINE",
    "data pipelines": "DATA_PIPELINE",
    "data warehouse": "DATA_WAREHOUSING",
    "data warehousing": "DATA_WAREHOUSING",
}


# -------------------------------------------------------------------
# Other relevant qualifications
# -------------------------------------------------------------------

OTHER_VOCABULARY = {
    "machine learning": "MACHINE_LEARNING",
    "machine-learning": "MACHINE_LEARNING",
    "machine learning model development": "ML_MODEL_DEVELOPMENT",
    "machine-learning model development": "ML_MODEL_DEVELOPMENT",
    "rest api": "REST_API",
    "rest apis": "REST_API",
    "vulnerability assessment": "VULNERABILITY_ASSESSMENT",
    "cybersecurity": "CYBERSECURITY",
    "cyber security": "CYBERSECURITY",
    "security automation": "SECURITY_AUTOMATION",
}


# -------------------------------------------------------------------
# Academic qualifications
# -------------------------------------------------------------------

ACADEMIC_VOCABULARY = {
    "bachelor": "BACHELOR",
    "bachelor's": "BACHELOR",
    "bsc": "BACHELOR",
    "bsc.": "BACHELOR",
    "b.sc": "BACHELOR",
    "b.sc.": "BACHELOR",
    "master": "MASTER",
    "master's": "MASTER",
    "msc": "MASTER",
    "msc.": "MASTER",
    "m.sc": "MASTER",
    "m.sc.": "MASTER",
    "phd": "PHD",
    "phd.": "PHD",
    "ph.d": "PHD",
    "ph.d.": "PHD",
    "computer science": "COMPUTER_SCIENCE",
    "software engineering": "SOFTWARE_ENGINEERING",
    "systems engineering": "SYSTEMS_ENGINEERING",
    "data science": "DATA_SCIENCE",
}
