"""
ResumeLens web application (Streamlit).

The user enters a résumé in plain text (uploading a .txt file, pasting
the text, or choosing one of the example résumés) and the application
runs the four stages of ResumeLens and shows the HTML visualization of
the candidate.

It reuses ResumePipeline (src/pipeline.py), so the web application and
the command line run exactly the same stages:

    1. Extraction       (regular expressions)
    2. Normalization    (finite-state transducers)
    3. Classification   (finite automata)
    4. Candidate profile (context-free grammar with textX) -> HTML

Run locally (from the root of the project):

    streamlit run streamlit_app.py
"""

import re
import tempfile
import uuid
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from src.pipeline import PipelineResult, ResumePipeline


PROJECT_ROOT = Path(__file__).resolve().parent
EXAMPLES_DIR = PROJECT_ROOT / "data" / "resumes"

UPLOAD = "Upload a .txt file"
PASTE = "Paste the text"
EXAMPLE = "Use an example résumé"


# -------------------------------------------------------------------
# ResumeLens
# -------------------------------------------------------------------

@st.cache_resource
def get_pipeline() -> ResumePipeline:
    """
    Build the pipeline only once (transducers, automata and grammar).

    The .rl and .html files of the pipeline are written in a temporary
    folder: the web application shows them on the page.
    """

    output_dir = Path(tempfile.mkdtemp(prefix="resumelens_"))

    return ResumePipeline(output_dir)


def analyze(text: str, name: str) -> PipelineResult:
    """Run the four stages of ResumeLens on the text of a résumé."""

    # A unique suffix keeps the files of different users (or runs) apart.
    unique_name = f"{_safe_name(name)}_{uuid.uuid4().hex[:8]}"

    return get_pipeline().process_text(text, unique_name)


def _safe_name(name: str) -> str:
    """Base name of the output files (letters, digits, '_' and '-')."""

    name = re.sub(r"[^A-Za-z0-9_-]+", "_", Path(name).stem).strip("_")

    return name or "resume"


def _decode(data: bytes) -> str:
    """Text of an uploaded file (UTF-8, or Latin-1 if it is not UTF-8)."""

    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def _examples() -> dict[str, Path]:
    """Example résumés of data/resumes, by file name."""

    return {path.name: path for path in sorted(EXAMPLES_DIR.glob("*.txt"))}


# -------------------------------------------------------------------
# Page
# -------------------------------------------------------------------

def read_input() -> tuple[str, str]:
    """
    Show the input options and return (text of the résumé, name).

    The text is empty if the user has not entered a résumé yet.
    """

    source = st.radio("How do you want to enter the résumé?", [UPLOAD, PASTE, EXAMPLE], horizontal=True)

    if source == UPLOAD:
        file = st.file_uploader("Résumé in plain text (.txt, in English)", type=["txt"])
        if file is None:
            return "", ""
        return _decode(file.getvalue()), file.name

    if source == PASTE:
        text = st.text_area(
            "Résumé text",
            height=260,
            placeholder="Wednesday Addams\n3 years of experience developing web applications.\n"
                        "Technical Skills:\nJS, React.js, NodeJS, Postgres, Git.",
        )
        return text, "pasted_resume"

    examples = _examples()

    if not examples:
        st.warning("There are no example résumés in data/resumes.")
        return "", ""

    choice = st.selectbox("Example résumé", list(examples))
    text = examples[choice].read_text(encoding="utf-8")

    with st.expander("Show the text of the example"):
        st.text(text)

    return text, choice


def show_result(result: PipelineResult, name: str) -> None:
    """Show the result of ResumeLens: summary, HTML, downloads and stages."""

    st.subheader(f"Result for: {name}")

    if result.accepted:
        st.success("Accepted profiles: " + ", ".join(result.accepted))
    else:
        st.info("The résumé does not satisfy the pattern of any profile.")

    base = _safe_name(name)

    if result.valid:
        html = result.html_path.read_text(encoding="utf-8")

        left, right = st.columns(2)
        left.download_button("Download HTML", html, file_name=f"{base}.html", mime="text/html")
        right.download_button("Download profile (.rl)", result.profile_text,
                              file_name=f"{base}.rl", mime="text/plain")

        components.html(html, height=1050, scrolling=True)
    else:
        st.error(
            "The generated candidate profile does not satisfy the grammar, "
            "so the visualization was not generated.\n\n"
            f"{result.error}"
        )
        st.download_button("Download profile (.rl)", result.profile_text,
                           file_name=f"{base}.rl", mime="text/plain")

    st.divider()
    st.subheader("What each stage produced")

    show_stage_1(result)
    show_stage_2(result)
    show_stage_3(result)
    show_stage_4(result)


