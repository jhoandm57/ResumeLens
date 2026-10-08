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