def process_cd(doc) -> str:
    options = ""
    for k, v in doc["options"].items():
        if v is not None:
            options += k + ". " + v + "\n"
    return doc["question"].strip() + "\n" + options + "Answer:"
