# ResumeLens – Test Design

This document describes how ResumeLens is tested: the testing strategy, the test cases of each stage, and the end-to-end scenarios that go from a résumé to its HTML visualization.

All the tests are automated with **pytest** and are in the `tests/` folder.

---

## 1. Testing Strategy

The tests follow the same division as the system (see [`03_system_design.md`](03_system_design.md)):

| Level | What is tested | Folder |
| :--- | :--- | :--- |
| **Unit tests by stage** | Each formal model alone, with inputs built by hand: the regular expressions, the transducers, the automata, the grammar, the generator, and the visualizer. | `tests/extraction`, `tests/normalization`, `tests/classification`, `tests/grammar` |
| **End-to-end tests** | The complete pipeline on real résumé files, from the `.txt` to the `.html`, compared with an expected result. | `tests/test_end_to_end.py` |

For every stage, the test cases cover three kinds of inputs:

- **Valid cases**: the examples of the statement (Wednesday Addams and Mary Jane Watson) and the examples of the two profiles defined by the team.
- **Variants**: different ways of writing the same information (`JS` / `JavaScript`, `Tensor Flow` / `TensorFlow`, different orders, upper and lower case).
- **Invalid or limit cases**: empty inputs, unknown values, missing mandatory groups, and texts that violate the grammar.

Some tests also check that the code matches the formal design documents: the number of states of each transducer (`06_fst_design.md`), and the number of states and transitions of each automaton (`07_automata_design.md`). If the implementation changes, these tests fail until the documentation is updated too.

### 1.1 Size of the Test Suite

| Stage | File | Test functions | Test cases collected by pytest |
| :--- | :--- | ---: | ---: |
| 1. Extraction | `tests/extraction/test_regex_patterns.py` | 23 | 23 |
| 1. Extraction | `tests/extraction/test_resume_extraction.py` | 6 | 6 |
| 2. Normalization | `tests/normalization/test_normalization_transducers.py` | 12 | 12 |
| 2. Normalization | `tests/normalization/test_resume_normalizer.py` | 22 | 22 |
| 3. Classification | `tests/classification/test_profile_automata.py` | 15 | 15 |
| 4. Grammar | `tests/grammar/test_profile_generator.py` | 8 | 8 |
| 4. Grammar | `tests/grammar/test_profile_validator.py` | 14 | 14 |
| 4. Grammar | `tests/grammar/test_profile_visualizer.py` | 9 | 9 |
| End-to-end | `tests/test_end_to_end.py` | 5 | 20 |
| **Total** | | **114** | **129** |

The unit tests are not parametrized, so each function is one test case (109 in total). In the end-to-end file, three tests are parametrized with the six example résumés: `2 + 3 × 6 = 20` test cases.

---

## 2. Stage 1 – Extraction (regular expressions)

Files: `tests/extraction/test_regex_patterns.py`, `tests/extraction/test_resume_extraction.py`

| Test case | Input | Expected result |
| :--- | :--- | :--- |
| Each category pattern | Texts with emails, phones, languages, frameworks, databases, academic titles, experience, tools, other qualifications | Every expected string is found |
| Variants of the same qualification | `JS`, `React.js`, `NodeJS`, `Scikit-learn`, `sklearn`, `TCP/IP`, `Linux` | Extracted as written |
| `JS` inside file names | `app.js`, `node.js` | `JS` is not extracted as a language |
| Phone formats | `+57 300 1234567`, `300 123 4567`, `+57-300-1234567`, `(300) 123-4567` | Recognized; years and IDs are ignored |
| Experience expressions | `3 years of experience`, `5+ yrs experience`, `2 years professional experience` | Recognized; partial numbers are ignored |
| Words containing degrees | `Webmaster and Headmaster` | Not extracted as academic titles |
| Candidate name | Name in the first line, with accents, particles (`de`, `van`), capitals, or with a `Name:` label | Name extracted; headings and job titles are rejected |
| Name label and header | Résumé with a `Name:` label and a different first line | The label has priority over the header |
| Name not found | Résumé without a recognizable name | `name = None` |
| Complete résumé | Text with every category | `ExtractedData` with every list filled |
| Empty résumé | `""` | Empty lists and `name = None` |

---

## 3. Stage 2 – Normalization (finite-state transducers)

Files: `tests/normalization/test_normalization_transducers.py`, `tests/normalization/test_resume_normalizer.py`

