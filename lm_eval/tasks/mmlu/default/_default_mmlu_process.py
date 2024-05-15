import os
import json
from datetime import datetime
import re


def process_mmlu(
    doc,
    keyword_replace=None,
    keyword_map=None,
    output_dir="lm_eval/tasks/benchmarks/onBrand/replacement_counts",
    subtype=None,
) -> str:
    base_onBrand_dir = "lm_eval/tasks/benchmarks/onBrand/replacement_counts"
    subtype_dir = f"{base_onBrand_dir}/{output_dir}"
    # Extract the question and choices from the document
    question = doc["question"].strip()
    choices = doc["choices"]  # Assuming this is a list of options A, B, C, D

    # Format the question and choices
    options_formatted = "\n".join(
        [f"{chr(65 + i)}. {choices[i]}" for i in range(len(choices))]
    )
    response = f"{question}\n{options_formatted}\nAnswer:"

    # Initialize replacement tracker
    replacement_tracker = []

    def count_and_replace(response, old_keyword, new_keyword):
        pattern = re.compile(re.escape(old_keyword), re.IGNORECASE)
        matches = pattern.findall(response)
        count = len(matches)
        response = pattern.sub(new_keyword, response)
        return response, count

    if keyword_replace is not None and keyword_map is not None:
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                response, count = count_and_replace(response, old_keyword, new_keyword)
                if count > 0:
                    replacement_tracker.append(
                        {"old": old_keyword, "replaced": new_keyword, "count": count}
                    )
            elif keyword_replace == "generic_to_brand":
                response, count = count_and_replace(response, new_keyword, old_keyword)
                if count > 0:
                    replacement_tracker.append(
                        {"old": new_keyword, "replaced": old_keyword, "count": count}
                    )
    # Format today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    daily_output_dir = os.path.join(subtype_dir, today_date)

    # Ensure the output directory exists
    os.makedirs(daily_output_dir, exist_ok=True)
    replacement_file = os.path.join(
        daily_output_dir, f"{keyword_replace}_replacements.json"
    )

    # Load or initialize the replacement file
    if os.path.exists(replacement_file):
        with open(replacement_file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Update the existing data with new counts
    for new_entry in replacement_tracker:
        updated = False
        for existing_entry in existing_data:
            if existing_entry["old"] == new_entry["old"]:
                existing_entry["count"] += new_entry["count"]
                updated = True
        if not updated:
            existing_data.append(new_entry)

    # Save the updated data to the replacement file
    with open(replacement_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    return response
