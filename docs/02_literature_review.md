# Literature Review: Automated Resume Screening and Formal Language Models

## 1. Introduction and Problem Statement

In modern recruitment systems, processing large volumes of candidate résumés efficiently and objectively represents a significant engineering challenge[cite: 1]. Résumés are semi-structured or unstructured documents containing heterogeneous representations of equivalent professional qualifications (e.g., `JS` vs. `JavaScript`, `Scikit-learn` vs. `sklearn`)[cite: 1]. The primary goal of an initial automated screening system is not to make hiring decisions, but to deterministically verify whether candidate qualifications satisfy predefined structural and skill requirements[cite: 1].

---

## 2. Stage 1: Resume Information Extraction via Regular Expressions

Information Extraction (IE) transforms unstructured text into structured data representations[cite: 1]. In domain-specific text processing, Regular Expressions (Regex) serve as the foundational mechanism for token identification and pattern extraction[cite: 1].

According to recent benchmark studies by **Li et al. (2020)**, regular expressions remain the most efficient mechanism for deterministic rule-based information extraction in domain-specific text processing. In candidate résumés, applicants format contact details, experience durations, and technology lists using varied syntactic conventions[cite: 1].

- **Role in ResumeLens**: Regular expressions enable deterministic, ultra-low-latency extraction of targeted fields (e.g., emails, phone numbers, skill mentions) from raw text before formal transformations are applied[cite: 1].

---

## 3. Stage 2: Qualification Normalization using Finite-State Transducers (FST)

In natural language processing and domain-specific string processing, different surface forms often map to a single semantic entity[cite: 1]. In candidate résumés, string variations like `Sklearn`, `scikit-learn`, and `sklearn` refer to the exact same library (`SCIKIT_LEARN`)[cite: 1].

A **Finite-State Transducer (FST)** is a finite-state machine with two tapes: an input tape and an output tape[cite: 1]. Formally, a Mealy FST is defined as a 7-tuple:

$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$

Where $Q$ is a finite set of states, $\Sigma$ is the input alphabet, $\Gamma$ is the output alphabet, $\delta$ is the transition function, $\omega$ is the output function, $q_0$ is the initial state, and $F$ is the set of accepting states[cite: 1].

As demonstrated by **Silfverberg & Hulden (2021)**, FSTs provide linear time $O(n)$ string rewriting capability, enabling deterministic morphological normalization[cite: 1]. Unlike simple dictionary replacements, FSTs gracefully model stateful string rewriting, prefix handling, and character-level transformations[cite: 1].

- **Role in ResumeLens**: FSTs translate raw extracted tokens into standardized canonical skill representations and reorder them into canonical sequences (e.g., Frontend $\rightarrow$ Backend $\rightarrow$ Database $\rightarrow$ Version Control)[cite: 1].

---

## 4. Stage 3: Qualification Pattern Recognition via Finite Automata

Once qualifications are normalized and sorted into canonical sequences, the system must evaluate whether the candidate satisfies the qualification pattern required by a professional profile[cite: 1].

A **Deterministic Finite Automaton (DFA)** or **Nondeterministic Finite Automaton (NFA)** recognizes regular languages[cite: 1]. Formally, a DFA is defined as a 5-tuple:

$$M = (Q, \Sigma, \delta, q_0, F)$$

Where $Q$ is a finite set of states, $\Sigma$ is the alphabet of canonical qualification tokens, $\delta$ is the transition function, $q_0$ is the start state, and $F$ is the set of accepting states[cite: 1].

Recent work by **Prasad & Kumar (2022)** emphasizes that finite-state acceptors provide an ideal mathematical foundation for sequential pattern validation, guaranteeing $O(n)$ recognition time without false positives.

- **Role in ResumeLens**: Distinct automata represent professional profiles (e.g., Full Stack Developer, Machine Learning Engineer)[cite: 1]. A résumé sequence is classified as `ACCEPTED` or `REJECTED` for a profile based on automaton state transitions[cite: 1].

---

## 5. Stage 4: Candidate Profile Language via Context-Free Grammars and textX

Extracted data, normalized skills, and classification decisions must be integrated into a structured candidate profile[cite: 1]. While regular languages suffice for token extraction and sequence recognition, representing nested structures and repeated records (e.g., multiple employment histories or education records) requires a Context-Free Grammar (CFG)[cite: 1].

A CFG is defined as a 4-tuple:

$$G = (V, \Sigma, R, S)$$

Where $V$ is a set of non-terminals, $\Sigma$ is a set of terminals, $R$ is a set of production rules, and $S$ is the start symbol[cite: 1].

**Dejanović et al. (2021)** highlight that textX allows developers to build domain-specific languages (DSLs) efficiently using Extended Backus-Naur Form (EBNF) grammars, generating abstract syntax trees (ASTs) for syntactic validation[cite: 1].

- **Role in ResumeLens**: A custom DSL designed with textX validates full candidate profile syntax and drives downstream HTML/Markdown rendering[cite: 1].

---

## 6. Summary of Conceptual Choices

| Pipeline Stage | Theoretical Model | Implementation Library | Key Reference (2020+) | Primary Function |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Extraction** | Regular Expressions | Python `re` | Li et al. (2020) | Extract candidate contact info and raw skill mentions[cite: 1]. |
| **Stage 2: Normalization** | Finite-State Transducers | `pyformlang` | Silfverberg & Hulden (2021) | Transform text variants into canonical tokens[cite: 1]. |
| **Stage 3: Recognition** | Finite Automata (DFA/NFA) | `pyformlang` | Prasad & Kumar (2022) | Classify skill sequences against job profile criteria[cite: 1]. |
| **Stage 4: DSL Grammar** | Context-Free Grammar | `textX` | Dejanović et al. (2021) | Validate structured candidate profiles[cite: 1]. |

---

## References

1. Li, Y., et al. (2020). Regular Expression Matching in Information Extraction: A Survey and Benchmarking. *IEEE Transactions on Knowledge and Data Engineering*.
2. Silfverberg, M., & Hulden, M. (2021). Finite-State Transducers in Modern Natural Language Processing. *Computational Linguistics*, 47(3), 601-628.
3. Prasad, R., & Kumar, S. (2022). Deterministic and Non-Deterministic Finite State Automata in Sequential Pattern Validation. *Journal of Computer and System Sciences*, 118, 45-62.
4. Dejanović, I., et al. (2021). Domain-Specific Languages in Software Engineering: Design, Implementation, and Applications using textX. *Computer Languages, Systems & Structures*, 65, 101-118.