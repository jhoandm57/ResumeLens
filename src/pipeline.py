"""
ResumeLens pipeline: entry point of the application.

A résumé in plain text goes through all the stages of ResumeLens:

    1. Extraction       (regular expressions)        -> ExtractedData
    2. Normalization    (finite-state transducers)   -> NormalizedData
    3. Classification   (finite automata)            -> ACCEPTED / REJECTED
    4. Candidate profile (context-free grammar, textX):
         generator  -> DSL text (.rl)
         validator  -> textX model
         visualizer -> HTML page (.html)

Usage (from the root of the project):

    python -m src.pipeline data/resumes/wednesday_addams.txt
    python -m src.pipeline data/resumes            (every .txt of the folder)
    python -m src.pipeline data/resumes -o other/output/folder

For each résumé the console shows a summary of every stage, and two
files are written in the output folder (data/output by default):

    <name>.rl    profile written in the candidate profile language
    <name>.html  visualization of the candidate

If the generated profile does not satisfy the grammar, the error is shown
with its line and column and the HTML is not generated.
"""

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

from textx.exceptions import TextXError

from src.model.classification.profile_automata import ACCEPTED, ProfileAutomata
from src.model.extraction.extracted_data import ExtractedData
from src.model.extraction.resume_extractor import extract_resume_information
from src.model.grammar.profile_generator import ProfileGenerator
from src.model.grammar.profile_validator import ProfileValidator
from src.model.normalization.normalized_data import NormalizedData
from src.model.normalization.resume_normalizer import ResumeNormalizer
from src.visualization.profile_visualizer import ProfileVisualizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "output"


@dataclass
class PipelineResult:
    """
    Result of processing one résumé with every stage.
    """

    source: Path
    extracted: ExtractedData
    normalized: NormalizedData
    classification: dict[str, str]
    profile_text: str
    rl_path: Path
    html_path: Path | None = None
    # Message of the textX error, or None if the profile is valid.
    error: str | None = None
    accepted: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return self.error is None


class ResumePipeline:
    """
    Runs the four stages of ResumeLens on résumés in plain text.

    The transducers, the automata and the grammar are built only once,
    so several résumés can be processed with the same object.
    """

    def __init__(self, output_dir: str | Path = DEFAULT_OUTPUT):
        self.output_dir = Path(output_dir)
        self.normalizer = ResumeNormalizer()
        self.automata = ProfileAutomata()
        self.generator = ProfileGenerator()
        self.validator = ProfileValidator()
        self.visualizer = ProfileVisualizer()

    def process_text(self, text: str, name: str, source: Path | None = None) -> PipelineResult:
        """
        Run every stage on the text of a résumé.

        Args:
            text: Complete text of the résumé.
            name: Base name of the output files (<name>.rl, <name>.html).
            source: File the text comes from (only informative).

        Returns:
            PipelineResult with the output of every stage.
        """

        # Stage 1: extraction (regular expressions)
        extracted = extract_resume_information(text)

        # Stage 2: normalization (finite-state transducers)
        normalized = self.normalizer.normalize(extracted)

        # Stage 3: classification (finite automata)
        classification = self.automata.classify(normalized)

        # Stage 4: candidate profile (textX)
        profile_text = self.generator.generate(normalized, classification)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        rl_path = self.output_dir / f"{name}.rl"
        rl_path.write_text(profile_text, encoding="utf-8")

        result = PipelineResult(
            source=source or Path(name),
            extracted=extracted,
            normalized=normalized,
            classification=classification,
            profile_text=profile_text,
            rl_path=rl_path,
            accepted=[p for p, r in classification.items() if r == ACCEPTED],
        )

        html_path = self.output_dir / f"{name}.html"

        try:
            model = self.validator.validate(profile_text)
        except TextXError as error:
            result.error = _describe_error(error)
            # An HTML of a previous run would no longer match this profile.
            html_path.unlink(missing_ok=True)
            return result

        html_path.write_text(self.visualizer.render(model), encoding="utf-8")
        result.html_path = html_path

        return result

    def process_file(self, path: str | Path) -> PipelineResult:
        """Run every stage on a résumé stored in a .txt file."""

        path = Path(path)
        text = path.read_text(encoding="utf-8")

        return self.process_text(text, path.stem, source=path)


def _describe_error(error: TextXError) -> str:
    return f"{type(error).__name__} (line {error.line}, column {error.col}): {error.message}"


def _join(values) -> str:
    return ", ".join(str(v) for v in values) if values else "-"


def print_summary(result: PipelineResult) -> None:
    """Show in the console the result of every stage of one résumé."""

    e = result.extracted
    n = result.normalized

    print("=" * 70)
    print(f"Resume: {result.source}")
    print("=" * 70)

    print("\n[Stage 1] Extraction (regular expressions)")
    print(f"  Name ........... {e.name or '-'}")
    print(f"  Emails ......... {_join(e.emails)}")
    print(f"  Phones ......... {_join(e.phones)}")
    print(f"  Languages ...... {_join(e.programming_languages)}")
    print(f"  Frameworks ..... {_join(e.frameworks_libraries)}")
    print(f"  Databases ...... {_join(e.databases)}")
    print(f"  Tools .......... {_join(e.tools_technologies)}")
    print(f"  Other .......... {_join(e.other_qualifications)}")
    print(f"  Academic ....... {_join(e.academic_qualifications)}")
    print(f"  Experience ..... {_join(e.professional_experience)}")

    print("\n[Stage 2] Normalization (finite-state transducers)")
    print(f"  Tokens ......... {_join(n.qualifications)}")
    print(f"  Academic ....... {_join(n.academic_qualifications)}")
    print(f"  Years .......... {n.experience_years if n.experience_years is not None else '-'}")

    print("\n[Stage 3] Classification (finite automata)")
    for profile, outcome in result.classification.items():
        sequence = n.profile_sequences.get(profile, [])
        print(f"  {profile:<26} {outcome:<9} <- {_join(sequence)}")

    print("\n[Stage 4] Candidate profile (textX)")
    print(f"  Profile ........ {result.rl_path}")

    if result.valid:
        print("  Validation ..... VALID")
        print(f"  Visualization .. {result.html_path}")
    else:
        print("  Validation ..... INVALID")
        print(f"  Error .......... {result.error}")
        print("  Visualization .. not generated")

    print()



def find_resumes(path: Path) -> list[Path]:
    """A single .txt file, or every .txt file of a folder (sorted)."""

    if path.is_dir():
        return sorted(path.glob("*.txt"))

    return [path]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.pipeline",
        description="ResumeLens: process plain-text resumes through every stage.",
    )
    parser.add_argument("path", type=Path, help="a .txt resume or a folder with .txt resumes")
    parser.add_argument(
        "-o", "--output", type=Path, default=DEFAULT_OUTPUT,
        help="folder for the .rl and .html files (default: data/output)",
    )
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"Error: {args.path} does not exist")
        return 1

    resumes = find_resumes(args.path)

    if not resumes:
        print(f"Error: there are no .txt files in {args.path}")
        return 1

    pipeline = ResumePipeline(args.output)
    results = []

    for resume in resumes:
        result = pipeline.process_file(resume)
        print_summary(result)
        results.append(result)

    valid = sum(r.valid for r in results)
    print(f"Processed: {len(results)}  |  valid profiles: {valid}  |  invalid: {len(results) - valid}")

    return 0 if valid == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