| Test case | Input | Expected result |
| :--- | :--- | :--- |
| Preprocessing | `"  Tensor   Flow "` | `"tensor flow"` |
| Each transducer (`M_LANG`, `M_FW`, `M_DB`, `M_TOOLS`, `M_OTHER`, `M_ACAD`) | Every variant of its vocabulary | Its canonical token (`JS → JAVASCRIPT`, `Postgres → POSTGRESQL`) |
| `M_EXP` | `5+ yrs of experience` | `5` (only the number is copied) |
| `M_EXP` without a number | `years of experience` | No output (`None`) |
| Rejected inputs | Unknown strings | No output (`None`), ignored by the normalizer |
| Size of the transducers | – | Number of states documented in `06_fst_design.md`, Section 6.8 (`M_LANG` 36, `M_FW` 140, `M_DB` 20, `M_TOOLS` 89, `M_OTHER` 137, `M_ACAD` 107, `M_EXP` 4) |
| Statement examples | Wednesday Addams, Mary Jane Watson | The canonical tokens of the statement |
| Cybersecurity example | Skills of the Cybersecurity profile, including `Linux` | Canonical tokens, with `LINUX` in its group of the cybersecurity order |
| Coverage of stage 1 | Every value extracted by stage 1 in the example résumés | Every value is normalized to a canonical token |
| Data kept without changes | Name, email and phone | Copied from `ExtractedData` as they are |
| Duplicates and `SQL` | `SQL` as language and database, repeated tools | Each token appears once |
| Experience | Several experience expressions | `experience_years` = maximum; entries kept as written |
| Canonical order of each profile | `Git, NodeJS, JS, Postgres, React.js` | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` (Full Stack order) |
| Order does not depend on the résumé | Same skills in different orders | Same sorted sequence |
| Tokens of other profiles | `PANDAS` in the Full Stack sequence | Discarded from that sequence |

---

## 4. Stage 3 – Classification (finite automata)

File: `tests/classification/test_profile_automata.py`

| Test case | Input sequence | Expected result |
| :--- | :--- | :--- |
| Full Stack example of the statement | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` | `A_FS`: ACCEPTED |
| Machine Learning example of the statement | `PYTHON, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, SQL, GIT` | `A_ML`: ACCEPTED |
| Example of the guide | `PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT` | `A_ML`: ACCEPTED |
| Cybersecurity and Data Engineer examples | `Python, Linux, TCP/IP, Docker, Nmap, Git.` and `Python, SQL, Spark, Airflow, PostgreSQL, ETL, Git.` | `A_SEC` and `A_DE`: ACCEPTED |
| Order of the résumé | Same skills written in different orders | Same result, because stage 2 sorts the sequence first |
| Several tokens of the same group | `PANDAS, NUMPY` | ACCEPTED (loop) |
| Optional groups present or missing | With and without `REST_API`, `MACHINE_LEARNING`, `DOCKER`, `AIRFLOW` | ACCEPTED in both cases |
| Missing mandatory group | Full Stack without backend | REJECTED |
| Unsorted or foreign tokens | `GIT, PYTHON, PANDAS, ...` or `REACT` inside the ML sequence | REJECTED |
| Empty sequence | `[]` | REJECTED in the four automata |
| Four profiles always | Any résumé | `classify` returns the four profiles |
| Determinism | – | No automaton has two transitions with the same state and token |
| Size | – | Every automaton has 7 states; transitions as documented in `07_automata_design.md` (`A_FS` 27, `A_ML` 22, `A_SEC` 23, `A_DE` 22) |
| Stage 2 compatibility | Every token of `ProfileVocabulary` | Can be produced by stage 2, and the sequence of stage 2 follows the groups of each automaton |

---

## 5. Stage 4 – Candidate Profile (textX)

Files: `tests/grammar/test_profile_generator.py`, `tests/grammar/test_profile_validator.py`, `tests/grammar/test_profile_visualizer.py`

The complete table of test cases of this stage is in [`08_grammar_design.md`](08_grammar_design.md), Section 10. In summary:

| Component | Test cases |
| :--- | :--- |
| `ProfileGenerator` | The statement example is generated exactly; generated profiles satisfy the grammar; several experiences; empty blocks are omitted; unknown name; phone across lines; the four profiles in order |
| `ProfileValidator` | Valid example files; access to every block of the model; minimal profile; comments; **lexical**, **syntactic**, and **semantic** errors with line and column |
| `ProfileVisualizer` | Complete HTML; name, contact, experience, education, tokens by category; the four results with the accepted ones highlighted; missing blocks shown as *Not reported*; escaping of `<`, `>`, and `&` |

