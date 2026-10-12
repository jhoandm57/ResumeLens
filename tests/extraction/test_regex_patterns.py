import re

from src.model.extraction.regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    PROGRAMMING_LANGUAGES_PATTERN,
    FRAMEWORKS_LIBRARIES_PATTERN,
    DATABASES_PATTERN,
    ACADEMIC_QUALIFICATIONS_PATTERN,
    EXPERIENCE_PATTERN,
    TOOLS_TECHNOLOGIES_PATTERN,
    OTHER_QUALIFICATIONS_PATTERN,
)


def find_matches(pattern, text):
    return re.findall(pattern, text, flags=re.IGNORECASE)


def test_email_pattern():
    text = "Contact: jhoan@example.com and dev.user@company.co"

    result = find_matches(EMAIL_PATTERN, text)

    assert result == [
        "jhoan@example.com",
        "dev.user@company.co",
    ]


def test_phone_pattern():
    text = "Phone: +57 300 123 4567"

    result = find_matches(PHONE_PATTERN, text)

    assert any("300" in phone for phone in result)


def test_programming_languages_pattern():
    text = "Python, JavaScript, JS, TypeScript and Bash"

    result = find_matches(PROGRAMMING_LANGUAGES_PATTERN, text)

    assert result == [
        "Python",
        "JavaScript",
        "JS",
        "TypeScript",
        "Bash",
    ]


def test_js_does_not_match_inside_file_names():
    text = "I use React.js, Node.js and app.js"

    result = find_matches(PROGRAMMING_LANGUAGES_PATTERN, text)

    assert "JS" not in result


def test_frameworks_and_libraries_pattern():
    text = (
        "React.js, NodeJS, Django, Pandas, "
        "Scikit-learn, Tensor Flow and PyTorch"
    )

    result = find_matches(FRAMEWORKS_LIBRARIES_PATTERN, text)

    assert result == [
        "React.js",
        "NodeJS",
        "Django",
        "Pandas",
        "Scikit-learn",
        "Tensor Flow",
        "PyTorch",
    ]


def test_databases_pattern():
    text = "Experience with PostgreSQL, Postgres, SQL and NoSQL"

    result = find_matches(DATABASES_PATTERN, text)

    assert result == [
        "PostgreSQL",
        "Postgres",
        "SQL",
        "NoSQL",
    ]


def test_academic_qualifications_pattern():
    text = (
        "B.Sc. in Computer Science, "
        "Master's in Data Science and Ph.D."
    )

    result = find_matches(ACADEMIC_QUALIFICATIONS_PATTERN, text)

    assert result == [
        "B.Sc.",
        "Computer Science",
        "Master's",
        "Data Science",
        "Ph.D.",
    ]


def test_experience_pattern():
    text = "I have 3 years of experience in software development"

    result = find_matches(EXPERIENCE_PATTERN, text)

    assert result == ["3 years of experience"]


def test_tools_and_technologies_pattern():
    text = "Git, Docker, Kubernetes, Nmap, TCP/IP and ETL"

    result = find_matches(TOOLS_TECHNOLOGIES_PATTERN, text)

    assert result == [
        "Git",
        "Docker",
        "Kubernetes",
        "Nmap",
        "TCP/IP",
        "ETL",
    ]


def test_other_qualifications_pattern():
    text = (
        "Machine Learning Model Development, REST APIs, "
        "Vulnerability Assessment and Cybersecurity"
    )

    result = find_matches(OTHER_QUALIFICATIONS_PATTERN, text)

    assert result == [
        "Machine Learning Model Development",
        "REST APIs",
        "Vulnerability Assessment",
        "Cybersecurity",
    ]


def test_phone_pattern_formats():
    text = "+57 300 1234567, 300 123 4567, +57-300-1234567 and (300) 123-4567"

    result = find_matches(PHONE_PATTERN, text)

    assert result == [
        "+57 300 1234567",
        "300 123 4567",
        "+57-300-1234567",
        "(300) 123-4567",
    ]


