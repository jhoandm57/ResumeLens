# ResumeLens – Regular Expression Extraction Stage

## 1. Purpose of the Stage

ResumeLens receives a résumé as unstructured text and uses regular expressions implemented with Python's `re` module to identify relevant information such as:

- Candidate name
- Contact information
- Programming languages
- Frameworks and libraries
- Databases
- Academic qualifications
- Professional experience
- Tools and technologies
- Other relevant qualifications

The extracted information is stored in a structured data representation that will be used by the following stages of the ResumeLens pipeline.

The regular expression stage is responsible only for **recognizing and extracting information**. It does not normalize different representations of the same qualification and does not classify the candidate into a professional profile.

For example, if the résumé contains:

```text
Technical Skills:
Python, React.js, NodeJS, Postgres, Git.
```

the extraction stage should preserve the forms found in the résumé:

```text
Python
React.js
NodeJS
Postgres
Git
```

The normalization stage will later transform equivalent variants into their canonical representations:

```text
Python       -> PYTHON
React.js     -> REACT
NodeJS       -> NODE_JS
Postgres     -> POSTGRESQL
Git          -> GIT
```

This separation allows each stage of the formal-language pipeline to have a specific responsibility.

### 1.1 Requirements of the Stage

According to the project statement, for each relevant type of information the team must:

| Requirement | Where |
| :--- | :--- |
| Define the corresponding regular expression | Section 4 (one subsection per category) and `src/model/extraction/regex_patterns.py` |
| Explain the language or textual pattern recognized by the expression | Section 4, paragraph **Language recognized** of each subsection |
| Implement the expression using Python's `re` module | `src/model/extraction/resume_extractor.py` (Section 9.2) |
| Keep the extracted information in a file or a data structure | `ExtractedData` dataclass in `src/model/extraction/extracted_data.py` (Section 9.3) |

Notation used in the **Language recognized** paragraphs: `L(R)` is the language (set of strings) recognized by the expression `R`; `·` is concatenation, `|` is union, `*` is zero or more repetitions, `+` is one or more repetitions, and `?` is an optional element.

---

## 2. Extraction Categories

The regular expression system is divided into several categories. Each category corresponds to a type of information that ResumeLens must be able to identify in a résumé.

### 2.1 Candidate Name

The name of the candidate is needed by the candidate-profile stage (DSL), which must represent the personal information of the candidate.

Unlike the other categories, the name does not belong to a controlled vocabulary: any person can have any name. For this reason the name is recognized by its **form** and its **position** in the résumé:

- It is written with capital initials (`Wednesday Addams`) or completely in capitals (`CLARK KENT`).
- It has between 2 and 4 words, optionally joined by lower-case particles (`Juan de la Cruz`).
- It appears alone in the **first non-empty line** of the résumé (as in the examples of the statement), or after an explicit label (`Name: Mary Jane Watson`).

Examples:

```text
Wednesday Addams
Mary Jane Watson
María José Gómez
Juan de la Cruz
Name: Peter Parker
```

The name is a single value (one résumé belongs to one candidate), so it is stored as a string, not as a list.

### 2.2 Contact Information

This category includes information used to identify communication channels for the candidate.

The initial implementation will support:

- Email addresses
- Telephone numbers

(The candidate name is described in Section 2.1.)

Examples:

```text
mary.watson@email.com
john.smith@gmail.com
+57 300 1234567
300 123 4567
+57-300-1234567
```

### 2.3 Programming Languages

The programming-language vocabulary is obtained by combining the qualifications of the four reference profiles.

The initial supported vocabulary is:

```text
JavaScript
Javascript
JS
TypeScript
Python
SQL
Bash
```

The regular expressions will be case-insensitive so that variants such as:

```text
Python
python
PYTHON
```

can be recognized as the same extracted lexical item while preserving the original text found in the résumé.

### 2.4 Frameworks and Libraries

The framework and library vocabulary combines the technologies associated with the four profiles.

The initial supported vocabulary is:

```text
React
React.js
ReactJS

Angular

Vue

Node.js
NodeJS

Django

Spring Boot

Pandas

NumPy

Scikit-learn
Scikit learn
Scikitlearn
sklearn

TensorFlow
Tensor Flow

PyTorch
Py Torch

Apache Spark
Spark

Apache Airflow
Airflow
```

The regular expressions must recognize the different ways in which the same technology can appear in résumé text.

For example:

```text
React
React.js
ReactJS
```

should all be extracted.

Likewise:

```text
Node.js
NodeJS
```

should both be extracted.

### 2.5 Databases

The database vocabulary includes the database-related qualifications present in the reference profiles and the examples provided by the project.

The initial supported vocabulary is:

```text
PostgreSQL
Postgres
SQL
NoSQL
```

In particular, the following variants must be recognized:

```text
PostgreSQL
Postgres
```

because they will later be normalized to:

```text
POSTGRESQL
```

The extraction stage preserves the original variant.

### 2.6 Academic Qualifications

This category identifies academic degrees and fields of study that may appear in a résumé.

The initial vocabulary includes:

```text
Bachelor
Bachelor's
BSc
B.Sc.

Master
Master's
MSc
M.Sc.

PhD
Ph.D.

Computer Science
Software Engineering
Systems Engineering
Data Science
```

Examples of text that should be recognized include:

```text
Bachelor's in Computer Science
B.Sc. in Software Engineering
Master's in Data Science
Ph.D. in Computer Science
```

### 2.7 Professional Experience

The professional experience category identifies explicit references to years of experience.