---

## 6. End-to-End Scenarios

File: `tests/test_end_to_end.py`

Each résumé of `data/resumes/` is a **scenario**. The test runs the complete pipeline (`ResumePipeline.process_file`) and compares the result with the expected result stored in `data/expected/<name>.json`:

```json
{
  "resume": "wednesday_addams.txt",
  "name": "Wednesday Addams",
  "profiles": {
    "FULL_STACK_DEVELOPER": {
      "sequence": ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
      "result": "ACCEPTED"
    },
    "MACHINE_LEARNING_ENGINEER": {
      "sequence": ["POSTGRESQL", "GIT"],
      "result": "REJECTED"
    }
  }
}
```

(The real files contain the four profiles.)

### 6.1 Scenarios

| Scenario | Résumé | Purpose | Accepted profiles |
| :--- | :--- | :--- | :--- |
| S1 | `wednesday_addams.txt` | Full Stack example of the statement | FULL_STACK_DEVELOPER |
| S2 | `mary_jane_watson.txt` | Machine Learning example of the statement | MACHINE_LEARNING_ENGINEER |
| S3 | `peter_parker.txt` | Profile defined by the team (software engineering) | CYBERSECURITY_ENGINEER |
| S4 | `clark_kent.txt` | Profile defined by the team (AI / data) | DATA_ENGINEER |
| S5 | `tony_stark.txt` | One résumé that satisfies **two** profiles | MACHINE_LEARNING_ENGINEER, DATA_ENGINEER |
| S6 | `bruce_wayne.txt` | Frontend, database, and Git, but **no backend**: the Full Stack automaton stops in `q2` | none |

### 6.2 Sequences of each scenario

The sequence is the input of each automaton (output of stage 2, already sorted by profile):

| Scenario | Profile | Sequence | Result |
| :--- | :--- | :--- | :--- |
| S1 | Full Stack | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` | ACCEPTED |
| S2 | Machine Learning | `PYTHON, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, SQL, GIT` | ACCEPTED |
| S3 | Cybersecurity | `PYTHON, BASH, LINUX, NETWORKING, TCP_IP, CYBERSECURITY, NMAP, VULNERABILITY_ASSESSMENT, SECURITY_AUTOMATION, DOCKER, GIT` | ACCEPTED |
| S4 | Data Engineer | `PYTHON, SQL, SPARK, AIRFLOW, ETL, DATA_PIPELINE, DATA_WAREHOUSING, POSTGRESQL, GIT` | ACCEPTED |
| S5 | Machine Learning | `PYTHON, PANDAS, NUMPY, TENSORFLOW, PYTORCH, MACHINE_LEARNING, SQL, POSTGRESQL, GIT` | ACCEPTED |
| S5 | Data Engineer | `PYTHON, SQL, SPARK, ETL, POSTGRESQL, GIT` | ACCEPTED |
| S6 | Full Stack | `TYPESCRIPT, ANGULAR, VUE, POSTGRESQL, GIT` | REJECTED |

### 6.3 What is checked in every scenario

| Test | Cases | Checks |
| :--- | ---: | :--- |
| `test_there_are_example_resumes` | 1 | `data/resumes/` has at least four résumés (one per profile) |
| `test_every_resume_has_an_expected_result_and_vice_versa` | 1 | Every `.txt` has its `.json` and every `.json` has its `.txt` |
| `test_resume_classification_matches_expected` | 6 | Stage 1: extracted name · Stage 2: sequence of each profile · Stage 3: ACCEPTED / REJECTED of each profile |
| `test_generated_profile_is_valid_and_visualized` | 6 | Stage 4: the generated profile satisfies the grammar, the `.rl` is written, and the HTML contains the name and every profile with its result |
| `test_scenarios` | 6 | Summary: the list of accepted profiles of each résumé |

---

## 7. Running the Tests

From the root of the project:

```bash
python -m pytest                              # all the tests
python -m pytest tests/extraction             # one stage
python -m pytest tests/test_end_to_end.py -v  # end-to-end scenarios
```

The complete run collects the 129 test cases of Section 1.1.

The end-to-end tests write their `.rl` and `.html` files in a temporary folder, so they do not modify `data/output/`.
