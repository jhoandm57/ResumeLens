"""
Finite automata of the ResumeLens qualification-pattern recognition stage.

There is one deterministic finite automaton (DFA) per profile.
The input is the sorted sequence of canonical tokens produced by the
normalization stage (NormalizedData.profile_sequences), so every
symbol of the alphabet is a complete token, such as PYTHON or GIT.

All the automata follow the same idea (one state per group):

    q0 --group 1--> q1 --group 2--> q2 ... --group 6--> q6 (accepting)

- Reading a token of the next group moves to the next state.
- A loop on a state accepts more tokens of the same group
  (for example PANDAS and NUMPY).
- An optional group has an extra transition that skips its state.
- Any other token has no transition, so the sequence is rejected.

See docs/07_automata_design.md.
"""

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)

from src.model.normalization.normalized_data import NormalizedData

from .profile_vocabulary import (
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    CYBERSECURITY_ENGINEER,
    DATA_ENGINEER,
    ProfileVocabulary as V,
)


ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"

# Name of the automaton of each profile (used in the documentation).
AUTOMATON_NAMES = {
    FULL_STACK_DEVELOPER: "A_FS",
    MACHINE_LEARNING_ENGINEER: "A_ML",
    CYBERSECURITY_ENGINEER: "A_SEC",
    DATA_ENGINEER: "A_DE",
}


