import os
import json


def doc_to_text(
    doc, keyword_replace=None, keyword_map=None, output_dir="lm_eval/tasks/medqa"
) -> str:
    option_choices = {
        "A": doc["ending0"],
        "B": doc["ending1"],
        "C": doc["ending2"],
        "D": doc["ending3"],
    }

    answers = "".join((f"{k}. {v}\n") for k, v in option_choices.items())
    prompt = f"Question: {doc['sent1']}\n{answers}Answer:"

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

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    replacement_file = os.path.join(output_dir, f"{keyword_replace}_replacements.json")

    # Load existing replacement tracking data if available
    if os.path.exists(replacement_file):
        with open(replacement_file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Add the current document's replacement data
    existing_data.append(
        {"document": doc["sent1"], "replacements": replacement_tracker}
    )

    # Write the updated data back to the file
    with open(replacement_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    return prompt


def doc_to_target(doc) -> int:
    return doc["label"]
