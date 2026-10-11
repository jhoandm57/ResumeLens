"""
End-to-end tests of ResumeLens.

Every résumé of data/resumes/ goes through the complete pipeline
(extraction -> normalization -> classification -> generator ->
validator -> visualizer), and the result is compared with the expected
result stored in data/expected/<name>.json:

    {
      "resume": "wednesday_addams.txt",
      "name": "Wednesday Addams",
      "profiles": {
        "FULL_STACK_DEVELOPER": {
          "sequence": ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
          "result": "ACCEPTED"
        },
        ...
      }
    }

Each résumé is a scenario of the test design (docs/09_test_design.md).
"""

import json
from pathlib import Path

import pytest

from src.pipeline import ResumePipeline


ROOT = Path(__file__).resolve().parents[1]
RESUMES = ROOT / "data" / "resumes"
EXPECTED = ROOT / "data" / "expected"

RESUME_FILES = sorted(RESUMES.glob("*.txt"))


def load_expected(resume: Path) -> dict:
    return json.loads((EXPECTED / f"{resume.stem}.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def pipeline(tmp_path_factory):
    # The transducers, automata and grammar are built only once.
    # The output files go to a temporary folder, not to data/output.
    return ResumePipeline(tmp_path_factory.mktemp("output"))


# -------------------------------------------------------------------
# Consistency of the example data
# -------------------------------------------------------------------

def test_there_are_example_resumes():
    assert len(RESUME_FILES) >= 4


def test_every_resume_has_an_expected_result_and_vice_versa():
    resumes = {path.stem for path in RESUME_FILES}
    expected = {path.stem for path in EXPECTED.glob("*.json")}

    assert resumes == expected


# -------------------------------------------------------------------
# Complete pipeline, one scenario per résumé
# -------------------------------------------------------------------

@pytest.mark.parametrize("resume", RESUME_FILES, ids=lambda path: path.stem)
def test_resume_classification_matches_expected(pipeline, resume):
    expected = load_expected(resume)
    result = pipeline.process_file(resume)

    assert result.extracted.name == expected["name"]

    for profile, data in expected["profiles"].items():
        # Stage 2: sorted sequence of the profile (input of the automaton)
        assert result.normalized.profile_sequences[profile] == data["sequence"], profile
        # Stage 3: result of the automaton
        assert result.classification[profile] == data["result"], profile


@pytest.mark.parametrize("resume", RESUME_FILES, ids=lambda path: path.stem)
def test_generated_profile_is_valid_and_visualized(pipeline, resume):
    expected = load_expected(resume)
    result = pipeline.process_file(resume)

    # Stage 4: the generated profile satisfies the grammar (textX)
    assert result.valid, result.error
    assert result.rl_path.exists()

    # The visualization was generated with the name and the results
    html = result.html_path.read_text(encoding="utf-8")
    assert f"<h1>{expected['name']}</h1>" in html

    for profile, data in expected["profiles"].items():
        css = "accepted" if data["result"] == "ACCEPTED" else "rejected"
        assert f'<tr class="{css}"><td>{profile}</td>' in html


# -------------------------------------------------------------------
# Summary of the scenarios (the profiles each résumé must satisfy)
# -------------------------------------------------------------------

ACCEPTED_PROFILES = {
    "wednesday_addams": ["FULL_STACK_DEVELOPER"],
    "mary_jane_watson": ["MACHINE_LEARNING_ENGINEER"],
    "peter_parker": ["CYBERSECURITY_ENGINEER"],
    "clark_kent": ["DATA_ENGINEER"],
    "tony_stark": ["MACHINE_LEARNING_ENGINEER", "DATA_ENGINEER"],    # two profiles
    "bruce_wayne": [],                                                # no profile
}


@pytest.mark.parametrize("name, accepted", ACCEPTED_PROFILES.items())
def test_scenarios(pipeline, name, accepted):
    result = pipeline.process_file(RESUMES / f"{name}.txt")

    assert result.accepted == accepted