Examples include:

```text
2 years of experience
3 years experience
5+ years of experience
2 yrs of experience
4 years of professional experience
```

Expressions where the number is only part of a larger number (`1.5 years of experience`, `10-15 years of experience`) are **not** extracted, because extracting only `5` or `15` would give a wrong value.

The initial regular expression focuses on explicit experience expressions instead of attempting to infer experience from job descriptions.

For example:

```text
3 years of experience developing web applications.
```

should be recognized, while a sentence such as:

```text
Worked at Google from 2022 to 2025.
```

will not necessarily be interpreted as a number of years by the regular expression stage.

### 2.8 Tools and Technologies

This category contains technologies and tools that are relevant to the four professional profiles but are not necessarily programming languages or frameworks.

The initial vocabulary includes:

```text
Git

Docker
Kubernetes

Nmap

Linux

TCP/IP
TCP IP
TCP / IP

Networking
Network

ETL
ELT

Data Pipeline
Data Pipelines

Data Warehouse
Data Warehousing
```

The extraction stage preserves the original form.

For example:

```text
TCP/IP
```

remains:

```text
TCP/IP
```

and is not converted into a canonical representation until the normalization stage.

### 2.9 Other Relevant Qualifications

Some qualifications describe concepts or professional capabilities rather than a specific programming language, framework, database, or tool.

The initial vocabulary includes:

```text
REST API
REST APIs

Machine Learning
Machine-Learning

Machine Learning Model Development

Vulnerability Assessment

Cybersecurity
Cyber Security

Security Automation
```

These expressions allow the system to capture relevant qualifications that contribute to the classification of the four profiles.

---

## 3. Qualification Vocabulary by Reference Profile

The extraction vocabulary is based on the four reference profiles used by ResumeLens.

### 3.1 Full Stack Developer

The project guide defines the Full Stack Developer profile using qualifications such as:

- JavaScript or TypeScript
- React, Angular, or Vue
- Node.js, Django, Spring Boot, or a similar backend technology
- SQL or NoSQL databases
- REST APIs
- Git

The example résumé in the project guide contains:

```text
JS
React.js
NodeJS
Postgres
Git
```

Therefore, the extraction system must support both the general qualifications and the concrete variants used in the example.

Relevant vocabulary:

```text
JavaScript
Javascript
JS
TypeScript

React
React.js
ReactJS
Angular
Vue

Node.js
NodeJS
Django
Spring Boot

SQL
NoSQL
PostgreSQL
Postgres

REST API
REST APIs

Git
```

### 3.2 Machine Learning Engineer

The project guide defines the Machine Learning Engineer profile using qualifications such as:

- Python
- Pandas or NumPy
- Scikit-learn
- TensorFlow, or PyTorch
- Machine-learning model development
- SQL
- Git

The example résumé contains:

```text
Python
Pandas
NumPy
Scikit-learn
TensorFlow
SQL
Git
```

Relevant vocabulary:

```text
Python

Pandas
NumPy

Scikit-learn
Scikit learn
Scikitlearn
sklearn

TensorFlow
Tensor Flow

PyTorch
Py Torch

Machine Learning
Machine-Learning
Machine Learning Model Development

SQL

Git
```

### 3.3 Cybersecurity Engineer

The Cybersecurity Engineer profile is an additional profile designed for this project. Its purpose is to provide a software-engineering profile with qualifications that can be distinguished from Full Stack Development and Machine Learning.

The proposed qualifications are:

- Python or Bash
- Linux
- Networking or TCP/IP
- Cybersecurity tools or frameworks
- Docker or Kubernetes
- Vulnerability assessment
- Git

For extraction purposes, these are represented by the following vocabulary:

```text
Python
Bash

Linux

Networking
Network
TCP/IP
TCP IP
TCP / IP

Docker
Kubernetes

Nmap

Vulnerability Assessment

Cybersecurity
Cyber Security

Security Automation

Git
```

This vocabulary is a project design decision and is not presented as a verbatim list from the original project guide.

### 3.4 Data Engineer

The Data Engineer profile is an additional profile designed for this project. Its purpose is to represent data infrastructure, data processing, and data-pipeline development rather than machine-learning model development.

The proposed qualifications are:

- Python or SQL
- Apache Spark
- Apache Airflow
- ETL or ELT
- Data pipelines
- Data warehousing
- Relational or NoSQL databases
- Git

For extraction purposes, these are represented by the following vocabulary:

```text
Python
SQL

Apache Spark
Spark

Apache Airflow
Airflow

ETL
ELT

Data Pipeline
Data Pipelines

Data Warehouse
Data Warehousing

PostgreSQL
Postgres
SQL
NoSQL

Git
```

The Data Engineer vocabulary intentionally emphasizes data engineering technologies and processes instead of machine-learning libraries such as TensorFlow, PyTorch, or Scikit-learn.

This separation is important because the classification stage must be able to distinguish Data Engineer from Machine Learning Engineer.

---

## 4. Regex Design

The regular expressions are divided by extraction category instead of using one large expression for the entire résumé.

This design makes the implementation easier to understand, test, modify, and extend.

All the patterns are applied with `re.IGNORECASE` (Section 5), **except the name patterns** (Section 4.1), because capital letters are exactly what identifies a proper name.

The main patterns will be defined in:

```text
src/model/extraction/regex_patterns.py
```

The extraction logic will be implemented separately in:

```text
src/model/extraction/resume_extractor.py
```

The extracted information will be represented in:

