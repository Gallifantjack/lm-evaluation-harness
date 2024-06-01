import ast

# String representation of a dictionary
string = "{'A': 'HOUSING', 'B': 'RELATIONSHIP', 'C': 'TRANSPORTATION', 'D': '<NO_SDOH>', 'E': 'SUPPORT', 'F': 'EMPLOYMENT', 'G': 'PARENT'}"

# Converting the string to a dictionary and constructing the options string
options = ''.join(f"{k}. {v}\n" for k, v in ast.literal_eval(string).items() if v is not None)

def process_shadr(doc) -> str:
    return (
        doc["input"].strip()
        + "\n"
        + options
        + "\nPlease determine which Social determinants of health conditions is in provided sentence: \n"
        + "Answer:"
    )
