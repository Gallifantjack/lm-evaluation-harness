import pandas as pd
import ast

# # Load the CSV file outside the function
# file_path = '../../../G2B_keywords.csv'
# df = pd.read_csv(file_path)

# # Convert the 'generic' and 'brand' columns to lower case once
# df['generic'] = df['generic'].str.lower()
# df['brand'] = df['brand'].str.lower()

# # Ensure 'found_keywords' are lists
# def ensure_list_format(column):
#     if isinstance(column.iloc[0], str):
#         try:
#             column = column.apply(ast.literal_eval)
#         except (ValueError, SyntaxError):
#             pass
#     return column

# df['found_keywords'] = ensure_list_format(df['found_keywords'])

def get_brand_names(df, generic_names):
    # Convert the list of generic names to lower case
    generic_names_lower = [name.lower() for name in generic_names]

    # Find the corresponding brand names
    brand_names = df[df['generic'].isin(generic_names_lower)]['brand'].tolist()

    # Generate the output string
    output_string = f"Note that the drugs mentioned in the question have generic names as {', '.join(generic_names_lower)}."

    return output_string, brand_names


def doc_to_text(doc) -> str:
    option_choices = {
        "A": doc["ending0"],
        "B": doc["ending1"],
        "C": doc["ending2"],
        "D": doc["ending3"],
    }
    answers = "".join((f"{k}. {v}\n") for k, v in option_choices.items())
    
    list_of_generic_names = doc['found_keywords']
    hint_prompt = f"Note that the drugs mentioned in the question have generic names as {', '.join(list_of_generic_names)}."
    return f"Question: {doc['sent1']}\n{answers}" + hint_prompt + "\nAnswer:"


def doc_to_target(doc) -> int:
    return doc["label"]
