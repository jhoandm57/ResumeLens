# Literature Review: Automated Resume Screening and Formal Language Models

## 1. Introduction and Problem Statement

In modern recruitment systems, processing large volumes of candidate résumés efficiently and objectively represents a significant engineering challenge[cite: 1]. Résumés are semi-structured or unstructured documents containing heterogeneous representations of equivalent professional qualifications (e.g., `JS` vs. `JavaScript`, `Scikit-learn` vs. `sklearn`)[cite: 1]. The primary goal of an initial automated screening system is not to make hiring decisions, but to deterministically verify whether candidate qualifications satisfy predefined structural and skill requirements[cite: 1].

---

## 2. Stage 1: Resume Information Extraction via Regular Expressions

Information Extraction (IE) transforms unstructured text into structured data representations[cite: 1]. In domain-specific text processing, Regular Expressions (Regex) serve as the foundational mechanism for token identification and pattern extraction[cite: 1].

According to recent benchmark studies by **Li et al. (2020)**, regular expressions remain the most efficient mechanism for deterministic rule-based information extraction in domain-specific text processing. In candidate résumés, applicants format contact details, experience durations, and technology lists using varied syntactic conventions[cite: 1].

- **Role in ResumeLens**: Regular expressions enable deterministic, ultra-low-latency extraction of targeted fields (e.g., emails, phone numbers, skill mentions) from raw text before formal transformations are applied[cite: 1].