def test_phone_pattern_ignores_years_and_ids():
    text = "Worked 2001-2004. ID 1234567890. Born 2001-10-09."

    result = find_matches(PHONE_PATTERN, text)

    assert result == []


def test_sklearn_is_extracted():
    text = "Python, sklearn and Pandas"

    result = find_matches(FRAMEWORKS_LIBRARIES_PATTERN, text)

    assert result == ["sklearn", "Pandas"]


def test_academic_pattern_ignores_words_containing_degrees():
    text = "Webmaster and Headmaster"

    result = find_matches(ACADEMIC_QUALIFICATIONS_PATTERN, text)

    assert result == []


def test_experience_pattern_with_professional():
    text = "4 years of professional experience and 5+ yrs experience"

    result = find_matches(EXPERIENCE_PATTERN, text)

    assert result == [
        "4 years of professional experience",
        "5+ yrs experience",
    ]


def test_experience_pattern_ignores_partial_numbers():
    text = (
        "1.5 years of experience, 10-15 years of experience "
        "and 10 - 15 years of experience"
    )

    result = find_matches(EXPERIENCE_PATTERN, text)

    assert result == []


def test_linux_is_extracted():
    text = "Python, Linux and Docker"

    result = find_matches(TOOLS_TECHNOLOGIES_PATTERN, text)

    assert result == ["Linux", "Docker"]


# -------------------------------------------------------------------
# Candidate name
# -------------------------------------------------------------------

from src.model.extraction.regex_patterns import (  # noqa: E402
    NAME_LABEL_PATTERN,
    NAME_HEADER_PATTERN,
)


def find_name(pattern, text):
    # The name patterns are NOT case-insensitive.
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else None


def test_name_header_examples_from_statement():
    assert find_name(NAME_HEADER_PATTERN, "Wednesday Addams\n3 years of experience") == "Wednesday Addams"
    assert find_name(NAME_HEADER_PATTERN, "Mary Jane Watson\nTechnical Skills:") == "Mary Jane Watson"


def test_name_header_skips_blank_lines_and_indentation():
    text = "\n\n    Peter Parker\n    peter@mail.com"

    assert find_name(NAME_HEADER_PATTERN, text) == "Peter Parker"


def test_name_header_supports_accents_particles_and_capitals():
    assert find_name(NAME_HEADER_PATTERN, "María José Gómez\n") == "María José Gómez"
    assert find_name(NAME_HEADER_PATTERN, "Juan de la Cruz\n") == "Juan de la Cruz"
    assert find_name(NAME_HEADER_PATTERN, "Shaun O'Connor\n") == "Shaun O'Connor"
    assert find_name(NAME_HEADER_PATTERN, "CLARK KENT\n") == "CLARK KENT"


def test_name_header_only_reads_the_first_line():
    # The name is not in the first non-empty line.
    text = "3 years of experience\nWednesday Addams"

    assert find_name(NAME_HEADER_PATTERN, text) is None


def test_name_header_rejects_headings_and_job_titles():
    assert find_name(NAME_HEADER_PATTERN, "Technical Skills\nPython") is None
    assert find_name(NAME_HEADER_PATTERN, "Technical Skills:\nPython") is None
    assert find_name(NAME_HEADER_PATTERN, "Curriculum Vitae\n") is None
    assert find_name(NAME_HEADER_PATTERN, "Python Developer\n") is None
    assert find_name(NAME_HEADER_PATTERN, "Senior Data Engineer\n") is None
    assert find_name(NAME_HEADER_PATTERN, "JS, React.js, NodeJS\n") is None
    assert find_name(NAME_HEADER_PATTERN, "Wednesday\n") is None
    assert find_name(NAME_HEADER_PATTERN, "wednesday addams\n") is None


def test_name_label():
    text = "Contact\nName: Wednesday Addams\nEmail: w@mail.com"

    assert find_name(NAME_LABEL_PATTERN, text) == "Wednesday Addams"
    assert find_name(NAME_LABEL_PATTERN, "FULL NAME:  Mary Jane Watson") == "Mary Jane Watson"
    assert find_name(NAME_LABEL_PATTERN, "Name: python developer") is None
