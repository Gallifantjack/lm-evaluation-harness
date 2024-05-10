import os
import json


def process_usmle_sa(
    doc,
    keyword_replace=None,
    keyword_map=None,
    output_dir="lm_eval/tasks/usmle_sa_step2",
) -> str:

    options = ""
    for k, v in doc["options"].items():
        if v is not None:
            options += k + ". " + v + "\n"

    question = doc["question"].strip()
    response = question + "\n" + options + "Answer:"

    replacement_tracker = {}

    if keyword_replace is not None and keyword_map is not None:
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                count = response.count(old_keyword)
                response = response.replace(old_keyword, new_keyword)
                replacement_tracker[old_keyword] = count
            elif keyword_replace == "generic_to_brand":
                count = response.count(new_keyword)
                response = response.replace(new_keyword, old_keyword)
                replacement_tracker[new_keyword] = count

    # Write the replacement tracker data to a JSON file
    os.makedirs(output_dir, exist_ok=True)
    replacement_file = os.path.join(output_dir, f"{keyword_replace}_replacements.json")

    # Load existing data if the file exists
    if os.path.exists(replacement_file):
        with open(replacement_file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Add the current document's replacement data
    existing_data.append(
        {"document": doc["question"], "replacements": replacement_tracker}
    )

    # Write updated data back to the file
    with open(replacement_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    return response
