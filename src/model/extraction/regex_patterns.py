"""
Regular expressions used by the ResumeLens extraction stage.

This module only defines the patterns.
It does not perform extraction or normalization.
"""

# -------------------------------------------------------------------
# Candidate name
# -------------------------------------------------------------------

# Upper-case and lower-case letters, including accented letters
# (Á, É, Ñ, Ü, ...) so that Spanish names are also recognized.
_UPPER = r"A-ZÀ-ÖØ-Þ"
_LOWER = r"a-zß-öø-ÿ"

# One word of a name:
#   - Capitalized:  Wednesday, Peter, María, McDonald, O'Connor, Jean-Luc
#   - All capitals: PARKER (some résumés write the name in capitals)
_NAME_WORD = (
    rf"(?:(?:[{_UPPER}]['’])?[{_UPPER}][{_LOWER}]+(?:[-'’]?[{_UPPER}]?[{_LOWER}]+)*"
    rf"|[{_UPPER}]{{2,}}(?:[-'’][{_UPPER}]{{2,}})*)"
)

# Lower-case particles that may appear between the words of a name:
#   Juan de la Cruz, Ludwig van Beethoven
_NAME_PARTICLE = r"(?:de|del|la|las|los|da|das|do|dos|di|du|van|von|der|y)"

# A complete name: 2 to 4 words, optionally joined by particles.
#   Wednesday Addams, Mary Jane Watson, Juan de la Cruz Pérez
_FULL_NAME = (
    rf"{_NAME_WORD}"
    rf"(?:[ \t]+(?:{_NAME_PARTICLE}[ \t]+)*{_NAME_WORD}){{1,3}}"
)

# Words that start a section heading, not a name. They are excluded
# so that a first line such as "Technical Skills" or "Curriculum Vitae"
# is not taken as the candidate name.
#
# The second lookahead rejects a line that contains a job title
# (for example "Python Developer" or "Data Engineer"). The dot does
# not cross line breaks, so only the current line is checked.
_NOT_A_NAME = (
    r"(?!(?i:curriculum|resume|résumé|cv|technical|skills|experience"
    r"|professional|education|contact|profile|summary|objective)\b)"
    r"(?![^\n]*\b(?i:developer|engineer|scientist|analyst|architect"
    r"|manager|designer|programmer|consultant|intern)\b)"
)

# Form 1: an explicit label.
#   Name: Wednesday Addams
#   Full Name: Mary Jane Watson
# The label is case-insensitive (?i:...), but the name itself is not,
# because capital letters are what identify a proper name.
NAME_LABEL_PATTERN = (
    rf"^[ \t]*(?i:(?:full[ \t]+)?name)[ \t]*:[ \t]*"
    rf"({_FULL_NAME})"
    rf"[ \t]*$"
)

# Form 2: the name alone in the first non-empty line of the résumé
# (the usual header of a résumé, as in the examples of the statement).
#   \A\s*   start of the text, skipping blank lines and indentation
#   [ \t]*$ nothing else can appear in that line (no ":" or ",")
NAME_HEADER_PATTERN = (
    rf"\A\s*{_NOT_A_NAME}"
    rf"({_FULL_NAME})"
    rf"[ \t]*$"
)

# -------------------------------------------------------------------
# Contact information
# -------------------------------------------------------------------

EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}\b"
)

# A phone number is accepted in two forms:
#
#   1. With country code (+):       +57 300 1234567, +57-300-123-4567
#   2. Without country code, the 3-3-4 groups must be separated:
#                                   300 123 4567, (300) 123-4567
#
# Long numbers without separators and without "+" (for example
# 1234567890) are not accepted, because they cannot be distinguished
# from ID numbers. Year ranges such as 2001-2004 are not accepted either.
PHONE_PATTERN = (
    r"(?<![\w+])"
    r"(?:"
    r"\+\d{1,3}[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    r"|\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}"
    r")"
    r"(?!\d)"
)


# -------------------------------------------------------------------
# Programming languages
# -------------------------------------------------------------------

