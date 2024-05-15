import os
import json
import re
from datetime import datetime


def doc_to_text(
    doc,
    keyword_replace=None,
    keyword_map=None,
    output_dir="lm_eval/tasks/benchmarks/onBrand/replacement_counts/medqa",
) -> str:
    option_choices = {
        "A": doc["ending0"],
        "B": doc["ending1"],
        "C": doc["ending2"],
        "D": doc["ending3"],
    }

    answers = "".join((f"{k}. {v}\n") for k, v in option_choices.items())
    prompt = f"Question: {doc['sent1']}\n{answers}Answer:"

    # Initialize replacement tracker
    replacement_tracker = []

    def count_and_replace(prompt, old_keyword, new_keyword):
        pattern = re.compile(re.escape(old_keyword), re.IGNORECASE)
        matches = pattern.findall(prompt)
        count = len(matches)
        prompt = pattern.sub(new_keyword, prompt)
        return prompt, count

    if keyword_replace is not None and keyword_map is not None:
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                prompt, count = count_and_replace(prompt, old_keyword, new_keyword)
                if count > 0:
                    replacement_tracker.append(
                        {"old": old_keyword, "replaced": new_keyword, "count": count}
                    )
            elif keyword_replace == "generic_to_brand":
                prompt, count = count_and_replace(prompt, new_keyword, old_keyword)
                if count > 0:
                    replacement_tracker.append(
                        {"old": new_keyword, "replaced": old_keyword, "count": count}
                    )

    # Format today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    daily_output_dir = os.path.join(output_dir, today_date)

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
            if (
                new_entry["old"].lower() == existing_entry["old"].lower()
                and new_entry["replaced"].lower() == existing_entry["replaced"].lower()
            ):
                existing_entry["count"] += new_entry["count"]
                updated = True
                break
        if not updated:
            existing_data.append(new_entry)

    # Save the updated data to the replacement file
    with open(replacement_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    return prompt


def doc_to_target(doc) -> int:
    return doc["label"]
