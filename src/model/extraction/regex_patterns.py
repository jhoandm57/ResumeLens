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

PHONE_PATTERN = (
    r"(?<!\d)"
    r"(?:\+?\d{1,3}[\s.-]?)?"
    r"(?:\(?\d{2,4}\)?[\s.-]?)?"
    r"\d{3}[\s.-]?\d{3,4}"
    r"(?:[\s.-]?\d{2,4})?"
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

# (?!\w) is used instead of a final \b because qualifications
# such as Ph.D. and B.Sc. can end with a period.
#
# ['’] supports both:
#   Bachelor's
#   Bachelor’s
#
ACADEMIC_QUALIFICATIONS_PATTERN = (
    r"(?:"
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

EXPERIENCE_PATTERN = (
    r"\b"
    r"\d+\+?"
    r"\s*(?:years?|yrs?)"
    r"(?:\s+of)?"
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