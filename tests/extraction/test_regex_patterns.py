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