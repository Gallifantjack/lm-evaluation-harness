import os
import json
from datetime import datetime


def doc_to_text(
    doc, keyword_replace=None, keyword_map=None, output_dir="lm_eval/tasks/medmcqa"
) -> str:
    """
    Question: <question>
    Choices:
    A. <choice1>
    B. <choice2>
    C. <choice3>
    D. <choice4>
    Answer:
    """
    choices = [doc["opa"], doc["opb"], doc["opc"], doc["opd"]]
    option_choices = {
        "A": choices[0],
        "B": choices[1],
        "C": choices[2],
        "D": choices[3],
    }

    prompt = "Question: " + doc["question"] + "\nChoices:\n"
    for choice, option in option_choices.items():
        prompt += f"{choice.upper()}. {option}\n"
    prompt += "Answer:"

    replacement_tracker = {}

    # Perform keyword replacements if applicable
    if keyword_replace is not None and keyword_map is not None:
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                count = prompt.count(old_keyword)
                prompt = prompt.replace(old_keyword, new_keyword)
                replacement_tracker[old_keyword] = count
            elif keyword_replace == "generic_to_brand":
                count = prompt.count(new_keyword)
                prompt = prompt.replace(new_keyword, old_keyword)
                replacement_tracker[new_keyword] = count

    # Format today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    daily_output_dir = os.path.join(output_dir, today_date)

    # Ensure the output directory exists
    os.makedirs(daily_output_dir, exist_ok=True)
    replacement_file = os.path.join(
        daily_output_dir, f"{keyword_replace}_replacements.json"
    )

    # Load existing replacement tracking data if available
    if os.path.exists(replacement_file):
        with open(replacement_file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Add the current document's replacement data
    existing_data.append(
        {"document": doc["question"], "replacements": replacement_tracker}
    )

    # Write the updated data back to the file
    with open(replacement_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    return prompt
