"""
Regular expressions used by the ResumeLens extraction stage.

This module only defines the patterns.
It does not perform extraction or normalization.
"""

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