# JS is separated from the other alternatives because:
# \bJS\b could incorrectly match the "js" in React.js or Node.js.
PROGRAMMING_LANGUAGES_PATTERN = (
    r"(?:"
    r"\b(?:"
    r"JavaScript"
    r"|Javascript"
    r"|TypeScript"
    r"|Python"
    r"|SQL"
    r"|Bash"
    r")\b"
    r"|(?<![\w.])JS(?!\w)"
    r")"
)


# -------------------------------------------------------------------
# Frameworks and libraries
# -------------------------------------------------------------------

FRAMEWORKS_LIBRARIES_PATTERN = (
    r"\b(?:"
    r"React(?:\.js|JS)?"
    r"|Angular"
    r"|Vue"
    r"|Node(?:\.js|JS)"
    r"|Django"
    r"|Spring\s+Boot"
    r"|Pandas"
    r"|NumPy"
    r"|Scikit[-\s]?learn"
    r"|sklearn"
    r"|Tensor\s*Flow"
    r"|Py\s*Torch"
    r"|Apache\s+Spark"
    r"|Spark"
    r"|Apache\s+Airflow"
    r"|Airflow"
    r")\b"
)


# -------------------------------------------------------------------
# Databases
# -------------------------------------------------------------------

DATABASES_PATTERN = (
    r"\b(?:"
    r"PostgreSQL"
    r"|Postgres"
    r"|NoSQL"
    r"|SQL"
    r")\b"
)


# -------------------------------------------------------------------
# Academic qualifications
# -------------------------------------------------------------------

# \b at the beginning prevents matches inside other words
# (for example, "master" inside "Webmaster").
#
# (?!\w) is used instead of a final \b because qualifications
# such as Ph.D. and B.Sc. can end with a period.
#
# ['’] supports both:
#   Bachelor's
#   Bachelor’s
#
ACADEMIC_QUALIFICATIONS_PATTERN = (
    r"\b(?:"
    r"Bachelor(?:['’]s)?"
    r"|B\.?Sc\.?"
    r"|Master(?:['’]s)?"
    r"|M\.?Sc\.?"
    r"|Ph\.?D\.?"
    r"|Computer\s+Science"
    r"|Software\s+Engineering"
    r"|Systems\s+Engineering"
    r"|Data\s+Science"
    r")(?!\w)"
)


# -------------------------------------------------------------------
# Professional experience
# -------------------------------------------------------------------

# The lookbehinds prevent taking only part of a number:
#   1.5 years of experience   -> not extracted (instead of "5 years ...")
#   10-15 years of experience -> not extracted (instead of "15 years ...")
#
# The optional word "professional" supports:
#   4 years of professional experience
EXPERIENCE_PATTERN = (
    r"(?<![\d.,\-–])"
    r"(?<![\-–]\s)"
    r"\b"
    r"\d+\+?"
    r"\s*(?:years?|yrs?)"
    r"(?:\s+of)?"
    r"(?:\s+professional)?"
    r"\s+experience"
    r"\b"
)


# -------------------------------------------------------------------
# Tools and technologies
# -------------------------------------------------------------------

TOOLS_TECHNOLOGIES_PATTERN = (
    r"\b(?:"
    r"Git"
    r"|Docker"
    r"|Kubernetes"
    r"|Nmap"
    r"|Linux"
    r"|TCP\s*/?\s*IP"
    r"|Networking"
    r"|Network"
    r"|ETL"
    r"|ELT"
    r"|Data\s+Pipelines?"
    r"|Data\s+Warehousing"
    r"|Data\s+Warehouse"
    r")\b"
)


# -------------------------------------------------------------------
# Other relevant qualifications
# -------------------------------------------------------------------

# More specific alternatives are placed before shorter alternatives.
# For example:
#
# Machine Learning Model Development
# must be checked before
# Machine Learning
#
OTHER_QUALIFICATIONS_PATTERN = (
    r"\b(?:"
    r"Machine[-\s]Learning\s+Model\s+Development"
    r"|REST\s+APIs?"
    r"|Machine[-\s]Learning"
    r"|Vulnerability\s+Assessment"
    r"|Cyber\s*Security"
    r"|Cybersecurity"
    r"|Security\s+Automation"
    r")\b"
)