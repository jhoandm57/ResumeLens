# ResumeLens – Problem Definition

## 1. Context

When a software company opens a position, it can receive hundreds of resumes. Before any interview, someone has to read each one and check the basics: does the candidate know the languages, frameworks, databases, and tools the role needs? Do they have the right degree or enough years of experience?

Doing this by hand takes a lot of time and is not very consistent. Two recruiters can read the same resume and reach different conclusions, and the same person can be stricter in the morning than at the end of the day.

There is also a more technical problem: resumes are free text. Every candidate organizes the document in their own way and writes technologies however they like. The same skill shows up in many forms:

```text
JavaScript   Javascript   JS
React        React.js     ReactJS
Node.js      NodeJS
PostgreSQL   Postgres
TensorFlow   Tensor Flow
```

A simple keyword search does not work well here. If you search for "JavaScript", you miss the candidate who wrote "JS". To catch everything, the recruiter would need to know in advance every way people write every technology.

---

## 2. Problem Statement

We have a resume in plain text and four professional profiles: Full Stack Developer, Machine Learning Engineer, Cybersecurity Engineer, and Data Engineer. We want to know, automatically and always with the same criterion, whether the qualifications written in the resume satisfy the pattern that each profile requires. We also want a structured summary of the candidate with that result.

We split the problem into four steps, and each one uses a formal language model:

1. **Find the information.** Locate names, contact data, skills, degrees, and experience in the text, no matter the capitalization or spelling. For this we use **regular expressions**.
2. **Unify the variants.** Turn `JS`, `Javascript`, and `JavaScript` into a single token, `JAVASCRIPT`. For this we use **finite-state transducers**.
3. **Check the profiles.** Decide whether the candidate's normalized skills form an accepted pattern for each profile. For this we use **finite automata**, so the decision is formal and can be verified.
4. **Describe the candidate.** Write the result in a small language of our own, check that it is well formed, and show it as a short HTML page. For this we use a **context-free grammar implemented with textX**.

ResumeLens **does not decide who gets hired**. It only helps with the first technical filter, and it does it in a way that anyone can repeat and check.

---

## 3. Objectives

### 3.1 General Objective

Build ResumeLens, a resume-screening tool based on formal languages and automata that extracts, normalizes, and classifies a candidate's technical qualifications against predefined profiles, giving the same answer every time and explaining why.

### 3.2 Specific Objectives

1. Write regular expressions that extract contact data, technical skills, academic degrees, and years of experience from resume text.
2. Build finite-state transducers that convert the extracted skills into canonical tokens.
3. Build one finite automaton per profile that recognizes its accepted qualification patterns.
4. Define a context-free grammar with textX for candidate profiles. It must reject profiles with lexical, syntactic, or semantic errors, and every valid profile must be shown as an HTML page.
5. Offer a command-line entry point (`python -m src.pipeline`) that runs a resume through the four stages and prints what each stage produced.
6. Test each stage on its own with unit tests, and the whole pipeline with end-to-end tests on example resumes.

---

## 4. Scope

### 4.1 In Scope

- Resumes in English, saved as plain-text files (`.txt`), one resume per file. The program can process one file or every `.txt` file in a folder.
- The skills vocabulary we defined for the four profiles.
- Experience written explicitly, like `3 years of experience` or `5+ yrs experience`.
- Differences in capitalization, spacing, and punctuation of the skills we know.
- An `ACCEPTED` / `REJECTED` answer for each profile. The four profiles are checked separately, so one resume can be accepted in several profiles or in none.
- For every resume, two output files: the candidate profile in our language (`.rl`), validated with textX, and its HTML page (`.html`). If the profile is not valid, the program reports the error with its line and column and does not create the HTML.

### 4.2 Out of Scope

- Reading PDF, Word, or image files (no OCR).
- Resumes in languages other than English.
- Calculating experience from dates (for example `2021 – 2024`) or from job descriptions.
- Understanding the meaning of the text, or recognizing skills that are not in our vocabulary.
- A graphical interface. The program runs from the command line, and the HTML page is its visual output.
- Ranking or scoring candidates, or making hiring decisions.
