import ast

def process_cd(doc) -> str:
    options = ""
    for k, v in ast.literal_eval(doc["choices"]).items():
        if v is not None:
            options += k + ". " + v + "\n"
    return doc["input"].strip() + "\n" + options + "Answer:"
