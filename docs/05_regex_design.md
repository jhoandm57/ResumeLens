# ResumeLens – Stage 1: Information Extraction with Regular Expressions

## 1. Purpose of the Stage

ResumeLens receives a résumé as unstructured text and uses regular expressions (Python's `re` module) to find the information that later stages need: the candidate name, contact information, programming languages, frameworks and libraries, databases, academic qualifications, professional experience, tools and technologies, and other qualifications relevant to the four profiles.

This stage only **recognizes and extracts**. It does not decide whether two expressions are equivalent (that is the job of the transducers in `06_fst_design.md`), and it does not classify the candidate (that is the job of the automata in `07_automata_design.md`). Every value is kept **exactly as it appears** in the résumé:

```text
Input:   Technical Skills: JS, React.js, NodeJS, Postgres, Git.
Output:  JS | React.js | NodeJS | Postgres | Git        -> input of Stage 2
```

### 1.1 Requirements of the Statement

| Requirement | Where |
| :--- | :--- |
| Define the regular expression of each type of information | Section 3 and `src/model/extraction/regex_patterns.py` |
| Explain the language or textual pattern recognized | Section 3, paragraph **Language recognized** of each category |
| Implement the expressions with Python's `re` module | `src/model/extraction/resume_extractor.py` (Section 4) |
| Keep the extracted information in a file or data structure | `ExtractedData` dataclass in `src/model/extraction/extracted_data.py` (Section 4) |

**Notation.** `L(R)` is the language recognized by `R`; `·` is concatenation, `∪` / `|` union, `*` zero or more, `+` one or more, `?` optional. `W` denotes one or more whitespace characters and `W?` zero or more. `D` is the set of digits.

---

## 2. Design Decisions

- **One expression per category.** Each type of information has its own pattern instead of one large expression for the whole résumé. This keeps each pattern small, testable, and easy to extend.
- **Case-insensitive matching.** All patterns are applied with `re.IGNORECASE`, so `Python`, `python`, and `PYTHON` are recognized by the same expression. The only exception is the **candidate name**, because capital letters are what identify a proper name.
- **Original forms are preserved.** `Postgres` is extracted as `Postgres`, not as `POSTGRESQL`. Mixing extraction and normalization would break the separation between the formal models of the pipeline.
- **Longest alternative first.** The regex engine tries alternatives from left to right, so more specific forms are written first (`PostgreSQL` before `Postgres`, `NoSQL` before `SQL`, `Machine Learning Model Development` before `Machine Learning`).
- **Word boundaries and lookarounds.** `\b`, `(?<!...)`, and `(?!...)` prevent matches inside other words or numbers (`master` in `Webmaster`, `JS` in `React.js`, `5` in `1.5 years`).
- **Controlled vocabulary.** The qualification patterns recognize the vocabulary of the four supported profiles (`04_profiles.md`). The same vocabulary is used by the transducers of Stage 2.

---

## 3. Regular Expressions

### 3.1 Candidate Name

The name does not belong to a vocabulary, so it is recognized by its **form** (2 to 4 capitalized words) and its **position** (first non-empty line, or after a `Name:` label).

```python
_UPPER = r"A-ZÀ-ÖØ-Þ"        # upper-case letters, including accented ones
_LOWER = r"a-zß-öø-ÿ"        # lower-case letters, including accented ones

_NAME_WORD = (
    rf"(?:(?:[{_UPPER}]['’])?[{_UPPER}][{_LOWER}]+(?:[-'’]?[{_UPPER}]?[{_LOWER}]+)*"
    rf"|[{_UPPER}]{{2,}}(?:[-'’][{_UPPER}]{{2,}})*)"
)
_NAME_PARTICLE = r"(?:de|del|la|las|los|da|das|do|dos|di|du|van|von|der|y)"
_FULL_NAME = rf"{_NAME_WORD}(?:[ \t]+(?:{_NAME_PARTICLE}[ \t]+)*{_NAME_WORD}){{1,3}}"

_NOT_A_NAME = (
    r"(?!(?i:curriculum|resume|résumé|cv|technical|skills|experience"
    r"|professional|education|contact|profile|summary|objective)\b)"
    r"(?![^\n]*\b(?i:developer|engineer|scientist|analyst|architect"
    r"|manager|designer|programmer|consultant|intern)\b)"
)

NAME_LABEL_PATTERN  = rf"^[ \t]*(?i:(?:full[ \t]+)?name)[ \t]*:[ \t]*({_FULL_NAME})[ \t]*$"
NAME_HEADER_PATTERN = rf"\A\s*{_NOT_A_NAME}({_FULL_NAME})[ \t]*$"
```

**Key components**

- `_NAME_WORD`: a capitalized word (`Wednesday`, `McDonald`, `O'Connor`, `Jean-Luc`) or a word in capitals (`PARKER`).
- `_FULL_NAME`: one word followed by 1 to 3 more (`{1,3}`), with optional particles (`Juan de la Cruz`). It uses `[ \t]` instead of `\s`, so a name cannot continue on the next line.
- `NAME_LABEL_PATTERN`: a complete line `Name: ...` (with `re.MULTILINE`). The inline flag `(?i:...)` makes only the label case-insensitive.
- `NAME_HEADER_PATTERN`: `\A\s*` anchors it to the first non-empty line of the text. `_NOT_A_NAME` rejects section headings (`Technical Skills`) and job titles (`Python Developer`).

`extract_name` tries the label first and the header after it, and collapses repeated spaces.

**Language recognized.** Let `U` be the upper-case letters, `l` the lower-case letters, `S = {space, tab}`, and `P` the particles:

```text
L(_NAME_WORD) = ( (U·{', ’})? · U · l+ · ({-, ', ’}? · U? · l+)* )  ∪  ( U·U+ · ({-, ', ’} · U·U+)* )
L(_FULL_NAME) = L(_NAME_WORD) · ( S+ · (P·S+)* · L(_NAME_WORD) ){1,3}
```

| Input (first line) | Result |
| :--- | :--- |
| `Wednesday Addams` / `Mary Jane Watson` / `CLARK KENT` | extracted |
| `Name: Peter Parker` (any line) | `Peter Parker` |
| `Technical Skills:` / `Python Developer` | not a name |
| `wednesday addams` / `Wednesday` | not a name (no capitals / one word) |

### 3.2 Email

```python
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
```

Local part, literal `@`, domain, and an extension of at least two letters.

**Language recognized.** With `Local = {A-Z, a-z, 0-9, ., _, %, +, -}`, `Domain = {A-Z, a-z, 0-9, ., -}`, and `Letter = {A-Z, a-z}`:

```text
L(EMAIL_PATTERN) = Local+ · @ · Domain+ · . · Letter{2,}
```

| Input | Result |
| :--- | :--- |
| `mary.watson@email.com`, `dev.user@company.co` | extracted |
| `mary.watson@email` / `@email.com` | not extracted |

### 3.3 Phone Number

```python
PHONE_PATTERN = (
    r"(?<![\w+])"
    r"(?:"
    r"\+\d{1,3}[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"   # with country code
    r"|\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}"                    # without country code
    r")"
    r"(?!\d)"
)
```

- With a country code (`+57 300 1234567`), separators are optional.
- Without a country code, the 3-3-4 groups **must** be separated (`300 123 4567`, `(300) 123-4567`). A long number such as `1234567890` is rejected because it cannot be told apart from an ID number. Dates such as `2001-2004` are rejected because they do not follow 3-3-4.
- `(?<![\w+])` and `(?!\d)` prevent taking part of a longer number.

**Language recognized.** With `Sep = {space, ., -}`:

```text
L = ( + · D{1,3} · Sep? · (? · D³ · )? · Sep? · D³ · Sep? · D⁴ )  ∪  ( (? · D³ · )? · Sep · D³ · Sep · D⁴ )
```

The match cannot be preceded by a letter, digit, or `+`, or followed by a digit.

| Input | Result |
| :--- | :--- |
| `+57 300 1234567`, `300 123 4567`, `(300) 123-4567` | extracted |
| `1234567890`, `2001-2004` | not extracted |

### 3.4 Programming Languages

```python
PROGRAMMING_LANGUAGES_PATTERN = (
    r"(?:\b(?:JavaScript|Javascript|TypeScript|Python|SQL|Bash)\b"
    r"|(?<![\w.])JS(?!\w))"
)
```

`JS` is a separate alternative because `\bJS\b` would match the `js` of `React.js` or `Node.js`: the dot creates a word boundary. The lookbehind `(?<![\w.])` rejects a `JS` that is preceded by a letter, digit, or dot.

**Language recognized** (any capitalization):

```text
L = { javascript, typescript, python, sql, bash }    as complete words
  ∪ { js }                                           not preceded by a letter, digit, or "."
```

### 3.5 Frameworks and Libraries

```python
FRAMEWORKS_LIBRARIES_PATTERN = (
    r"\b(?:React(?:\.js|JS)?|Angular|Vue|Node(?:\.js|JS)|Django|Spring\s+Boot"
    r"|Pandas|NumPy|Scikit[-\s]?learn|sklearn|Tensor\s*Flow|Py\s*Torch"
    r"|Apache\s+Spark|Spark|Apache\s+Airflow|Airflow)\b"
)
```

- `React(?:\.js|JS)?` matches `React`, `React.js`, and `ReactJS`. `Node(?:\.js|JS)` matches `Node.js` and `NodeJS`.
- `Scikit[-\s]?learn` matches `Scikit-learn`, `Scikit learn`, and `Scikitlearn`. `sklearn` is a separate alternative.
- `Tensor\s*Flow` and `Py\s*Torch` accept the forms with and without a space (`TensorFlow`, `Tensor Flow`).

**Language recognized** (any capitalization, complete words):

```text
L = { react, react.js, reactjs, angular, vue, node.js, nodejs, django,
      pandas, numpy, sklearn, spark, airflow }
  ∪ { spring·W·boot, apache·W·spark, apache·W·airflow }
  ∪ { scikit·(- | W | ε)·learn }
  ∪ { tensor·W?·flow, py·W?·torch }
```

### 3.6 Databases

```python
DATABASES_PATTERN = r"\b(?:PostgreSQL|Postgres|NoSQL|SQL)\b"
```

The longer alternatives come first. The stage extracts `Postgres` as it is written, and Stage 2 later maps it to `POSTGRESQL`.

**Language recognized:** `L = { postgresql, postgres, nosql, sql }` as complete words, with any capitalization. `MySQL` is not recognized, because there is no `\b` between `y` and `S`.

### 3.7 Academic Qualifications

```python
ACADEMIC_QUALIFICATIONS_PATTERN = (
    r"\b(?:Bachelor(?:['’]s)?|B\.?Sc\.?|Master(?:['’]s)?|M\.?Sc\.?|Ph\.?D\.?"
    r"|Computer\s+Science|Software\s+Engineering|Systems\s+Engineering|Data\s+Science"
    r")(?!\w)"
)
```

- `\b` at the start prevents matches inside words (`master` in `Webmaster`).
- `(?!\w)` replaces the final `\b`, because `Ph.D.` and `B.Sc.` end with a period.
- `['’]` accepts both apostrophes (`Bachelor's`, `Bachelor’s`).

The input `Bachelor's in Computer Science` produces `Bachelor's` and `Computer Science`.

**Language recognized:**

```text
L = { bachelor, bachelor's, master, master's }
  ∪ { b·.?·sc·.?, m·.?·sc·.?, ph·.?·d·.? }
  ∪ { computer·W·science, software·W·engineering, systems·W·engineering, data·W·science }
```

Each match starts at a word boundary and is not followed by a letter or digit.

### 3.8 Professional Experience

```python
EXPERIENCE_PATTERN = (
    r"(?<![\d.,\-–])(?<![\-–]\s)"
    r"\b\d+\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+professional)?\s+experience\b"
)
```

- It matches `2 years of experience`, `3 years experience`, `5+ years of experience`, `1 yr of experience`, and `4 years of professional experience`.
- The lookbehinds prevent extracting part of a number: `1.5 years ...` and `10-15 years ...` are not extracted, instead of producing `5 years` or `15 years`.

**Language recognized:**

```text
L = D+ · (+)? · W? · (year | years | yr | yrs) · (W·of)? · (W·professional)? · W · experience
```

The number cannot be preceded by a digit, `.`, `,`, `-`, or `–`. Because the expression already guarantees this structure, the transducer `M_EXP` of Stage 2 only copies the number.

### 3.9 Tools and Technologies

```python
TOOLS_TECHNOLOGIES_PATTERN = (
    r"\b(?:Git|Docker|Kubernetes|Nmap|Linux|TCP\s*/?\s*IP|Networking|Network"
    r"|ETL|ELT|Data\s+Pipelines?|Data\s+Warehousing|Data\s+Warehouse)\b"
)
```

`TCP\s*/?\s*IP` accepts `TCP/IP`, `TCP / IP`, and `TCP IP`. `Data\s+Pipelines?` accepts both singular and plural.

**Language recognized** (complete words):

```text
L = { git, docker, kubernetes, nmap, linux, networking, network, etl, elt }
  ∪ { tcp·W?·(/)?·W?·ip }
  ∪ { data·W·pipeline, data·W·pipelines, data·W·warehousing, data·W·warehouse }
```

### 3.10 Other Relevant Qualifications

```python
OTHER_QUALIFICATIONS_PATTERN = (
    r"\b(?:Machine[-\s]Learning\s+Model\s+Development|REST\s+APIs?|Machine[-\s]Learning"
    r"|Vulnerability\s+Assessment|Cyber\s*Security|Cybersecurity|Security\s+Automation)\b"
)
```

`Machine Learning Model Development` is written before `Machine Learning` so that the longer qualification is extracted complete. `REST\s+APIs?` accepts `REST API` and `REST APIs`.

**Language recognized** (complete words):

```text
L = { machine·(- | W)·learning·W·model·W·development, machine·(- | W)·learning }
  ∪ { rest·W·api, rest·W·apis }
  ∪ { vulnerability·W·assessment, security·W·automation }
  ∪ { cyber·W?·security }
```

---

## 4. Implementation

| File | Responsibility |
| :--- | :--- |
| `regex_patterns.py` | Defines the patterns of Section 3. It has no logic. |
| `resume_extractor.py` | Applies the patterns with `re.findall(..., flags=re.IGNORECASE)` (`re.search` with `re.MULTILINE` for the name). It has one function per category (`extract_name`, `extract_contact_information`, `extract_programming_languages`, ...) and the entry point `extract_resume_information(text)`. |
| `extracted_data.py` | `ExtractedData`, the data structure that keeps the result. |

```python
@dataclass
class ExtractedData:
    name: str | None = None                      # one candidate per résumé
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    programming_languages: list[str] = field(default_factory=list)
    frameworks_libraries: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    academic_qualifications: list[str] = field(default_factory=list)
    professional_experience: list[str] = field(default_factory=list)
    tools_technologies: list[str] = field(default_factory=list)
    other_qualifications: list[str] = field(default_factory=list)
```

Each list keeps the strings exactly as they were found and in the order they appear. A category that is not found produces an empty list (or `None` for the name). `ExtractedData` is the input of Stage 2.

---

## 5. Example

```text
Mary Jane Watson
mary.watson@email.com
+57 300 1234567
2 years of experience developing predictive models and data-processing pipelines.
Technical Skills:
Python, Pandas, NumPy, Scikit-learn, TensorFlow, Postgres, SQL and Git.
```

```python
ExtractedData(
    name="Mary Jane Watson",
    emails=["mary.watson@email.com"],
    phones=["+57 300 1234567"],
    programming_languages=["Python", "SQL"],
    frameworks_libraries=["Pandas", "NumPy", "Scikit-learn", "TensorFlow"],
    databases=["Postgres", "SQL"],
    academic_qualifications=[],
    professional_experience=["2 years of experience"],
    tools_technologies=["Git"],
    other_qualifications=[],
)
```

`SQL` appears both as a language and as a database. Stage 2 keeps only one `SQL` token.

---

## 6. Limitations

- **No semantic understanding.** In `I do not have experience with Python.`, `Python` is still extracted. A phrase such as "Facebook's JavaScript library" is not recognized as React. This stage is lexical by design.
- **Closed vocabulary.** Qualifications outside the vocabulary of the four profiles are ignored.
- **Phone formats.** Only common formats are supported. A number without separators and without a country code is rejected on purpose.
- **Candidate name.** If the résumé does not start with the name and has no `Name:` label, the result is `None`. A first line of capitalized words that is not a name (for example `Bogotá Colombia`) may be taken as one. Names longer than 4 words or written in lower case are not recognized.
