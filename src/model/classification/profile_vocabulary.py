"""
Vocabulary that each automaton accepts for a professional profile.

Every profile is divided into GROUPS of equivalent tokens (for example,
PANDAS or NUMPY). The candidate needs at least one token of every
mandatory group; optional groups may be missing.

This is the ONLY definition of the groups in the project:

- The normalization stage (ResumeNormalizer.sort_for_profile) uses
  GROUPS to sort the tokens of each profile.
- The classification stage (ProfileAutomata) uses the same groups to
  build the transitions of each automaton.

So the order of the sequence and the order expected by the automaton
always come from the same place.

See docs/07_automata_design.md, Section 4.
"""


# Names of the four profiles
FULL_STACK_DEVELOPER = "FULL_STACK_DEVELOPER"
MACHINE_LEARNING_ENGINEER = "MACHINE_LEARNING_ENGINEER"
CYBERSECURITY_ENGINEER = "CYBERSECURITY_ENGINEER"
DATA_ENGINEER = "DATA_ENGINEER"


class ProfileVocabulary:
    """
    Canonical tokens accepted by each group of each profile.
    """

    # ---------------------------------------------------------------
    # Full Stack Developer (automaton A_FS)
    # ---------------------------------------------------------------

    FS_FRONTEND_LANGUAGE = ["JAVASCRIPT", "TYPESCRIPT"]
    FS_FRONTEND_FRAMEWORK = ["REACT", "ANGULAR", "VUE"]
    FS_BACKEND = ["NODE_JS", "DJANGO", "SPRING_BOOT"]
    FS_API = ["REST_API"]                           # optional
    FS_DATABASE = ["SQL", "POSTGRESQL", "NOSQL"]
    FS_VERSION_CONTROL = ["GIT"]

    # ---------------------------------------------------------------
    # Machine Learning Engineer (automaton A_ML)
    # ---------------------------------------------------------------

    ML_LANGUAGE = ["PYTHON"]
    ML_DATA_LIBRARIES = ["PANDAS", "NUMPY"]
    ML_LIBRARIES = ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"]
    ML_DEVELOPMENT = ["MACHINE_LEARNING", "ML_MODEL_DEVELOPMENT"]   # optional
    ML_DATABASE = ["SQL", "POSTGRESQL"]
    ML_VERSION_CONTROL = ["GIT"]

    # ---------------------------------------------------------------
    # Cybersecurity Engineer (automaton A_SEC)
    # ---------------------------------------------------------------

    SEC_SCRIPTING = ["PYTHON", "BASH"]
    SEC_OPERATING_SYSTEM = ["LINUX"]
    SEC_NETWORKING = ["NETWORKING", "TCP_IP"]
    SEC_SECURITY = [
        "CYBERSECURITY",
        "NMAP",
        "VULNERABILITY_ASSESSMENT",
        "SECURITY_AUTOMATION",
    ]
    SEC_CONTAINERS = ["DOCKER", "KUBERNETES"]       # optional
    SEC_VERSION_CONTROL = ["GIT"]

    # ---------------------------------------------------------------
    # Data Engineer (automaton A_DE)
    # ---------------------------------------------------------------

    DE_LANGUAGE = ["PYTHON", "SQL"]
    DE_PROCESSING = ["SPARK"]
    DE_ORCHESTRATION = ["AIRFLOW"]                  # optional
    DE_DATA_INTEGRATION = ["ETL", "ELT", "DATA_PIPELINE"]
    DE_STORAGE = ["DATA_WAREHOUSING", "POSTGRESQL", "NOSQL"]
    DE_VERSION_CONTROL = ["GIT"]

    # ---------------------------------------------------------------
    # Groups of every profile, in order
    # ---------------------------------------------------------------

    GROUPS = {
        FULL_STACK_DEVELOPER: [
            FS_FRONTEND_LANGUAGE,
            FS_FRONTEND_FRAMEWORK,
            FS_BACKEND,
            FS_API,
            FS_DATABASE,
            FS_VERSION_CONTROL,
        ],
        MACHINE_LEARNING_ENGINEER: [
            ML_LANGUAGE,
            ML_DATA_LIBRARIES,
            ML_LIBRARIES,
            ML_DEVELOPMENT,
            ML_DATABASE,
            ML_VERSION_CONTROL,
        ],
        CYBERSECURITY_ENGINEER: [
            SEC_SCRIPTING,
            SEC_OPERATING_SYSTEM,
            SEC_NETWORKING,
            SEC_SECURITY,
            SEC_CONTAINERS,
            SEC_VERSION_CONTROL,
        ],
        DATA_ENGINEER: [
            DE_LANGUAGE,
            DE_PROCESSING,
            DE_ORCHESTRATION,
            DE_DATA_INTEGRATION,
            DE_STORAGE,
            DE_VERSION_CONTROL,
        ],
    }

    # Optional groups (the automaton has a transition that skips them).
    OPTIONAL = {
        FULL_STACK_DEVELOPER: [FS_API],
        MACHINE_LEARNING_ENGINEER: [ML_DEVELOPMENT],
        CYBERSECURITY_ENGINEER: [SEC_CONTAINERS],
        DATA_ENGINEER: [DE_ORCHESTRATION],
    }