```text
src/model/extraction/extracted_data.py
```

### 4.1 Candidate Name

The name is recognized with two expressions built from the same pieces:

```python
_UPPER = r"A-ZÀ-ÖØ-Þ"        # upper-case letters, including accented letters
_LOWER = r"a-zß-öø-ÿ"        # lower-case letters, including accented letters

_NAME_WORD = (
    rf"(?:(?:[{_UPPER}]['’])?[{_UPPER}][{_LOWER}]+(?:[-'’]?[{_UPPER}]?[{_LOWER}]+)*"
    rf"|[{_UPPER}]{{2,}}(?:[-'’][{_UPPER}]{{2,}})*)"
)

_NAME_PARTICLE = r"(?:de|del|la|las|los|da|das|do|dos|di|du|van|von|der|y)"

_FULL_NAME = (
    rf"{_NAME_WORD}"
    rf"(?:[ \t]+(?:{_NAME_PARTICLE}[ \t]+)*{_NAME_WORD}){{1,3}}"
)

NAME_LABEL_PATTERN = (
    rf"^[ \t]*(?i:(?:full[ \t]+)?name)[ \t]*:[ \t]*"
    rf"({_FULL_NAME})"
    rf"[ \t]*$"
)

NAME_HEADER_PATTERN = (
    rf"\A\s*{_NOT_A_NAME}"
    rf"({_FULL_NAME})"
    rf"[ \t]*$"
)
```

#### Structure

`_NAME_WORD` recognizes one word of a name in two forms:

- **Capitalized word:** one upper-case letter followed by lower-case letters. It may contain internal capitals or a hyphen/apostrophe (`McDonald`, `Jean-Luc`) and may start with a letter and an apostrophe (`O'Connor`).
- **Word in capitals:** two or more upper-case letters (`PARKER`), optionally joined by a hyphen (`JEAN-LUC`).

`_NAME_PARTICLE` recognizes the lower-case connectors of Spanish, Portuguese, Dutch, and German names (`de`, `la`, `van`, `von`, ...).

`_FULL_NAME` is a word followed by **1 to 3** more words (`{1,3}`), separated by spaces or tabs (`[ \t]+`), with optional particles between them. Spaces and tabs are used instead of `\s` so that a name **cannot continue in the next line**.

`NAME_LABEL_PATTERN` (form 1) recognizes a line with an explicit label:

- `^` and `$` (with `re.MULTILINE`) require the label and the name to occupy a complete line.
- `(?i:(?:full[ \t]+)?name)` accepts `Name`, `NAME`, `Full Name`, ... The flag `(?i:...)` makes **only the label** case-insensitive.
- The group `(...)` captures the name.

`NAME_HEADER_PATTERN` (form 2) recognizes the name in the header of the résumé:

- `\A` is the beginning of the text (not of each line), and `\s*` skips blank lines and indentation. Therefore only the **first non-empty line** can be the name.
- `[ \t]*$` requires that nothing else appears in that line, so `Technical Skills:` or `JS, React.js` are not names (they contain `:` or `,`).
- `_NOT_A_NAME` contains two negative lookaheads:

```python
_NOT_A_NAME = (
    r"(?!(?i:curriculum|resume|résumé|cv|technical|skills|experience"
    r"|professional|education|contact|profile|summary|objective)\b)"
    r"(?![^\n]*\b(?i:developer|engineer|scientist|analyst|architect"
    r"|manager|designer|programmer|consultant|intern)\b)"
)
```

The first one rejects a line that starts with a section heading (`Curriculum Vitae`, `Technical Skills`). The second one rejects a line that contains a job title anywhere (`Python Developer`, `Senior Data Engineer`); `[^\n]*` does not cross the line break, so only the first line is checked.

The extraction function (`extract_name`) tries form 1 first and form 2 after it, and replaces any sequence of spaces with a single space (`Mary   Jane Watson -> Mary Jane Watson`). If no form matches, the name is `None`.

#### Language recognized

Let `U` be the set of upper-case letters and `l` the set of lower-case letters (both including accented letters), `S = { space, tab }`, and `P` the set of particles. Then:

```text
L(_NAME_WORD) = ( (U·{', ’})? · U · l+ · ({-, ', ’}? · U? · l+)* )
              ∪ ( U·U+ · ({-, ', ’} · U·U+)* )

L(_FULL_NAME) = L(_NAME_WORD) · ( S+ · (P·S+)* · L(_NAME_WORD) ){1,3}
```

that is, sequences of 2 to 4 name words separated by blanks, with optional particles. `NAME_HEADER_PATTERN` recognizes the texts whose first non-empty line belongs to `L(_FULL_NAME)` and does not start with a heading word or contain a job title; `NAME_LABEL_PATTERN` recognizes lines of the form `(full )?name : w`, with `w ∈ L(_FULL_NAME)`.

Examples:

| Input (first line) | Result |
| :--- | :--- |
| `Wednesday Addams` | `Wednesday Addams` |
| `Mary Jane Watson` | `Mary Jane Watson` |
| `Juan de la Cruz` | `Juan de la Cruz` |
| `CLARK KENT` | `CLARK KENT` |
| `Name: Peter Parker` (any line) | `Peter Parker` |
| `Technical Skills:` | not a name |
| `Python Developer` | not a name |
| `wednesday addams` | not a name (no capitals) |
| `Wednesday` | not a name (only one word) |

### 4.2 Email

The initial email pattern is:

```python
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
```

#### Structure

The pattern can be divided into several parts:

```regex
[A-Za-z0-9._%+-]+
```

Matches the local part of the email address.

For example:

```text
mary.watson
john_smith
user123
```

The `+` means that one or more characters from the specified set are required.

The symbol:

```text
@
```

matches the literal `@` character.

Then:

```regex
[A-Za-z0-9.-]+
```

matches the domain.

Examples:

```text
gmail
company
university
```

Finally:

```regex
\.[A-Za-z]{2,}
```

matches the domain extension.

Examples:

```text
.com
.org
.co
.edu
```

The use of `\b` establishes word boundaries around the complete expression.

Examples that should be recognized:

```text
mary.watson@email.com
john.smith@gmail.com
peter_parker@company.co
```

### 4.3 Phone Number

The phone-number pattern is:

```python
PHONE_PATTERN = (
    r"(?<![\w+])"
    r"(?:"
    r"\+\d{1,3}[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    r"|\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}"
    r")"
    r"(?!\d)"
)
```

A phone number is accepted in two forms:

1. **With country code** (`+` followed by 1 to 3 digits): `+57 300 1234567`, `+57-300-123-4567`, `+57 (300) 123 4567`. The separators between the groups are optional.
2. **Without country code**: the groups 3-3-4 **must** be separated: `300 123 4567`, `300-123-4567`, `(300) 123-4567`.

#### Important components

- `\+\d{1,3}` is the country code (`+57`, `+1`).
- `\(?\d{3}\)?` is the area/mobile prefix, optionally between parentheses.
- `[\s.-]?` is an optional separator (space, `.`, or `-`); `[\s.-]` (without `?`) is a mandatory separator.
- `\d{3}` and `\d{4}` are the last two groups.
- `(?<![\w+])` and `(?!\d)` (lookarounds) prevent extracting only part of a longer sequence of digits or letters.

#### Design decisions

- A long number without separators and without `+` (for example `1234567890`) is **not** accepted, because it cannot be distinguished from an ID number.
- Year ranges and dates such as `2001-2004` or `2001-10-09` are **not** accepted, because they do not have the 3-3-4 structure.

#### Language recognized

Let `D` be the set of digits and `Sep = { space, ., - }`:

```text
L(PHONE_PATTERN) = ( + · D{1,3} · Sep? · (? · D³ · )? · Sep? · D³ · Sep? · D⁴ )
                 ∪ ( (? · D³ · )? · Sep · D³ · Sep · D⁴ )
```

not preceded by a letter, digit, or `+`, and not followed by a digit.

| Input | Result |
| :--- | :--- |
| `+57 300 1234567` | extracted |
| `300 123 4567` | extracted |
| `(300) 123-4567` | extracted |
| `1234567890` | not extracted |
| `2001-2004` | not extracted |

### 4.4 Programming Languages

The initial pattern is:

```python
PROGRAMMING_LANGUAGES_PATTERN = (
    r"(?:"
    r"\b(?:"
    r"JavaScript"
    r"|Javascript"
    r"|TypeScript"
    r"|Python"
    r"|SQL"
    r"|Bash"
    r")\b"
    r"|(?<![\w.])JS(?!\w)"
    r")"
)
```

`JS` is separated from the other alternatives because `\bJS\b` would incorrectly match the `js` of `React.js`, `Node.js`, or `app.js` (the dot is a word boundary). The lookbehind `(?<![\w.])` rejects `JS` preceded by a letter, digit, or dot.

The main structure is:

```regex
\b(?: ... )\b
```

The first and last `\b` establish word boundaries.

The expression:

```regex
(?: ... )
```

creates a non-capturing group.

Inside the group, the `|` operator represents alternatives.

Therefore:

```regex
Python|Bash|SQL
```

means:

```text
Python OR Bash OR SQL
```

The pattern recognizes:

```text
JavaScript
Javascript
JS
TypeScript
Python
SQL
Bash
```

The extraction process will use `re.IGNORECASE` so that different capitalizations are accepted.

For example:

```text
Python
python
PYTHON
PyThOn
```

can all be detected.

The extracted value should preserve the original text appearing in the résumé.

#### Language recognized

With case-insensitive matching (`re.IGNORECASE`):

```text
L = { javascript, typescript, python, sql, bash }   (as complete words)
  ∪ { js }                                          (not preceded by a letter, digit, or ".")
```

where every letter can be upper-case or lower-case. For example `React.js` does not produce `JS`.

### 4.5 Frameworks and Libraries

The initial pattern is:

```python
FRAMEWORKS_LIBRARIES_PATTERN = (
    r"\b(?:"
    r"React(?:\.js|JS)?"
    r"|Angular"
    r"|Vue"
    r"|Node(?:\.js|JS)"
    r"|Django"
    r"|Spring\s+Boot"
    r"|Pandas"
    r"|NumPy"
    r"|Scikit[-\s]?learn"
    r"|sklearn"
    r"|Tensor\s*Flow"
    r"|Py\s*Torch"
    r"|Apache\s+Spark"
    r"|Spark"
    r"|Apache\s+Airflow"
    r"|Airflow"
    r")\b"
)
```

#### React variants

The expression:

```regex
React(?:\.js|JS)?
```

recognizes:

```text
React
React.js
ReactJS
```

The part:

```regex
(?:\.js|JS)?
```

is optional because of `?`.

Therefore:

```text
React
```

is valid even when `.js` or `JS` is not present.

#### Node.js variants

The expression:

```regex
Node(?:\.js|JS)
```

recognizes:

```text
Node.js
NodeJS
```

