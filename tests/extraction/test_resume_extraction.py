from src.model.extraction.resume_extractor import extract_resume_information
from src.model.extraction.extracted_data import ExtractedData


def test_extract_resume_information_returns_expected_type():
    resume = "Python developer with 3 years of experience."

    result = extract_resume_information(resume)

    assert isinstance(result, ExtractedData)


def test_extract_resume_information_extracts_all_categories():
    resume = """
    Contact: jhoan@example.com
    Phone: +57 300 123 4567

    Skills: Python, JavaScript, React.js, PostgreSQL, Git, Docker.

    Education: B.Sc. in Computer Science.

    Experience: 3 years of experience in software development.

    Qualifications: REST APIs and Machine Learning.
    """

    result = extract_resume_information(resume)

    assert "jhoan@example.com" in result.emails
    assert len(result.phones) > 0

    assert "Python" in result.programming_languages
    assert "JavaScript" in result.programming_languages

    assert "React.js" in result.frameworks_libraries
    assert "PostgreSQL" in result.databases

    assert "B.Sc." in result.academic_qualifications
    assert "3 years of experience" in result.professional_experience

    assert "Git" in result.tools_technologies
    assert "Docker" in result.tools_technologies

    assert "REST APIs" in result.other_qualifications
    assert "Machine Learning" in result.other_qualifications


def test_empty_resume_returns_empty_lists():
    result = extract_resume_information("")

    assert result.name is None
    assert result.emails == []
    assert result.phones == []
    assert result.programming_languages == []
    assert result.frameworks_libraries == []
    assert result.databases == []
    assert result.academic_qualifications == []
    assert result.professional_experience == []
    assert result.tools_technologies == []
    assert result.other_qualifications == []

def test_extract_name_from_header():
    resume = """
    Wednesday Addams
    3 years of experience developing web applications.
    Technical Skills:
    JS, React.js, NodeJS, Postgres, Git.
    """

    result = extract_resume_information(resume)

    assert result.name == "Wednesday Addams"


def test_label_has_priority_over_header():
    resume = "Curriculum Vitae\nName: Mary   Jane Watson\nPython, SQL"

    result = extract_resume_information(resume)

    # Multiple spaces are reduced to one.
    assert result.name == "Mary Jane Watson"


def test_name_is_none_when_not_found():
    result = extract_resume_information("Python developer with 3 years of experience.")

    assert result.name is None
