"""
Validation of candidate profiles written in the ResumeLens DSL (stage 4).

ProfileValidator loads the grammar resume_lens.tx with textX and
checks a profile in two levels:

1. Lexical and syntactic rules (done by textX with the grammar).
   A violation raises TextXSyntaxError. Examples:
       - "react" in lower case            (lexical: not a TOKEN)
       - "MAYBE" as a result              (lexical: not 'ACCEPTED' / 'REJECTED')
       - the classification block missing (syntactic)
       - a missing "}"                    (syntactic)

2. Semantic rules (object processors registered in textX).
   A violation raises TextXSemanticError. Examples:
       - a token that is not in the canonical vocabulary of its category
       - a skill category or a profile written twice
       - one of the four profiles missing in the classification

If the profile is valid, the result is the textX model: the profile
as Python objects (model.name, model.skills.categories, ...), which is
the input of the visualization.

See docs/08_grammar_design.md.
"""

from pathlib import Path

from textx import get_location, metamodel_from_file
from textx.exceptions import TextXError, TextXSemanticError

from src.model.classification.profile_vocabulary import ProfileVocabulary
from src.model.normalization.normalization_vocabulary import NormalizationVocabulary as V


GRAMMAR_FILE = Path(__file__).with_name("resume_lens.tx")

# Canonical tokens accepted in each skill category.
CATEGORY_TOKENS = {
    "languages": set(V.LANGUAGES.values()),
    "frameworks": set(V.FRAMEWORKS.values()),
    "databases": set(V.DATABASES.values()),
    "tools": set(V.TOOLS.values()),
    "other": set(V.OTHER.values()),
}

# Fields of study: academic tokens that are not degrees.
FIELD_TOKENS = set(V.ACADEMIC.values()) - {"BACHELOR", "MASTER", "PHD"}


class ProfileValidator:
    """
    Validates candidate profiles with the grammar and the semantic rules.
    """

    def __init__(self):
        self.metamodel = metamodel_from_file(str(GRAMMAR_FILE))

        # Semantic rules: textX calls each function for every object
        # of that rule while it builds the model.
        self.metamodel.register_obj_processors({
            "SkillCategory": _check_skill_category,
            "Field": _check_field,
            "Skills": _check_skills,
            "Classification": _check_classification,
        })

    def validate(self, text: str):
        """
        Validate a profile and return its textX model.

        Raises:
            TextXSyntaxError: the text violates a lexical or syntactic rule.
            TextXSemanticError: the text violates a semantic rule.
        """

        return self.metamodel.model_from_str(text)

    def validate_file(self, path: str | Path):
        """Validate a profile stored in a file (.rl)."""

        return self.metamodel.model_from_file(str(path))

    def is_valid(self, text: str) -> bool:
        """True if the profile satisfies the grammar and the semantic rules."""

        try:
            self.validate(text)
            return True
        except TextXError:
            return False


# -------------------------------------------------------------------
# Semantic rules (object processors)
# -------------------------------------------------------------------

def _check_skill_category(category):
    """Every token of a category must be a canonical token of that category."""

    allowed = CATEGORY_TOKENS[category.category]

    for token in category.tokens:
        if token not in allowed:
            raise TextXSemanticError(
                f'"{token}" is not a valid token of the category '
                f'"{category.category}"',
                **get_location(category),
            )


def _check_field(field):
    """A field of study must be a canonical academic field."""

    if field.value not in FIELD_TOKENS:
        raise TextXSemanticError(
            f'"{field.value}" is not a valid field of study',
            **get_location(field),
        )


def _check_skills(skills):
    """A skill category cannot be written twice."""

    names = [category.category for category in skills.categories]
    repeated = sorted({name for name in names if names.count(name) > 1})

    if repeated:
        raise TextXSemanticError(
            f"repeated skill category: {', '.join(repeated)}",
            **get_location(skills),
        )


def _check_classification(classification):
    """The four profiles must appear exactly once."""

    profiles = [result.profile for result in classification.results]
    repeated = sorted({p for p in profiles if profiles.count(p) > 1})
    missing = [p for p in ProfileVocabulary.GROUPS if p not in profiles]

    if repeated:
        raise TextXSemanticError(
            f"repeated profile: {', '.join(repeated)}",
            **get_location(classification),
        )

    if missing:
        raise TextXSemanticError(
            f"missing profile: {', '.join(missing)}",
            **get_location(classification),
        )