#### Spring Boot

The expression:

```regex
Spring\s+Boot
```

recognizes:

```text
Spring Boot
```

and also supports multiple whitespace characters between the two words.

The expression:

```regex
\s+
```

means one or more whitespace characters.

#### Scikit-learn variants

The expression:

```regex
Scikit[-\s]?learn
```

recognizes:

```text
Scikit-learn
Scikit learn
Scikitlearn
```

The part:

```regex
[-\s]?
```

allows:

- a hyphen,
- whitespace,
- or no separator.

The abbreviation `sklearn` (an example of the project statement) is a separate alternative.

#### TensorFlow variants

The expression:

```regex
Tensor\s*Flow
```

recognizes:

```text
TensorFlow
Tensor Flow
Tensor    Flow
```

The difference between `\s*` and `\s+` is that `*` allows zero or more spaces.

#### PyTorch variants

The expression:

```regex
Py\s*Torch
```

recognizes:

```text
PyTorch
Py Torch
Py    Torch
```

#### Language recognized

With case-insensitive matching, and `W` = one or more whitespace characters:

```text
L = { react, react.js, reactjs, angular, vue, node.js, nodejs, django,
      pandas, numpy, sklearn, spark, airflow }
  ∪ { spring·W·boot, apache·W·spark, apache·W·airflow }
  ∪ { scikit·(- | W | ε)·learn }
  ∪ { tensor·W?·flow, py·W?·torch }
```

as complete words (`\b` at both ends).

### 4.6 Databases

The initial database pattern is:

```python
DATABASES_PATTERN = (
    r"\b(?:"
    r"PostgreSQL"
    r"|Postgres"
    r"|NoSQL"
    r"|SQL"
    r")\b"
)
```

The longer alternatives are written first (`PostgreSQL` before `Postgres`, `NoSQL` before `SQL`) so that the regex engine tries the most specific form first.

The expression recognizes:

```text
PostgreSQL
Postgres
SQL
NoSQL
```

The important distinction is that the extraction stage does not transform:

```text
Postgres
```

into:

```text
POSTGRESQL
```

Instead, it extracts:

```text
Postgres
```

The normalization stage will later apply the FST transformation:

```text
Postgres
PostgreSQL
       ↓
POSTGRESQL
```

This preserves the separation of responsibilities between the two stages.

#### Language recognized

```text
L = { postgresql, postgres, nosql, sql }
```

as complete words, with any capitalization. `MySQL` is not recognized (`\b` does not exist between `y` and `S`).

### 4.7 Academic Qualifications

The initial academic qualification pattern is:

```python
ACADEMIC_QUALIFICATIONS_PATTERN = (
    r"\b(?:"
    r"Bachelor(?:['’]s)?"
    r"|B\.?Sc\.?"
    r"|Master(?:['’]s)?"
    r"|M\.?Sc\.?"
    r"|Ph\.?D\.?"
    r"|Computer\s+Science"
    r"|Software\s+Engineering"
    r"|Systems\s+Engineering"
    r"|Data\s+Science"
    r")(?!\w)"
)
```

The pattern supports variants such as:

```text
Bachelor
Bachelor's

BSc
B.Sc.

Master
Master's

MSc
M.Sc.

PhD
Ph.D.
```

It also recognizes academic fields such as:

```text
Computer Science
Software Engineering
Systems Engineering
Data Science
```

For example:

```text
Bachelor's in Computer Science
```

can produce the extracted qualifications:

```text
Bachelor's
Computer Science
```

The extraction stage does not attempt to determine whether the degree has been completed or whether it is currently being pursued.

#### Boundaries

- `\b` at the beginning prevents matches inside other words (for example, `master` inside `Webmaster` or `Headmaster`).
- `(?!\w)` is used at the end instead of `\b`, because `Ph.D.` and `B.Sc.` end with a period, and there is no word boundary after a period followed by a space.
- `['’]` accepts both apostrophes: `Bachelor's` and `Bachelor’s`.

#### Language recognized

With case-insensitive matching, and `W` = one or more whitespace characters:

```text
L = { bachelor, bachelor's, master, master's }
  ∪ { b·.?·sc·.?, m·.?·sc·.?, ph·.?·d·.? }
  ∪ { computer·W·science, software·W·engineering,
      systems·W·engineering, data·W·science }
```

starting at a word boundary and not followed by a letter or digit.

### 4.8 Professional Experience

The initial experience pattern is:

```python
EXPERIENCE_PATTERN = (
    r"(?<![\d.,\-–])"
    r"(?<![\-–]\s)"
    r"\b"
    r"\d+\+?"
    r"\s*(?:years?|yrs?)"
    r"(?:\s+of)?"
    r"(?:\s+professional)?"
    r"\s+experience"
    r"\b"
)
```

The pattern recognizes expressions such as:

```text
2 years of experience
3 years experience
5+ years of experience
2 yrs of experience
1 year of experience
```

#### Important components

```regex
\d+
```

matches one or more digits.

Therefore:

```text
2
10
15
```

can be recognized.

The expression:

```regex
\+?
```

allows an optional `+`.

Therefore:

```text
5+
```

is accepted.

The expression:

```regex
(?:years?|yrs?)
```

supports:

```text
year
years
yr
yrs
```

The expression:

```regex
(?:\s+of)?
```

allows the phrase:

```text
of
```

to be optional.

Therefore both:

```text
3 years of experience
```

and:

```text
3 years experience
```

can be recognized.

The expression:

