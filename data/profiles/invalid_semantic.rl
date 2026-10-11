// INVALID (semantic): MYSQL is not a token of the canonical vocabulary.
candidate "Wednesday Addams" {
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
        tools: GIT, MYSQL
    }
    classification {
        FULL_STACK_DEVELOPER: ACCEPTED
        MACHINE_LEARNING_ENGINEER: REJECTED
        CYBERSECURITY_ENGINEER: REJECTED
        DATA_ENGINEER: REJECTED
    }
}
