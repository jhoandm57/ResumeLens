from pathlib import Path

from textx import metamodel_from_file

from src.model.classification.profile_automata import ProfileAutomata
from src.model.extraction.resume_extractor import extract_resume_information
from src.model.grammar.profile_generator import UNKNOWN_NAME, ProfileGenerator
from src.model.normalization.normalized_data import NormalizedData
from src.model.normalization.resume_normalizer import ResumeNormalizer


GRAMMAR = Path(__file__).resolve().parents[2] / "src" / "model" / "grammar" / "resume_lens.tx"
METAMODEL = metamodel_from_file(str(GRAMMAR))

NORMALIZER = ResumeNormalizer()
AUTOMATA = ProfileAutomata()
GENERATOR = ProfileGenerator()

ALL_REJECTED = {
    "FULL_STACK_DEVELOPER": "REJECTED",
    "MACHINE_LEARNING_ENGINEER": "REJECTED",
    "CYBERSECURITY_ENGINEER": "REJECTED",
    "DATA_ENGINEER": "REJECTED",
}


def generate_from_text(text):
    """Stages 1, 2, 3 and the generator of stage 4."""
    normalized = NORMALIZER.normalize(extract_resume_information(text))
    return GENERATOR.generate(normalized, AUTOMATA.classify(normalized))


WEDNESDAY = """
Wednesday Addams
wednesday@mail.com
+57 300 1234567
3 years of experience developing web applications.
Education: B.Sc. in Computer Science.
Technical Skills:
JS, React.js, NodeJS, Postgres, Git.
"""


def test_statement_example_is_generated_exactly():
    expected = '''candidate "Wednesday Addams" {
    contact {
        email wednesday@mail.com
        phone +57 300 1234567
    }
    experience {
        years 3
        entry "3 years of experience"
    }
    education {
        degree BACHELOR
        field COMPUTER_SCIENCE
    }
    skills {
        languages: JAVASCRIPT
        frameworks: REACT, NODE_JS
        databases: POSTGRESQL
        tools: GIT
    }
    classification {
        FULL_STACK_DEVELOPER: ACCEPTED
        MACHINE_LEARNING_ENGINEER: REJECTED
        CYBERSECURITY_ENGINEER: REJECTED
        DATA_ENGINEER: REJECTED
    }
}
'''

    assert generate_from_text(WEDNESDAY) == expected


def test_generated_profile_satisfies_the_grammar():
    model = METAMODEL.model_from_str(generate_from_text(WEDNESDAY))

    assert model.name == "Wednesday Addams"
    assert model.experience.years == 3
    assert [r.result for r in model.classification.results] == [
        "ACCEPTED", "REJECTED", "REJECTED", "REJECTED",
    ]


def test_machine_learning_example_satisfies_the_grammar():
    text = """
    Mary Jane Watson
    2 years of experience developing predictive models and data-processing pipelines.
    Technical Skills:
    Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.
    """

    model = METAMODEL.model_from_str(generate_from_text(text))
    skills = {c.category: c.tokens for c in model.skills.categories}

    # SQL is a language and a database: it appears in both categories.
    assert skills["languages"] == ["PYTHON", "SQL"]
    assert skills["databases"] == ["SQL"]
    assert ("MACHINE_LEARNING_ENGINEER", "ACCEPTED") in [
        (r.profile, r.result) for r in model.classification.results
    ]


def test_several_experience_entries_are_listed():
    normalized = NormalizedData(
        experience_years=5,
        experience_entries=["2 years of experience", "5+ yrs experience"],
    )

    text = GENERATOR.generate(normalized, ALL_REJECTED)
    model = METAMODEL.model_from_str(text)

    assert model.experience.years == 5
    assert [e.text for e in model.experience.entries] == [
        "2 years of experience",
        "5+ yrs experience",
    ]


def test_empty_blocks_are_omitted():
    text = GENERATOR.generate(NormalizedData(name="Peter Parker"), ALL_REJECTED)

    assert "experience" not in text
    assert "education" not in text
    assert "skills" not in text
    assert "contact {" in text            # contact is always present

    model = METAMODEL.model_from_str(text)
    assert model.experience is None
    assert model.skills is None


def test_unknown_name():
    text = GENERATOR.generate(NormalizedData(), ALL_REJECTED)

    assert METAMODEL.model_from_str(text).name == UNKNOWN_NAME


def test_phone_with_line_break_is_written_in_one_line():
    normalized = NormalizedData(name="Clark Kent", phones=["+57\n300 1234567"])

    text = GENERATOR.generate(normalized, ALL_REJECTED)

    assert "phone +57 300 1234567" in text
    assert METAMODEL.model_from_str(text).contact.phones[0].value == "+57 300 1234567"


def test_classification_always_lists_the_four_profiles_in_order():
    text = GENERATOR.generate(NormalizedData(name="Clark Kent"), ALL_REJECTED)
    model = METAMODEL.model_from_str(text)

    assert [r.profile for r in model.classification.results] == [
        "FULL_STACK_DEVELOPER",
        "MACHINE_LEARNING_ENGINEER",
        "CYBERSECURITY_ENGINEER",
        "DATA_ENGINEER",
    ]