```regex
(?:\s+professional)?
```

allows the optional word `professional`:

```text
4 years of professional experience
```

The lookbehinds:

```regex
(?<![\d.,\-–])
(?<![\-–]\s)
```

prevent taking only part of a number:

```text
1.5 years of experience     -> not extracted (instead of "5 years of experience")
10-15 years of experience   -> not extracted (instead of "15 years of experience")
10 - 15 years of experience -> not extracted
```

The pattern intentionally focuses on explicit mentions of experience.

#### Language recognized

Let `D` be the set of digits and `W` one or more whitespace characters:

```text
L(EXPERIENCE_PATTERN) = D+ · (+)? · W? · (year | years | yr | yrs)
                        · (W·of)? · (W·professional)? · W · experience
```

with any capitalization, as long as the number is not preceded by a digit, `.`, `,`, `-`, or `–`. This is the same language accepted by the transducer `M_EXP` of the normalization stage (`06_fst_design.md`, Section 6.7).

### 4.9 Tools and Technologies

The initial pattern is:

```python
TOOLS_TECHNOLOGIES_PATTERN = (
    r"\b(?:"
    r"Git"
    r"|Docker"
    r"|Kubernetes"
    r"|Nmap"
    r"|Linux"
    r"|TCP\s*/?\s*IP"
    r"|Networking"
    r"|Network"
    r"|ETL"
    r"|ELT"
    r"|Data\s+Pipelines?"
    r"|Data\s+Warehousing"
    r"|Data\s+Warehouse"
    r")\b"
)
```

#### TCP/IP variants

The expression:

```regex
TCP\s*/?\s*IP
```

recognizes:

```text
TCP/IP
TCP / IP
TCP IP
```

The expression:

```regex
/?
```

makes the slash optional.

The expression:

```regex
\s*
```

allows zero or more whitespace characters.

#### Data Pipeline variants

The expression:

```regex
Data\s+Pipelines?
```

recognizes:

```text
Data Pipeline
Data Pipelines
```

The `s?` makes the final `s` optional.

#### Data Warehousing

The pattern recognizes:

```text
Data Warehouse
Data Warehousing
```

These expressions represent data-engineering concepts rather than individual software libraries.

#### Language recognized

With case-insensitive matching, `W` = one or more whitespace characters and `W?` = zero or more:

```text
L = { git, docker, kubernetes, nmap, linux, networking, network, etl, elt }
  ∪ { tcp·W?·(/)?·W?·ip }
  ∪ { data·W·pipeline, data·W·pipelines, data·W·warehousing, data·W·warehouse }
```

as complete words.

### 4.10 Other Relevant Qualifications

The initial pattern is:

```python
OTHER_QUALIFICATIONS_PATTERN = (
    r"\b(?:"
    r"Machine[-\s]Learning\s+Model\s+Development"
    r"|REST\s+APIs?"
    r"|Machine[-\s]Learning"
    r"|Vulnerability\s+Assessment"
    r"|Cyber\s*Security"
    r"|Cybersecurity"
    r"|Security\s+Automation"
    r")\b"
)
```

#### REST API variants

The expression:

```regex
REST\s+APIs?
```

recognizes:

```text
REST API
REST APIs
```

because the `s?` allows the final `s` to be optional.

#### Machine Learning variants

The expression:

```regex
Machine[-\s]Learning
```

recognizes:

```text
Machine Learning
Machine-Learning
```

The expression:

```regex
[-\s]
```

allows either a hyphen or whitespace between the words.

#### Cybersecurity variants

The expressions:

```regex
Cyber\s*Security
```

and:

```regex
Cybersecurity
```

allow the system to recognize:

```text
Cybersecurity
Cyber Security
```

#### Order of the alternatives

`Machine Learning Model Development` is written **before** `Machine Learning`. The regex engine tries the alternatives from left to right, so the longer qualification is extracted complete instead of only its first two words.

#### Language recognized

With case-insensitive matching and `W` = one or more whitespace characters:

```text
L = { machine·(- | W)·learning·W·model·W·development, machine·(- | W)·learning }
  ∪ { rest·W·api, rest·W·apis }
  ∪ { vulnerability·W·assessment, security·W·automation }
  ∪ { cyber·W?·security }
```

as complete words.

---

## 5. Case-Insensitive Matching

The extraction implementation will use Python's `re.IGNORECASE` flag.

For example:

```python
re.findall(
    PROGRAMMING_LANGUAGES_PATTERN,
    resume_text,
    re.IGNORECASE
)
```

This allows the same regular expression to recognize different capitalization styles.

For example:

```text
Python
python
PYTHON
PyThOn
```

will all be recognized.

The only exception is the candidate name (Section 4.1): its patterns are applied **without** `re.IGNORECASE`, because capital letters are what distinguishes a proper name from the rest of the text (only the label `Name:` is case-insensitive, with the inline flag `(?i:...)`).

This avoids unnecessarily creating patterns such as:

```text
Python
python
PYTHON
PyThOn
```

for every possible capitalization.

The original text found in the résumé should still be preserved in the extraction result whenever possible because normalization is a responsibility of the following stage.

---

## 6. Supported Variations

One of the most important requirements of the regex design is recognizing different textual representations of the same qualification.

The extraction stage should support the following initial variations.

### JavaScript

```text
JavaScript
Javascript
JS
```

Later normalization:

```text
JavaScript
Javascript
JS
    ↓
JAVASCRIPT
```

### React

```text
React
React.js
ReactJS
```

Later normalization:

