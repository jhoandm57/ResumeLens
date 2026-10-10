"""
Complete ResumeLens pipeline (stages 1 to 3).

    text --(regex)--> ExtractedData
         --(FST)----> NormalizedData
         --(DFA)----> ClassificationResult

Stage 4 (candidate profile DSL with textX) will take the
ClassificationResult as input.

Usage (from the root of the project):

    python -m src.model.pipeline path/to/resume.txt
"""

import sys
from pathlib import Path

from src.model.extraction.resume_extractor import extract_resume_information
from src.model.normalization.resume_normalizer import normalize_resume
from src.model.classification.resume_classifier import classify_resume
from src.model.classification.classification_result import ClassificationResult


def run_pipeline(text: str) -> ClassificationResult:
    """
    Run extraction, normalization and classification on a résumé.

    Args:
        text: Complete résumé text.

    Returns:
        ClassificationResult (it also contains the NormalizedData).
    """

    extracted = extract_resume_information(text)
    normalized = normalize_resume(extracted)

    return classify_resume(normalized)


def format_result(result: ClassificationResult) -> str:
    """Readable report of the classification of a résumé."""

    lines = [f"Candidate: {result.normalized.name or '(unknown)'}", ""]

    for profile, decision in result.decisions.items():
        lines.append(f"Profile pattern: {profile}  [{decision.automaton}]")
        lines.append(f"  Sequence: {', '.join(decision.sequence) or 'ε (empty)'}")

        run = "q0" + "".join(
            f" --{symbol}--> {s_to}" for _, symbol, s_to in decision.trace
        )
        lines.append(f"  Run:      {run}")
        lines.append(f"  Output:   {decision.result}")

        if decision.missing_groups:
            lines.append(f"  Missing:  {', '.join(decision.missing_groups)}")

        lines.append("")

    accepted = ", ".join(result.accepted_profiles) or "none"
    lines.append(f"Accepted profiles: {accepted}")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.model.pipeline path/to/resume.txt")
        sys.exit(1)

    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    print(format_result(run_pipeline(text)))


if __name__ == "__main__":
    main()
