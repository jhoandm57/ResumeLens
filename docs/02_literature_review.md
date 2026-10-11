# Literature Review: Automated Resume Screening and Formal Language Models

## 1. Introduction and Problem Statement

In modern recruitment systems, processing large volumes of candidate résumés efficiently and objectively represents a significant engineering challenge. Résumés are semi-structured or unstructured documents containing heterogeneous representations of equivalent professional qualifications (e.g., `JS` vs. `JavaScript`, `Scikit-learn` vs. `sklearn`). The primary goal of an initial automated screening system is not to make hiring decisions, but to deterministically verify whether candidate qualifications satisfy predefined structural and skill requirements.

ResumeLens addresses this problem with a four-stage pipeline in which each stage is grounded in a different formal model: regular expressions, finite-state transducers, finite automata and context-free grammars. The following sections review the theoretical basis of each stage and the references that support it.

---

## 2. Stage 1: Resume Information Extraction via Regular Expressions

Information Extraction (IE) transforms unstructured text into structured data representations. In domain-specific text processing, regular expressions serve as a foundational mechanism for token identification and pattern extraction, because they describe exactly the class of regular languages and can be matched in time linear in the length of the input (Hopcroft et al., 2007).

**Li et al. (2008)** show that regular expressions are a central component of rule-based information extraction systems, and that their precision and recall depend heavily on how carefully the patterns are designed for the target domain. This matches the résumé setting, where applicants format contact details, experience durations and technology lists using varied syntactic conventions.

- **Role in ResumeLens**: Regular expressions enable deterministic extraction of targeted fields (e.g., emails, phone numbers, experience entries and skill mentions) from raw text before any formal transformation is applied.

---

## 3. Stage 2: Qualification Normalization using Finite-State Transducers (FST)

In natural language processing and domain-specific string processing, different surface forms often map to a single semantic entity. In candidate résumés, string variations like `Sklearn`, `scikit-learn` and `sklearn` refer to the same library (`SCIKIT_LEARN`).

A **Finite-State Transducer (FST)** is a finite-state machine with two tapes: an input tape and an output tape. Formally, a Mealy-style FST can be defined as a 7-tuple:

$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$

Where $Q$ is a finite set of states, $\Sigma$ is the input alphabet, $\Gamma$ is the output alphabet, $\delta$ is the transition function, $\omega$ is the output function, $q_0$ is the initial state, and $F$ is the set of accepting states.

**Mohri (1997)** presents finite-state transducers as an efficient and compact model for language and speech processing, showing that sequential (deterministic) transducers process an input in time linear in its length and can be composed and minimized. Unlike simple dictionary replacements, transducers model stateful string rewriting, making the mapping from surface forms to canonical forms explicit and verifiable.

- **Role in ResumeLens**: FSTs translate raw extracted tokens into standardized canonical skill representations and reorder them into canonical sequences (e.g., Frontend $\rightarrow$ Backend $\rightarrow$ Database $\rightarrow$ Version Control).

---

## 4. Stage 3: Qualification Pattern Recognition via Finite Automata

Once qualifications are normalized and sorted into canonical sequences, the system must evaluate whether the candidate satisfies the qualification pattern required by a professional profile.

A **Deterministic Finite Automaton (DFA)** or **Nondeterministic Finite Automaton (NFA)** recognizes regular languages, and both models are equivalent in expressive power through the subset construction. Formally, a DFA is defined as a 5-tuple:

$$M = (Q, \Sigma, \delta, q_0, F)$$

Where $Q$ is a finite set of states, $\Sigma$ is the alphabet of canonical qualification tokens, $\delta$ is the transition function, $q_0$ is the start state, and $F$ is the set of accepting states.

As described by **Hopcroft et al. (2007)**, a DFA decides membership of a string by reading each symbol exactly once, which gives recognition in $O(n)$ time and a deterministic, reproducible answer for every input. The automata in ResumeLens are built and executed with `pyformlang`, a Python library designed for the manipulation of regular expressions, finite automata, transducers and grammars (**Romero, 2021**).

- **Role in ResumeLens**: Distinct automata represent professional profiles (e.g., Full Stack Developer, Machine Learning Engineer). A résumé sequence is classified as `ACCEPTED` or `REJECTED` for a profile based on whether the automaton ends in an accepting state.

---

## 5. Stage 4: Candidate Profile Language via Context-Free Grammars and textX

Extracted data, normalized skills and classification decisions must be integrated into a structured candidate profile. While regular languages suffice for token extraction and sequence recognition, representing nested structures and repeated records (e.g., multiple employment histories or education records) is naturally expressed with a Context-Free Grammar (CFG).

A CFG is defined as a 4-tuple:

$$G = (V, \Sigma, R, S)$$

Where $V$ is a set of non-terminals, $\Sigma$ is a set of terminals, $R$ is a set of production rules, and $S$ is the start symbol.

**Dejanović et al. (2017)** present textX, a Python meta-language and tool for implementing domain-specific languages (DSLs). From a single grammar description, textX builds both the parser and the meta-model, so a valid input is turned directly into a graph of Python objects, while an invalid one produces a syntax error that reports its position.

- **Role in ResumeLens**: A custom DSL designed with textX validates the full candidate profile syntax, and the resulting model drives the HTML rendering of stage 4.

---

## 6. Summary of Conceptual Choices

| Pipeline Stage | Theoretical Model | Implementation Library | Key Reference | Primary Function |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Extraction** | Regular Expressions | Python `re` | Li et al. (2008) | Extract candidate contact info and raw skill mentions. |
| **Stage 2: Normalization** | Finite-State Transducers | `pyformlang` | Mohri (1997) | Transform text variants into canonical tokens. |
| **Stage 3: Recognition** | Finite Automata (DFA/NFA) | `pyformlang` | Hopcroft et al. (2007); Romero (2021) | Classify skill sequences against job profile criteria. |
| **Stage 4: DSL Grammar** | Context-Free Grammar | `textX` | Dejanović et al. (2017) | Validate structured candidate profiles. |

---

## References

Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž. (2017). TextX: A Python tool for Domain-Specific Languages implementation. *Knowledge-Based Systems*, *115*, 1–4. https://doi.org/10.1016/j.knosys.2016.10.023

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007). *Introduction to automata theory, languages, and computation* (3rd ed.). Pearson Addison-Wesley.

Li, Y., Krishnamurthy, R., Raghavan, S., Vaithyanathan, S., & Jagadish, H. V. (2008). Regular expression learning for information extraction. In *Proceedings of the 2008 Conference on Empirical Methods in Natural Language Processing* (pp. 21–30). Association for Computational Linguistics. https://aclanthology.org/D08-1003/

Mohri, M. (1997). Finite-state transducers in language and speech processing. *Computational Linguistics*, *23*(2), 269–311. https://aclanthology.org/J97-2003/

Romero, J. (2021). Pyformlang: An educational library for formal language manipulation. In *Proceedings of the 52nd ACM Technical Symposium on Computer Science Education (SIGCSE '21)* (pp. 576–582). ACM. https://doi.org/10.1145/3408877.3432464
