"""
Canonical order of the qualifications of each professional profile.

Before the normalized tokens are sent to the automata, they are
organized in the order defined by each profile. In this way, the
result does not depend on the order in which the candidate wrote
the qualifications.

See docs/06_fst_design.md, Section 7.
"""

FULL_STACK_DEVELOPER = "FULL_STACK_DEVELOPER"
MACHINE_LEARNING_ENGINEER = "MACHINE_LEARNING_ENGINEER"
CYBERSECURITY_ENGINEER = "CYBERSECURITY_ENGINEER"
DATA_ENGINEER = "DATA_ENGINEER"


FULL_STACK_ORDER = [
    # Frontend language
    "JAVASCRIPT", "TYPESCRIPT",
    # Frontend framework
    "REACT", "ANGULAR", "VUE",
    # Backend
    "NODE_JS", "DJANGO", "SPRING_BOOT",
    # API
    "REST_API",
    # Database
    "SQL", "POSTGRESQL", "NOSQL",
    # Version control
    "GIT",
]

MACHINE_LEARNING_ORDER = [
    # Language
    "PYTHON",
    # Data libraries
    "PANDAS", "NUMPY",
    # ML libraries
    "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH",
    # ML development
    "MACHINE_LEARNING", "ML_MODEL_DEVELOPMENT",
    # Database
    "SQL", "POSTGRESQL",
    # Version control
    "GIT",
]

CYBERSECURITY_ORDER = [
    # Scripting
    "PYTHON", "BASH",
    # Networking
    "NETWORKING", "TCP_IP",
    # Security
    "CYBERSECURITY", "NMAP", "VULNERABILITY_ASSESSMENT", "SECURITY_AUTOMATION",
    # Containers
    "DOCKER", "KUBERNETES",
    # Version control
    "GIT",
]

DATA_ENGINEER_ORDER = [
    # Language
    "PYTHON", "SQL",
    # Processing
    "SPARK",
    # Orchestration
    "AIRFLOW",
    # Data integration
    "ETL", "ELT", "DATA_PIPELINE",
    # Storage
    "DATA_WAREHOUSING", "POSTGRESQL", "NOSQL",
    # Version control
    "GIT",
]


PROFILE_ORDERS = {
    FULL_STACK_DEVELOPER: FULL_STACK_ORDER,
    MACHINE_LEARNING_ENGINEER: MACHINE_LEARNING_ORDER,
    CYBERSECURITY_ENGINEER: CYBERSECURITY_ORDER,
    DATA_ENGINEER: DATA_ENGINEER_ORDER,
}


def sort_for_profile(tokens: list[str], profile: str) -> list[str]:
    """
    Organize the tokens in the canonical order of a profile.

    - Only the tokens of the profile are kept.
    - Each token appears at most once.
    - The tokens follow the position of the order table.

    Args:
        tokens: Normalized tokens in any order.
        profile: Name of the profile (key of PROFILE_ORDERS).

    Returns:
        Sorted sequence for the automaton of the profile.
    """

    order = PROFILE_ORDERS[profile]
    kept = {token for token in tokens if token in order}

    return sorted(kept, key=order.index)