class ProfileAutomata:
    """
    Builds the four profile automata and classifies a résumé.
    """

    def __init__(self):
        # List of transitions (source, token, target) of each automaton.
        # It is used by the tests to check that every automaton is
        # deterministic and has the size documented in docs/07.
        self.transitions: dict[str, list[tuple[str, str, str]]] = {}

        self.automata = {
            FULL_STACK_DEVELOPER: self._build_full_stack(),
            MACHINE_LEARNING_ENGINEER: self._build_machine_learning(),
            CYBERSECURITY_ENGINEER: self._build_cybersecurity(),
            DATA_ENGINEER: self._build_data_engineer(),
        }

    # ---------------------------------------------------------------
    # Helper
    # ---------------------------------------------------------------

    def _add(self, profile, dfa, source, tokens, target):
        """
        Add one transition  source --token--> target  for each token.
        """

        for token in tokens:
            dfa.add_transition(source, Symbol(token), target)
            self.transitions.setdefault(profile, []).append(
                (source.value, token, target.value)
            )

    # ---------------------------------------------------------------
    # A_FS — Full Stack Developer
    # ---------------------------------------------------------------

    def _build_full_stack(self):
        p = FULL_STACK_DEVELOPER
        dfa = DeterministicFiniteAutomaton()

        # States
        q0 = State("q0")
        q1 = State("q1")    # frontend language read
        q2 = State("q2")    # frontend framework read
        q3 = State("q3")    # backend read
        q4 = State("q4")    # REST API read
        q5 = State("q5")    # database read
        q6 = State("q6")    # version control read

        dfa.add_start_state(q0)
        dfa.add_final_state(q6)

        # 1. Frontend language: JAVASCRIPT | TYPESCRIPT
        self._add(p, dfa, q0, V.FS_FRONTEND_LANGUAGE, q1)
        self._add(p, dfa, q1, V.FS_FRONTEND_LANGUAGE, q1)     # loop

        # 2. Frontend framework: REACT | ANGULAR | VUE
        self._add(p, dfa, q1, V.FS_FRONTEND_FRAMEWORK, q2)
        self._add(p, dfa, q2, V.FS_FRONTEND_FRAMEWORK, q2)    # loop

        # 3. Backend: NODE_JS | DJANGO | SPRING_BOOT
        self._add(p, dfa, q2, V.FS_BACKEND, q3)
        self._add(p, dfa, q3, V.FS_BACKEND, q3)               # loop

        # 4. API (optional): REST_API
        self._add(p, dfa, q3, V.FS_API, q4)

        # 5. Database: SQL | POSTGRESQL | NOSQL
        self._add(p, dfa, q4, V.FS_DATABASE, q5)
        self._add(p, dfa, q3, V.FS_DATABASE, q5)              # skips the API
        self._add(p, dfa, q5, V.FS_DATABASE, q5)              # loop

        # 6. Version control: GIT
        self._add(p, dfa, q5, V.FS_VERSION_CONTROL, q6)

        return dfa

    # ---------------------------------------------------------------
    # A_ML — Machine Learning Engineer
    # ---------------------------------------------------------------

    def _build_machine_learning(self):
        p = MACHINE_LEARNING_ENGINEER
        dfa = DeterministicFiniteAutomaton()

        q0 = State("q0")
        q1 = State("q1")    # language read
        q2 = State("q2")    # data library read
        q3 = State("q3")    # ML library read
        q4 = State("q4")    # ML development read
        q5 = State("q5")    # database read
        q6 = State("q6")    # version control read

        dfa.add_start_state(q0)
        dfa.add_final_state(q6)

        # 1. Language: PYTHON
        self._add(p, dfa, q0, V.ML_LANGUAGE, q1)

        # 2. Data libraries: PANDAS | NUMPY
        self._add(p, dfa, q1, V.ML_DATA_LIBRARIES, q2)
        self._add(p, dfa, q2, V.ML_DATA_LIBRARIES, q2)        # loop

        # 3. ML libraries: SCIKIT_LEARN | TENSORFLOW | PYTORCH
        self._add(p, dfa, q2, V.ML_LIBRARIES, q3)
        self._add(p, dfa, q3, V.ML_LIBRARIES, q3)             # loop

        # 4. ML development (optional): MACHINE_LEARNING | ML_MODEL_DEVELOPMENT
        self._add(p, dfa, q3, V.ML_DEVELOPMENT, q4)
        self._add(p, dfa, q4, V.ML_DEVELOPMENT, q4)           # loop

        # 5. Database: SQL | POSTGRESQL
        self._add(p, dfa, q4, V.ML_DATABASE, q5)
        self._add(p, dfa, q3, V.ML_DATABASE, q5)              # skips ML development
        self._add(p, dfa, q5, V.ML_DATABASE, q5)              # loop

        # 6. Version control: GIT
        self._add(p, dfa, q5, V.ML_VERSION_CONTROL, q6)

        return dfa

    # ---------------------------------------------------------------
    # A_SEC — Cybersecurity Engineer
    # ---------------------------------------------------------------

    def _build_cybersecurity(self):
        p = CYBERSECURITY_ENGINEER
        dfa = DeterministicFiniteAutomaton()

        q0 = State("q0")
        q1 = State("q1")    # scripting language read
        q2 = State("q2")    # operating system read
        q3 = State("q3")    # networking read
        q4 = State("q4")    # security read
        q5 = State("q5")    # containers read
        q6 = State("q6")    # version control read

        dfa.add_start_state(q0)
        dfa.add_final_state(q6)

        # 1. Scripting: PYTHON | BASH
        self._add(p, dfa, q0, V.SEC_SCRIPTING, q1)
        self._add(p, dfa, q1, V.SEC_SCRIPTING, q1)            # loop

        # 2. Operating system: LINUX
        self._add(p, dfa, q1, V.SEC_OPERATING_SYSTEM, q2)

        # 3. Networking: NETWORKING | TCP_IP
        self._add(p, dfa, q2, V.SEC_NETWORKING, q3)
        self._add(p, dfa, q3, V.SEC_NETWORKING, q3)           # loop

        # 4. Security: CYBERSECURITY | NMAP | VULNERABILITY_ASSESSMENT | SECURITY_AUTOMATION
        self._add(p, dfa, q3, V.SEC_SECURITY, q4)
        self._add(p, dfa, q4, V.SEC_SECURITY, q4)             # loop

        # 5. Containers (optional): DOCKER | KUBERNETES
        self._add(p, dfa, q4, V.SEC_CONTAINERS, q5)
        self._add(p, dfa, q5, V.SEC_CONTAINERS, q5)           # loop

        # 6. Version control: GIT
        self._add(p, dfa, q5, V.SEC_VERSION_CONTROL, q6)
        self._add(p, dfa, q4, V.SEC_VERSION_CONTROL, q6)      # skips containers

        return dfa

    # ---------------------------------------------------------------
    # A_DE — Data Engineer
    # ---------------------------------------------------------------

    def _build_data_engineer(self):
        p = DATA_ENGINEER
        dfa = DeterministicFiniteAutomaton()

        q0 = State("q0")
        q1 = State("q1")    # language read
        q2 = State("q2")    # processing read
        q3 = State("q3")    # orchestration read
        q4 = State("q4")    # data integration read
        q5 = State("q5")    # storage read
        q6 = State("q6")    # version control read

        dfa.add_start_state(q0)
        dfa.add_final_state(q6)

        # 1. Language: PYTHON | SQL
        self._add(p, dfa, q0, V.DE_LANGUAGE, q1)
        self._add(p, dfa, q1, V.DE_LANGUAGE, q1)              # loop

        # 2. Processing: SPARK
        self._add(p, dfa, q1, V.DE_PROCESSING, q2)

        # 3. Orchestration (optional): AIRFLOW
        self._add(p, dfa, q2, V.DE_ORCHESTRATION, q3)

        # 4. Data integration: ETL | ELT | DATA_PIPELINE
        self._add(p, dfa, q3, V.DE_DATA_INTEGRATION, q4)
        self._add(p, dfa, q2, V.DE_DATA_INTEGRATION, q4)      # skips orchestration
        self._add(p, dfa, q4, V.DE_DATA_INTEGRATION, q4)      # loop

        # 5. Storage: DATA_WAREHOUSING | POSTGRESQL | NOSQL
        self._add(p, dfa, q4, V.DE_STORAGE, q5)
        self._add(p, dfa, q5, V.DE_STORAGE, q5)               # loop

        # 6. Version control: GIT
        self._add(p, dfa, q5, V.DE_VERSION_CONTROL, q6)

        return dfa

    # ---------------------------------------------------------------
    # Recognition
    # ---------------------------------------------------------------

    def accepts(self, profile: str, sequence: list[str]) -> bool:
        """
        Run the automaton of a profile on a sorted token sequence.
        """

        return self.automata[profile].accepts([Symbol(token) for token in sequence])

    def classify(self, normalized: NormalizedData) -> dict[str, str]:
        """
        Classify a résumé with the four automata.

        This is the main entry point of the classification stage.

        Args:
            normalized: Result of the normalization stage. Each automaton
                        reads the sequence of its profile from
                        normalized.profile_sequences (already sorted).

        Returns:
            Dictionary profile -> ACCEPTED or REJECTED.
        """

        return {
            profile: (
                ACCEPTED
                if self.accepts(profile, normalized.profile_sequences.get(profile, []))
                else REJECTED
            )
            for profile in self.automata
        }
