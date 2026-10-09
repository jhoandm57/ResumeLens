# ResumeLens – Problem Definition

## 1. Context

Recruitment processes in software companies usually receive a large number of resumes for each open position. In an initial screening phase, recruiters must review every document to verify whether the candidate meets the minimum technical qualifications required by the role, such as specific programming languages, frameworks, databases, tools, academic background, or years of experience.

This manual review is slow, repetitive, and prone to inconsistencies. Two recruiters may evaluate the same resume differently, and the same recruiter may apply different criteria depending on fatigue or the order in which resumes are reviewed.

Additionally, resumes are written as **unstructured or semi-structured text**. Each candidate decides how to organize the document and how to name their qualifications. As a consequence, the same qualification can appear under many different surface forms:

```text
JavaScript   Javascript   JS
React        React.js     ReactJS
Node.js      NodeJS
PostgreSQL   Postgres
TensorFlow   Tensor Flow
```

A naive keyword search fails in this scenario: it either misses valid qualifications written with a different variant, or it requires the recruiter to anticipate every possible way of writing each technology.

---

## 2. Problem Statement

Given a resume written in natural, unstructured text and a set of predefined professional profiles (Full Stack Developer, Machine Learning Engineer, Cybersecurity Engineer, and Data Engineer), the problem is to **automatically and deterministically determine whether the qualifications expressed in the resume satisfy the qualification pattern required by each profile**, and to produce a structured candidate profile that summarizes the result.

To solve this, ResumeLens must:

1. Identify and extract relevant information from free text, even when it appears with different formats, capitalizations, or spellings (**regular expressions**).
2. Transform the different variants of the same qualification into a single canonical representation (**finite-state transducers**).
3. Decide, with a formal and verifiable criterion, whether the normalized qualifications of the candidate belong to the language of accepted qualification patterns of a profile (**finite automata**).
4. Represent the extracted information, the normalized qualifications, and the classification decisions in a structured and syntactically validated format (**context-free grammar with textX**).

The system **does not make hiring decisions**. Its purpose is to support the initial technical screening by verifying, in a transparent and reproducible way, whether a candidate meets the minimum requirements defined for a profile.

---

## 3. Objectives

### 3.1 General Objective

Design and implement ResumeLens, a resume-screening system based on formal languages and automata, capable of extracting, normalizing, and classifying the technical qualifications of a candidate against predefined professional profiles in a deterministic and explainable way.

### 3.2 Specific Objectives

1. Design and implement regular expressions that extract contact information, technical skills, academic qualifications, and years of experience from unstructured resume text.
2. Design and implement finite-state transducers that normalize the extracted qualifications into canonical tokens.
3. Design and implement finite automata that recognize the accepted qualification patterns of each reference profile.
4. Design a context-free grammar, implemented with textX, that defines a language for structured candidate profiles.
5. Validate each stage with unit tests and the complete pipeline with integration tests based on representative resumes.

---

## 4. Scope

### 4.1 In Scope

- Resumes written in English and provided as plain text.
- The vocabulary of qualifications defined for the four reference profiles.
- Explicit experience expressions such as `3 years of experience` or `5+ yrs experience`.
- Variations in capitalization, spacing, and punctuation of known qualifications.
- Binary classification (`ACCEPTED` / `REJECTED`) per profile.

### 4.2 Out of Scope

- Reading PDF, DOCX, or image files (OCR).
- Resumes written in languages other than English.
- Inferring experience from date ranges (e.g., `2021 – 2024`) or job descriptions.
- Semantic understanding of the text or recognition of qualifications outside the defined vocabulary.
- Ranking candidates, scoring them, or making hiring decisions.
