# ResumeLens – Regular Expression Extraction Stage

ResumeLens receives a résumé as unstructured text and uses regular expressions implemented with Python's `re` module to identify relevant information such as:

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

---

## 2. Extraction Categories

The regular expression system is divided into several categories. Each category corresponds to a type of information that ResumeLens must be able to identify in a résumé.

### 2.1 Contact Information

This category includes information used to identify communication channels for the candidate.

The initial implementation will support:

- Email addresses
- Telephone numbers

Examples:

```text
mary.watson@email.com
john.smith@gmail.com
+57 300 1234567
300 123 4567
+57-300-1234567
```

### 2.2 Programming Languages

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

### 2.3 Frameworks and Libraries

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

### 2.4 Databases

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

### 2.5 Academic Qualifications

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

### 2.6 Professional Experience

The professional experience category identifies explicit references to years of experience.

Examples include:

```text
2 years of experience
3 years experience
5+ years of experience
2 yrs of experience
4 years of professional experience
```

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

### 2.7 Tools and Technologies

This category contains technologies and tools that are relevant to the four professional profiles but are not necessarily programming languages or frameworks.

The initial vocabulary includes:

```text
Git

Docker
Kubernetes

Nmap

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

### 2.8 Other Relevant Qualifications

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

### 4.1 Email

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

### 4.2 Phone Number

The initial phone-number pattern is:

```python
PHONE_PATTERN = (
    r"(?<!\d)(?:\+?\d{1,3}[\s.-]?)?"
    r"(?:\(?\d{2,4}\)?[\s.-]?)?"
    r"\d{3}[\s.-]?\d{3,4}"
    r"(?:[\s.-]?\d{2,4})?(?!\d)"
)
```

This pattern is designed to support common phone-number representations without restricting the system to a single country.

Examples include:

```text
+57 300 1234567
+57-300-1234567
300 123 4567
300-123-4567
```

#### Important components

```regex
\+?
```

allows an optional `+`.

Therefore both:

```text
+57
```

and:

```text
57
```

can be recognized.

The expression:

```regex
\d
```

represents a digit from 0 to 9.

The expression:

```regex
\d{3}
```

means exactly three digits.

The expression:

```regex
[\s.-]?
```

allows an optional separator such as:

```text
space
.
-
```

The negative lookarounds:

```regex
(?<!\d)
(?!\d)
```

help prevent the expression from extracting only part of a larger sequence of digits.

Because telephone numbers have many international formats, this pattern should be validated with test cases and may be extended if additional formats are required.

### 4.3 Programming Languages

The initial pattern is:

```python
PROGRAMMING_LANGUAGES_PATTERN = (
    r"\b(?:JavaScript|Javascript|TypeScript|Python|SQL|Bash)\b"
    r"|(?<![\w.])JS(?!\w)"
)
```

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

### 4.4 Frameworks and Libraries

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
Scikit[-\s]?learn|sklearn
```

recognizes:

```text
Scikit-learn
Scikit learn
Scikitlearn
sklearn
```

`sklearn` is included as a separate alternative because it is the name used to import the library in Python (`import sklearn`), and it is commonly written in résumés.

The part:

```regex
[-\s]?
```

allows:

- a hyphen,
- whitespace,
- or no separator.

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

### 4.5 Databases

The initial database pattern is:

```python
DATABASES_PATTERN = (
    r"\b(?:PostgreSQL|Postgres|SQL|NoSQL)\b"
)
```

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

### 4.6 Academic Qualifications

The initial academic qualification pattern is:

```python
ACADEMIC_QUALIFICATIONS_PATTERN = (
    r"(?:"
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

### 4.7 Professional Experience

The initial experience pattern is:

```python
EXPERIENCE_PATTERN = (
    r"\b\d+\+?\s*(?:years?|yrs?)"
    r"(?:\s+of)?\s+experience\b"
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

The pattern intentionally focuses on explicit mentions of experience.

### 4.8 Tools and Technologies

The initial pattern is:

```python
TOOLS_TECHNOLOGIES_PATTERN = (
    r"\b(?:"
    r"Git"
    r"|Docker"
    r"|Kubernetes"
    r"|Nmap"
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

### 4.9 Other Relevant Qualifications

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

### 4.10 Formal Definition of the Recognized Languages

Each regular expression of the extraction stage denotes a **regular language**: the set of strings that the expression accepts. This section describes, for each pattern, the language it recognizes, together with examples of strings that belong and do not belong to it.

#### Notation

```text
Σ        Alphabet: the set of characters that can appear in résumé text.
Letter   {a, ..., z, A, ..., Z}
Digit    {0, ..., 9}
WS       Whitespace characters {space, tab, newline, ...}
ε        Empty string

X ∪ Y    Union          (regex: X|Y)
X · Y    Concatenation  (regex: XY)
X*       Kleene star: zero or more repetitions
X⁺       One or more repetitions (X · X*)
X?       Optional: X ∪ {ε}
X^{m,n}  Between m and n repetitions

[w]      All case variants of the word w, because matching uses re.IGNORECASE.
         Example: [Git] = {git, Git, GIT, gIT, ...}
```

Since every language below is built from finite sets using only union, concatenation, and Kleene closure, all of them are regular. Therefore, each one could also be recognized by a finite automaton.

The word boundaries (`\b`) and lookarounds (`(?<!...)`, `(?!...)`) do not add new strings to the language. They only restrict **the context** in which a string is accepted inside the résumé text. For example, `Git` is not extracted from `GitHub`.

#### 4.10.1 Email

```text
A = Letter ∪ Digit ∪ {., _, %, +, -}
B = Letter ∪ Digit ∪ {., -}

L_EMAIL = A⁺ · {@} · B⁺ · {.} · Letter^{2,}
```

An email is a non-empty local part, the symbol `@`, a non-empty domain, a dot, and an extension of at least two letters.

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `mary.watson@email.com` | `mary.watson@` | Missing domain |
| `peter_parker@company.co` | `@gmail.com` | Empty local part |
| `john.smith@gmail.com` | `user@domain.c` | Extension with fewer than 2 letters |

#### 4.10.2 Phone Number

```text
Sep = WS ∪ {., -}

Country = ({+} ∪ {ε}) · Digit^{1,3} · Sep?
Area    = ({(} ∪ {ε}) · Digit^{2,4} · ({)} ∪ {ε}) · Sep?
Number  = Digit^{3} · Sep? · Digit^{3,4} · (Sep? · Digit^{2,4})?

L_PHONE = Country? · Area? · Number
```

In addition, the match cannot be immediately preceded or followed by another digit.

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `+57 300 1234567` | `12345` | Fewer than 6 digits in the main number |
| `300 123 4567` | `123` | Too short |
| `+57-300-1234567` | | |

**Known limitation:** the language is broad, so strings that are not phone numbers, such as the year range `2001-2004`, also belong to `L_PHONE` (see Section 13.4).

#### 4.10.3 Programming Languages

```text
L_LANG = [JavaScript] ∪ [TypeScript] ∪ [Python] ∪ [SQL] ∪ [Bash] ∪ [JS]
```

This is a **finite language** (up to case variants). `Javascript` is already included in `[JavaScript]`.

Context restrictions:

- Words must be complete: `\b` on both sides.
- `JS` cannot be preceded by a letter, digit, `_`, or `.`, so it is not extracted from `React.js`, `Node.js`, or `Next.js`.

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `JS` | `js` inside `React.js` | Preceded by `.` |
| `python` | `Pythonic` | Not a complete word |
| `TypeScript` | `Java` | Not in the vocabulary |

#### 4.10.4 Frameworks and Libraries

```text
L_FW = [React] · ({.js} ∪ {JS} ∪ {ε})
     ∪ [Angular] ∪ [Vue] ∪ [Django] ∪ [Pandas] ∪ [NumPy]
     ∪ [Node] · ({.js} ∪ {JS})
     ∪ [Spring] · WS⁺ · [Boot]
     ∪ [Scikit] · ({-} ∪ WS ∪ {ε}) · [learn]
     ∪ [sklearn]
     ∪ [Tensor] · WS* · [Flow]
     ∪ [Py] · WS* · [Torch]
     ∪ ([Apache] · WS⁺)? · [Spark]
     ∪ ([Apache] · WS⁺)? · [Airflow]
```

Because of `WS⁺` and `WS*`, this language is **infinite**: `Spring Boot`, `Spring  Boot`, and `Spring   Boot` are all different strings of the language.

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `React.js`, `ReactJS`, `React` | `Node` | The `.js` / `JS` suffix is mandatory |
| `NodeJS`, `Node.js` | `Vuex` | Not a complete word |
| `Scikit-learn`, `Scikitlearn`, `sklearn` | `Flask` | Not in the vocabulary |
| `Tensor Flow`, `PyTorch` | | |

#### 4.10.5 Databases

```text
L_DB = [PostgreSQL] ∪ [Postgres] ∪ [NoSQL] ∪ [SQL]
```

This is a finite language. `PostgreSQL` is placed before `Postgres` in the pattern so that the longest form is extracted.

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `PostgreSQL` | `MySQL` | `SQL` is not a complete word inside `MySQL` |
| `Postgres` | `MongoDB` | Not in the vocabulary |
| `NoSQL` | | |

#### 4.10.6 Academic Qualifications

```text
Apos = {', ’}

L_ACAD = [Bachelor] · (Apos · [s])?
       ∪ [B] · {.}? · [Sc] · {.}?
       ∪ [Master] · (Apos · [s])?
       ∪ [M] · {.}? · [Sc] · {.}?
       ∪ [Ph] · {.}? · [D] · {.}?
       ∪ [Computer] · WS⁺ · [Science]
       ∪ [Software] · WS⁺ · [Engineering]
       ∪ [Systems] · WS⁺ · [Engineering]
       ∪ [Data] · WS⁺ · [Science]
```

Context restriction: the match cannot be followed by a letter, digit, or `_` (`(?!\w)`). A final `\b` is not used because forms such as `Ph.D.` and `B.Sc.` end with a period.

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `Bachelor's`, `Bachelor’s` | `Masters` | Followed by a letter without an apostrophe |
| `B.Sc.`, `BSc` | `Bachelors` | Followed by a letter without an apostrophe |
| `Ph.D.`, `PhD` | | |
| `Data Science` | | |

#### 4.10.7 Professional Experience

```text
L_EXP = Digit⁺ · {+}? · WS* · ([year] ∪ [years] ∪ [yr] ∪ [yrs])
        · (WS⁺ · [of])? · WS⁺ · [experience]
```

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `3 years of experience` | `years of experience` | Missing number |
| `5+ yrs experience` | `three years of experience` | The number is written in words |
| `2 yrs of experience` | `4 years of professional experience` | An extra word appears before `experience` |

#### 4.10.8 Tools and Technologies

```text
L_TOOLS = [Git] ∪ [Docker] ∪ [Kubernetes] ∪ [Nmap]
        ∪ [TCP] · WS* · {/}? · WS* · [IP]
        ∪ [Networking] ∪ [Network]
        ∪ [ETL] ∪ [ELT]
        ∪ [Data] · WS⁺ · [Pipeline] · [s]?
        ∪ [Data] · WS⁺ · [Warehousing]
        ∪ [Data] · WS⁺ · [Warehouse]
```

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `Git` | `GitHub` | Not a complete word |
| `TCP/IP`, `TCP / IP`, `TCP IP` | `Jenkins` | Not in the vocabulary |
| `Data Pipelines` | | |

#### 4.10.9 Other Relevant Qualifications

```text
MLSep = {-} ∪ WS

L_OTHER = [Machine] · MLSep · [Learning] · WS⁺ · [Model] · WS⁺ · [Development]
        ∪ [REST] · WS⁺ · [API] · [s]?
        ∪ [Machine] · MLSep · [Learning]
        ∪ [Vulnerability] · WS⁺ · [Assessment]
        ∪ [Cyber] · WS* · [Security]
        ∪ [Security] · WS⁺ · [Automation]
```

`Cybersecurity` already belongs to `[Cyber] · WS* · [Security]` (with zero spaces).

| Accepted | Rejected | Reason for rejection |
| :--- | :--- | :--- |
| `Machine-Learning Model Development` | `ML` | Abbreviation not in the vocabulary |
| `REST API`, `REST APIs` | `RESTful` | Not a complete word |
| `Cyber Security`, `Cybersecurity` | | |

#### 4.10.10 Language of the Complete Extraction Stage

The set of all qualifications that the extraction stage can recognize is the union of the previous languages:

```text
L_EXTRACTION = L_LANG ∪ L_FW ∪ L_DB ∪ L_ACAD ∪ L_EXP ∪ L_TOOLS ∪ L_OTHER
```

Since regular languages are closed under union, `L_EXTRACTION` is also regular. Contact information (`L_EMAIL` and `L_PHONE`) is extracted separately because it identifies the candidate but is not a qualification.

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
sklearn
```

Later normalization:

```text
Scikit-learn
Scikit learn
Scikitlearn
sklearn
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

This file defines the structure used to represent the extracted information.

The structure will contain:

```text
ExtractedResume
│
├── contact
│   ├── emails
│   └── phones
│
├── programming_languages
│
├── frameworks_libraries
│
├── databases
│
├── academic_qualifications
│
├── professional_experience
│
├── tools_technologies
│
└── other_qualifications
```

A conceptual example is:

```python
{
    "contact": {
        "emails": ["mary.watson@email.com"],
        "phones": ["+57 300 1234567"]
    },
    "programming_languages": [
        "Python",
        "SQL"
    ],
    "frameworks_libraries": [
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow"
    ],
    "databases": [
        "PostgreSQL"
    ],
    "academic_qualifications": [],
    "professional_experience": [
        "2 years of experience"
    ],
    "tools_technologies": [
        "Git"
    ],
    "other_qualifications": []
}
```

The exact Python implementation of this structure will be defined when the extraction module is implemented.

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

Tools/Technologies:
    Git
```

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

Additional formats may be added if required by the test cases.

---

## 14. Summary of the Regex Design

The extraction stage can be summarized as:

```text
                  RÉSUMÉ
                     |
                     v
             Regular Expressions
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
   Contact      Qualifications   Experience
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