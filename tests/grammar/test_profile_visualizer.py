from pathlib import Path

from src.model.grammar.profile_validator import ProfileValidator
from src.visualization.profile_visualizer import ProfileVisualizer


VALIDATOR = ProfileValidator()
VISUALIZER = ProfileVisualizer()
PROFILES = Path(__file__).resolve().parents[2] / "data" / "profiles"


def render_file(name):
    model = VALIDATOR.validate_file(PROFILES / name)
    return VISUALIZER.render(model)


def minimal_profile(name):
    return f"""
    candidate "{name}" {{
        contact {{ }}
        classification {{
            FULL_STACK_DEVELOPER: REJECTED
            MACHINE_LEARNING_ENGINEER: REJECTED
            CYBERSECURITY_ENGINEER: REJECTED
            DATA_ENGINEER: REJECTED
        }}
    }}
    """


# -------------------------------------------------------------------
# Content of the visualization
# -------------------------------------------------------------------

def test_html_is_a_complete_document():
    html = render_file("valid_wednesday_addams.rl")

    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html


def test_html_contains_name_and_contact():
    html = render_file("valid_wednesday_addams.rl")

    assert "<h1>Wednesday Addams</h1>" in html
    assert "wednesday@mail.com" in html
    assert "+57 300 1234567" in html


def test_html_contains_experience_and_education():
    html = render_file("valid_wednesday_addams.rl")

    assert "<strong>3</strong>" in html
    assert "3 years of experience" in html
    assert "Degree: BACHELOR" in html
    assert "Field: COMPUTER_SCIENCE" in html


def test_html_contains_tokens_by_category():
    html = render_file("valid_wednesday_addams.rl")

    for token in ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]:
        assert f'<span class="token">{token}</span>' in html

    assert "Frameworks and libraries" in html
    assert "Databases" in html


def test_html_contains_every_profile_result():
    html = render_file("valid_mary_jane_watson.rl")

    assert html.count('<tr class="accepted">') == 1
    assert html.count('<tr class="rejected">') == 3
    assert (
        '<tr class="accepted"><td>MACHINE_LEARNING_ENGINEER</td>'
        '<td class="result">ACCEPTED</td></tr>'
    ) in html


def test_accepted_profile_is_highlighted():
    html = render_file("valid_wednesday_addams.rl")

    assert '<tr class="accepted"><td>FULL_STACK_DEVELOPER</td>' in html
    assert '<tr class="rejected"><td>DATA_ENGINEER</td>' in html


def test_missing_blocks_are_shown_as_not_reported():
    model = VALIDATOR.validate(minimal_profile("Peter Parker"))
    html = VISUALIZER.render(model)

    assert "<h1>Peter Parker</h1>" in html
    # contact (empty), experience, education and skills
    assert html.count("Not reported") == 4
    assert '<tr class="accepted">' not in html


# -------------------------------------------------------------------
# Escaping of special characters
# -------------------------------------------------------------------

def test_special_characters_in_name_are_escaped():
    model = VALIDATOR.validate(minimal_profile("Tom <b>Admin</b> & Co"))
    html = VISUALIZER.render(model)

    assert "<h1>Tom &lt;b&gt;Admin&lt;/b&gt; &amp; Co</h1>" in html
    assert "<b>Admin</b>" not in html


def test_special_characters_in_experience_are_escaped():
    text = minimal_profile("Peter Parker").replace(
        "contact { }",
        'contact { }\n experience { years 2 entry "2 years <script> & R&D" }',
    )
    html = VISUALIZER.render(VALIDATOR.validate(text))

    assert "2 years &lt;script&gt; &amp; R&amp;D" in html
    assert "<script>" not in html