# -------------------------------------------------------------------
# Detail of each stage
# -------------------------------------------------------------------

def _join(values) -> str:
    return ", ".join(str(v) for v in values) if values else "—"


def show_stage_1(result: PipelineResult) -> None:
    """Values extracted by the regular expressions, as written in the résumé."""

    e = result.extracted
    rows = [
        ("Name", e.name or "—"),
        ("Emails", _join(e.emails)),
        ("Phones", _join(e.phones)),
        ("Programming languages", _join(e.programming_languages)),
        ("Frameworks and libraries", _join(e.frameworks_libraries)),
        ("Databases", _join(e.databases)),
        ("Tools and technologies", _join(e.tools_technologies)),
        ("Other qualifications", _join(e.other_qualifications)),
        ("Academic qualifications", _join(e.academic_qualifications)),
        ("Professional experience", _join(e.professional_experience)),
    ]

    with st.expander("Stage 1 – Extraction (regular expressions)"):
        st.caption("Values found in the résumé, exactly as they were written.")
        st.dataframe(
            [{"Category": category, "Extracted": value} for category, value in rows],
            hide_index=True,
        )


def show_stage_2(result: PipelineResult) -> None:
    """Canonical token produced by the transducer of each extracted value."""

    e = result.extracted
    n = result.normalized
    t = get_pipeline().normalizer.transducers

    categories = [
        ("Languages", "M_LANG", t.languages, e.programming_languages),
        ("Frameworks", "M_FW", t.frameworks, e.frameworks_libraries),
        ("Databases", "M_DB", t.databases, e.databases),
        ("Tools", "M_TOOLS", t.tools, e.tools_technologies),
        ("Other", "M_OTHER", t.other, e.other_qualifications),
        ("Academic", "M_ACAD", t.academic, e.academic_qualifications),
        ("Experience", "M_EXP", t.experience, e.professional_experience),
    ]

    rows = [
        {
            "Category": category,
            "Transducer": name,
            "Extracted": value,
            "Output": t.translate(fst, value) or "rejected",
        }
        for category, name, fst, values in categories
        for value in values
    ]

    with st.expander("Stage 2 – Normalization (finite-state transducers)"):
        st.caption("Each extracted value is translated by the transducer of its category.")

        if rows:
            st.dataframe(rows, hide_index=True)
        else:
            st.write("No values were extracted.")

        years = n.experience_years if n.experience_years is not None else "—"
        st.markdown(f"**Years of experience:** {years}")

        st.markdown("**Sorted sequence of each profile** (input of the automata):")
        st.dataframe(
            [
                {"Profile": profile, "Sequence": _join(sequence)}
                for profile, sequence in n.profile_sequences.items()
            ],
            hide_index=True,
        )


def show_stage_3(result: PipelineResult) -> None:
    """Result of the automaton of each profile."""

    sequences = result.normalized.profile_sequences

    with st.expander("Stage 3 – Classification (finite automata)"):
        st.caption("Each automaton reads the sorted sequence of its profile.")
        st.dataframe(
            [
                {
                    "Profile": profile,
                    "Sequence read by the automaton": _join(sequences.get(profile, [])),
                    "Result": outcome,
                }
                for profile, outcome in result.classification.items()
            ],
            hide_index=True,
        )


def show_stage_4(result: PipelineResult) -> None:
    """Candidate profile written in the DSL and result of the validation."""

    with st.expander("Stage 4 – Candidate profile (context-free grammar, textX)"):
        if result.valid:
            st.success("The profile satisfies the grammar and the semantic rules (valid).")
        else:
            st.error(f"Invalid profile: {result.error}")

        st.caption("Profile written in the candidate profile language (.rl):")
        st.code(result.profile_text, language=None)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="ResumeLens", layout="wide")

    st.title("ResumeLens")
    st.caption(
        "Formal language-based résumé screening: regular expressions → "
        "finite-state transducers → finite automata → context-free grammar (textX)."
    )

    text, name = read_input()

    if st.button("Analyze", type="primary"):
        if not text.strip():
            st.warning("Enter a résumé first.")
        else:
            with st.spinner("Running the four stages..."):
                # The result is kept in the session state, so it stays on
                # the page when a download button or a section is clicked
                # (Streamlit runs the script again after every interaction).
                st.session_state["result"] = analyze(text, name)
                st.session_state["result_name"] = name

    if "result" in st.session_state:
        show_result(st.session_state["result"], st.session_state["result_name"])


main()
