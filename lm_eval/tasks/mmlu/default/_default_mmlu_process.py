import os
import json


def process_mmlu(
    doc, keyword_replace=None, keyword_map=None, output_dir="lm_eval/tasks/mmlu"
) -> str:
    # Extract the question and choices from the document
    question = doc["question"].strip()
    choices = doc["choices"]  # Assuming this is a list of options A, B, C, D

    # Format the question and choices
    options_formatted = "\n".join(
        [f"{chr(65 + i)}. {choices[i]}" for i in range(len(choices))]
    )
    response = f"{question}\n{options_formatted}\nAnswer:"

    replacement_tracker = {}

    # Perform keyword replacements if applicable
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

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    replacement_file = os.path.join(output_dir, "mmlu_replacements.json")

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

    return response
