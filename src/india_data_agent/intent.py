import re


def extract_entity(question):
    q = question.lower().strip()

    # Remove common question words
    q = re.sub(
        r"\b(what|was|is|the|value|of|in|for|how|much|did|tell|me|about|"
        r"gross|enrolment|enrollment|ratio)\b",
        " ",
        q,
    )

    # Remove year expressions
    q = q.replace("1999-2000", " ")
    q = q.replace("1999–2000", " ")
    q = q.replace("2009-10", " ")
    q = q.replace("2009–10", " ")

    # Remove possessive "'s"
    q = re.sub(r"'s\b", "", q)

    # Remove punctuation
    q = re.sub(r"[^a-zA-Z0-9() ]", " ", q)

    q = " ".join(q.split())

    # Known entities from the dataset
    entities = [
        "Jharkhand",
        "Bihar",
        "Assam",
        "Kerala",
        "H.P",
        "Tamil Nadu",
        "India",
        "China",
        "Indonesia",
        "Thailand",
        "Malaysia",
        "Brazil",
        "Developed countries",
        "Developing Countries",
        "World Average",
    ]

    for entity in entities:
        if entity.lower() in q:
            return entity

    return q.strip()