```text
React
React.js
ReactJS
    ↓
REACT
```

### Node.js

```text
Node.js
NodeJS
```

Later normalization:

```text
Node.js
NodeJS
    ↓
NODE_JS
```

### PostgreSQL

```text
PostgreSQL
Postgres
```

Later normalization:

```text
Postgres
PostgreSQL
    ↓
POSTGRESQL
```

### Pandas

```text
Pandas
pandas
PANDAS
```

The case-insensitive regular expression recognizes the different capitalization forms.

Later normalization:

```text
Pandas
    ↓
PANDAS
```

### Scikit-learn

```text
Scikit-learn
Scikit learn
Scikitlearn
```

Later normalization:

```text
Scikit-learn
Scikit learn
Scikitlearn
        ↓
SCIKIT_LEARN
```

### TensorFlow

```text
TensorFlow
Tensor Flow
```

Later normalization:

```text
TensorFlow
Tensor Flow
    ↓
TENSORFLOW
```

### PyTorch

```text
PyTorch
Py Torch
```

Later normalization:

```text
PyTorch
Py Torch
    ↓
PYTORCH
```

---

## 7. Extraction Strategy

The extraction process follows these steps:

```text
Résumé text
     |
     v
Regex matching
     |
     +----------------------+
     |                      |
     v                      v
Contact                 Qualifications
     |                      |
     |              +-------+-------+
     |              |       |       |
     |              v       v       v
     |           Languages Frameworks Databases
     |              |
     |              +------------------+
     |                                 |
     v                                 v
Academic qualifications        Tools / technologies
     |
     v
Professional experience
     |
     v
Other qualifications
     |
     v
Structured extraction result
```

The extraction process does not perform classification.

For example, if the system finds:

```text
Python
Git
Docker
```

it should not conclude:

```text
CYBERSECURITY_ENGINEER
```

at this stage.

It should simply return:

```text
Python
Git
Docker
```

The classification decision belongs to the finite-automata stage.

---

## 8. Preservation of Original Forms

The extraction stage must preserve the lexical form found in the résumé.

For example, given:

```text
Technical Skills:
Python, React.js, NodeJS, Postgres, Git.
```

the result should contain:

```text
Python
React.js
NodeJS
Postgres
Git
```

It should not directly return:

```text
PYTHON
REACT
NODE_JS
POSTGRESQL
GIT
```

because that would mix extraction and normalization.

The transformation into canonical representations will be performed by the finite-state transducers in the next stage.

Therefore, the pipeline is:

```text
Raw résumé
    |
    v
Regular Expressions
    |
    v
Original extracted qualifications
    |
    v
Finite-State Transducers
    |
    v
Canonical qualifications
    |
    v
Finite Automata
    |
    v
Profile classification
```

---

## 9. File Structure

The extraction implementation is divided into three main files.

```text
src/
└── model/
    └── extraction/
        ├── __init__.py
        ├── regex_patterns.py
        ├── resume_extractor.py
        └── extracted_data.py
```

Each file has a different responsibility.

### 9.1 `regex_patterns.py`

This file contains the regular expression definitions.

Structure:

```text
regex_patterns.py
│
├── NAME_LABEL_PATTERN
├── NAME_HEADER_PATTERN
├── EMAIL_PATTERN
├── PHONE_PATTERN
├── PROGRAMMING_LANGUAGES_PATTERN
├── FRAMEWORKS_LIBRARIES_PATTERN
├── DATABASES_PATTERN
├── ACADEMIC_QUALIFICATIONS_PATTERN
├── EXPERIENCE_PATTERN
├── TOOLS_TECHNOLOGIES_PATTERN
└── OTHER_QUALIFICATIONS_PATTERN
```

This file should contain the patterns themselves rather than the logic used to execute them.

Example:

```python
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
```

The purpose is to keep the regular-expression definitions centralized and easy to modify.

### 9.2 `resume_extractor.py`

This file contains the logic responsible for applying the regular expressions to résumé text.

The main responsibilities are:

```text
Read résumé text
      |
      v
Apply regex patterns
      |
      v
Collect matches
      |
      v
Build structured extraction result
```

The module will contain functions conceptually organized as:

```text
extract_name()
extract_contact_information()
extract_programming_languages()
extract_frameworks_libraries()
extract_databases()
extract_academic_qualifications()
extract_professional_experience()
extract_tools_technologies()
extract_other_qualifications()
```

A general function will combine the results:

```text
extract_resume_information(resume_text)
```

This function will serve as the main entry point for the extraction module.

### 9.3 `extracted_data.py`

This file defines the data structure that keeps the extracted information (requirement: *keep the extracted information in a file or a data structure*):

```python
@dataclass
class ExtractedData:
    name: str | None = None          # a single value (one candidate per résumé)

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

Every list keeps the strings **exactly as they were found** in the résumé and in the order in which they appear. If a category is not found, its list is empty (and the name is `None`).

Example for the résumé of Section 11:

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

`ExtractedData` is the input of the normalization stage (`06_fst_design.md`).

---

## 10. Relationship Between the Three Files

The three files form the following dependency structure:

```text
regex_patterns.py
        |
        | provides regex patterns
        v
resume_extractor.py
        |
        | applies patterns
        v
extracted_data.py
        |
        | stores structured information
        v
