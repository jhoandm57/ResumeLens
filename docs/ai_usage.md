# Use of AI Tools

This document describes how the team used generative AI tools during the development of ResumeLens. AI was used as a collaborative assistant: it helped speed up repetitive implementation work, testing and technical writing, while the design of the system, the formal models and the final validation of every deliverable remained the responsibility of the team.

---

## 1. Tools Used

| Tool | Main use in the project |
| :--- | :--- |
| **Claude** (Anthropic) | Python scaffolding and refactoring, `pytest` test templates, review of Markdown documentation, repository cleanup |
| **ChatGPT** (OpenAI) | Explanations of `pyformlang` and `textX` APIs, debugging of syntax and runtime errors, wording suggestions |
| **Gemini** (Google) | Initial drafts of documentation sections and comparison of alternative formulations |

---

## 2. Collaboration Approach

The team worked with AI tools under a simple principle: **the team decides, the AI assists**. In practice, every interaction followed the same cycle:

1. **Design by the team.** The team first defined what had to be built: the stages of the pipeline, the canonical vocabulary, the qualification patterns of each profile, the automata and transducers, and the grammar of the DSL.
2. **Assisted drafting.** The AI was asked for a specific piece of work (a class skeleton, a group of test cases, a section of a document) based on that design.
3. **Human review and adjustment.** The team read, ran and corrected the output, adapting it to the design decisions and to the conventions of the repository.
4. **Verification.** Nothing was accepted until it was checked: code had to pass the test suite, formal definitions had to match the implementation, and references had to be verified against their original sources.

---

## 3. Where AI Assisted

### 3.1 Python implementation

- Boilerplate for classes and data containers (e.g., `ExtractedData`, `NormalizedData`) and for the command line interface of `src/pipeline.py`.
- Refactoring suggestions to reduce duplication, for example keeping a single definition of the qualification groups in `ProfileVocabulary`.
- Help with the syntax and API of `pyformlang` (construction of transducers and finite automata) and `textX` (grammar rules, error positions, model navigation).
- Debugging of exceptions and failing tests.

### 3.2 Tests

- Templates for `pytest` modules and parametrized test cases.
- Suggestions of edge cases (empty sections, unknown skill variants, special characters such as `<` and `&` in the HTML output, invalid DSL profiles).

### 3.3 Documentation

- Structure and formatting of the Markdown documents in `docs/`, including tables and LaTeX notation for the formal tuples.
- Proofreading and wording of technical explanations in English.

---

## 4. What the Team Led

The following decisions and tasks were made and carried out by the team. AI tools were consulted at most as a sounding board:

- **Architecture** of the four-stage pipeline and the data passed between stages.
- **Definition of the professional profiles**, including the two profiles chosen by the team (Cybersecurity Engineer and Data Engineer) and their qualification patterns.
- **Theoretical decisions**: alphabet of canonical tokens, design of each transducer, choice and construction of each automaton, and structure of the context-free grammar.
- **Formal definitions** (5-tuples, 7-tuples and EBNF) and their consistency with the code.
- **Example résumés and expected results** used for the demo and the end-to-end tests.
- **Final validation**: running the complete test suite, checking the console and HTML output of the pipeline, and reviewing every document before delivery.

---

## 5. Verification and Lessons Learned

AI output was treated as a draft, never as a final answer. The most relevant lesson came from the literature review: the first draft of `docs/02_literature_review.md` contained citation markers without a real source and several bibliographic references that could not be found in any database. During the review, the team checked each reference against its original publisher and replaced them with verified sources (Li et al., 2008; Mohri, 1997; Hopcroft et al., 2007; Romero, 2021; Dejanović et al., 2017).

This confirmed the rules the team followed for the rest of the project:

- Every reference must be verified in its original source before it is cited.
- Every piece of generated code must be understood by the team and covered by tests.
- Every formal definition must be checked against the implementation, not only against the text that describes it.

---

## 6. Responsibility

The team members are the authors of ResumeLens and take full responsibility for its content. All members are able to explain and justify the design, the formal models and the implementation presented in this repository.
