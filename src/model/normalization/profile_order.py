"""
Canonical order of the qualifications of each professional profile.

Before the normalized tokens are sent to the automata, they are
organized in the order defined by each profile. In this way, the
result does not depend on the order in which the candidate wrote
the qualifications.

Each profile is defined as an ordered list of GROUPS. A group
contains equivalent alternatives of the profile pattern
(for example, PANDAS or NUMPY).

Contract with the recognition stage (automata):

- The sequence of a profile follows the order of its groups.
- A candidate can have MORE THAN ONE token of the same group
  (for example, PANDAS and NUMPY). All of them are kept, in the
  order of the group, so no information is lost.
- Deciding which groups are mandatory, and accepting one or more
  tokens per group, is the responsibility of the automata.
  PROFILE_GROUPS is exported so that the automata can be built
  from the same definition.

See docs/06_fst_design.md, Section 7.
"""

FULL_STACK_DEVELOPER = "FULL_STACK_DEVELOPER"
MACHINE_LEARNING_ENGINEER = "MACHINE_LEARNING_ENGINEER"
CYBERSECURITY_ENGINEER = "CYBERSECURITY_ENGINEER"
DATA_ENGINEER = "DATA_ENGINEER"


FULL_STACK_GROUPS = [
    ["JAVASCRIPT", "TYPESCRIPT"],           # Frontend language
    ["REACT", "ANGULAR", "VUE"],            # Frontend framework
    ["NODE_JS", "DJANGO", "SPRING_BOOT"],   # Backend
    ["REST_API"],                           # API
    ["SQL", "POSTGRESQL", "NOSQL"],         # Database
    ["GIT"],                                # Version control
]

MACHINE_LEARNING_GROUPS = [
    ["PYTHON"],                                     # Language
    ["PANDAS", "NUMPY"],                            # Data libraries
    ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"],      # ML libraries
    ["MACHINE_LEARNING", "ML_MODEL_DEVELOPMENT"],   # ML development
    ["SQL", "POSTGRESQL"],                          # Database
    ["GIT"],                                        # Version control
]

CYBERSECURITY_GROUPS = [
    ["PYTHON", "BASH"],                     # Scripting
    ["LINUX"],                              # Operating system
    ["NETWORKING", "TCP_IP"],               # Networking
    ["CYBERSECURITY", "NMAP",
     "VULNERABILITY_ASSESSMENT",
     "SECURITY_AUTOMATION"],                # Security
    ["DOCKER", "KUBERNETES"],               # Containers
    ["GIT"],                                # Version control
]

DATA_ENGINEER_GROUPS = [
    ["PYTHON", "SQL"],                          # Language
    ["SPARK"],                                  # Processing
    ["AIRFLOW"],                                # Orchestration
    ["ETL", "ELT", "DATA_PIPELINE"],            # Data integration
    ["DATA_WAREHOUSING", "POSTGRESQL", "NOSQL"],  # Storage
    ["GIT"],                                    # Version control
]


PROFILE_GROUPS = {
    FULL_STACK_DEVELOPER: FULL_STACK_GROUPS,
    MACHINE_LEARNING_ENGINEER: MACHINE_LEARNING_GROUPS,
    CYBERSECURITY_ENGINEER: CYBERSECURITY_GROUPS,
    DATA_ENGINEER: DATA_ENGINEER_GROUPS,
}


def _flatten(groups: list[list[str]]) -> list[str]:
    """
    Join the groups of a profile into a single ordered list.
    """

    return [token for group in groups for token in group]


FULL_STACK_ORDER = _flatten(FULL_STACK_GROUPS)
MACHINE_LEARNING_ORDER = _flatten(MACHINE_LEARNING_GROUPS)
CYBERSECURITY_ORDER = _flatten(CYBERSECURITY_GROUPS)
DATA_ENGINEER_ORDER = _flatten(DATA_ENGINEER_GROUPS)


PROFILE_ORDERS = {
    profile: _flatten(groups)
    for profile, groups in PROFILE_GROUPS.items()
}


def sort_for_profile(tokens: list[str], profile: str) -> list[str]:
    """
    Organize the tokens in the canonical order of a profile.

    - Only the tokens of the profile are kept.
    - Each token appears at most once.
    - The tokens follow the order of the groups of the profile.
      If several tokens belong to the same group, all of them
      are kept (see the contract in the module docstring).

    Args:
        tokens: Normalized tokens in any order.
        profile: Name of the profile (key of PROFILE_ORDERS).

    Returns:
        Sorted sequence for the automaton of the profile.
    """

    order = PROFILE_ORDERS[profile]
    kept = {token for token in tokens if token in order}

    return sorted(kept, key=order.index)