Extracted résumé information
```

The responsibilities are therefore separated as follows:

| File | Responsibility |
|---|---|
| `regex_patterns.py` | Defines the regular expressions |
| `resume_extractor.py` | Applies the regular expressions and collects matches |
| `extracted_data.py` | Represents and stores the extracted information |

This separation prevents the extraction module from becoming a single large file containing patterns, processing logic, and data structures at the same time.

---

## 11. Example of the Complete Extraction Process

Consider the following résumé fragment:

```text
Mary Jane Watson

mary.watson@email.com
+57 300 1234567

2 years of experience developing predictive models and data-processing pipelines.

Technical Skills:
Python, Pandas, NumPy, Scikit-learn, TensorFlow,
Postgres, SQL and Git.
```

The extraction stage should identify:

```text
Name:
    Mary Jane Watson

Contact:
    mary.watson@email.com
    +57 300 1234567

Professional Experience:
    2 years of experience

Programming Languages:
    Python
    SQL

Frameworks/Libraries:
    Pandas
    NumPy
    Scikit-learn
    TensorFlow

Databases:
    Postgres
    SQL

Tools/Technologies:
    Git
```

`SQL` is extracted both as a programming language and as a database; the normalization stage keeps only one `SQL` token.

The extracted information remains in its original lexical form.

The next stage can then transform:

```text
Python
Pandas
Scikit-learn
TensorFlow
Postgres
SQL
Git
```

into:

```text
PYTHON
PANDAS
SCIKIT_LEARN
TENSORFLOW
POSTGRESQL
SQL
GIT
```

The finite automaton can then use these canonical symbols to evaluate the candidate's profile.

---

## 12. Design Principles

The regex extraction stage follows the following principles:

### 12.1 Separation of responsibilities

- Regular expressions extract information.
- Finite-state transducers normalize information.
- Finite automata classify information.
- Context-free grammar validates the structured candidate representation.

Each formal model has a different responsibility.

### 12.2 Recognition of variants

The regex system must recognize realistic variations in the way qualifications can appear in résumé text.

Examples include:

```text
React
React.js
ReactJS
```

and:

```text
Postgres
PostgreSQL
```

The objective is to prevent equivalent qualifications from being missed simply because the candidate used a different textual representation.

### 12.3 Case-insensitive matching

The implementation uses case-insensitive matching where appropriate so that capitalization does not prevent recognition.

Examples:

```text
Python
python
PYTHON
```

should all be recognized.

### 12.4 Preservation before normalization

The original extracted form should be preserved until the normalization stage.

For example:

```text
React.js
```

must remain:

```text
React.js
```

after extraction.

It becomes:

```text
REACT
```

only after the corresponding FST transformation.

### 12.5 Controlled vocabulary

The system does not attempt to recognize every technology that exists.

Instead, the vocabulary is controlled according to the four professional profiles used by ResumeLens.

This makes the extraction process:

- More predictable
- Easier to test
- Easier to maintain
- More directly connected to the classification automata

New technologies can be added later if the project requirements are expanded.

---

## 13. Limitations

The regular-expression approach has several limitations.

### 13.1 Natural language variation

A résumé may describe the same qualification using a phrase that is not included in the controlled vocabulary.

For example:

```text
I have extensive experience building applications with Facebook's JavaScript library.
```

may refer to React without explicitly using the word React.

The regex system will not infer this relationship.

### 13.2 Ambiguous terms

Some qualifications may belong to multiple categories.

For example:

```text
SQL
Python
Git
```

can appear in several professional profiles.

The extraction stage should therefore not assign a profile based only on the presence of a single qualification.

### 13.3 Context

Regular expressions recognize textual patterns but do not fully understand the context in which a term appears.The regex-based extraction approach may produce false positives when a qualification appears in a different semantic context. ResumeLens does not perform semantic analysis or natural-language understanding at this stage, since the objective of this stage is lexical extraction using regular expressions.

For example:

```text
I do not have experience with Python.
```

contains the word:

```text
Python
```

and the regex can extract it even though the candidate explicitly states that they do not have experience with Python.

This limitation should be considered when designing test cases and interpreting the results.

### 13.4 Telephone formats

Telephone numbers have many international representations. The initial phone pattern supports common formats, but it is not intended to represent every possible telephone-number format worldwide.

Additional formats may be added if required by the test cases. Numbers without separators and without country code are intentionally rejected to avoid confusing them with ID numbers.

### 13.5 Candidate name

The name is recognized by its form and position, not by a vocabulary. Therefore:

- If the résumé does not start with the name and has no `Name:` label, the name is not extracted (`None`).
- A first line formed only by capitalized words that are not a name and do not contain a heading word or a job title (for example, `Bogotá Colombia`) could be taken as a name.
- Names with more than 4 words (without counting particles) or written completely in lower case are not recognized.

---

## 14. Summary of the Regex Design

The extraction stage can be summarized as:

```text
                  RÉSUMÉ
                     |
                     v
             Regular Expressions
                     |
       +-------------+-------------+-------------+
       |             |             |             |
       v             v             v             v
     Name        Contact      Qualifications   Experience
                     |
        +------------+------------+
        |            |            |
        v            v            v
    Languages    Frameworks    Databases
        |
        +-------------------------+
                                  |
                                  v
                         Tools / Technologies
                                  |
                                  v
                         Other Qualifications
                                  |
                                  v
                      Structured Extraction
                                  |
                                  v
                       Normalization Stage
```

The central design principle is:

```text
EXTRACT FIRST
     ↓
NORMALIZE SECOND
     ↓
CLASSIFY THIRD
```

The regular-expression module therefore provides the lexical information required by the finite-state transducers and the finite automata in the following stages of ResumeLens.