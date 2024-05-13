import os
import json
from datetime import datetime


def process_usmle_sa(
    doc,
    keyword_replace=None,
    keyword_map=None,
    output_dir="lm_eval/tasks/benchmarks/onBrand/replacement_counts/usmle_sa_step2",
) -> str:

    options = ""
    for k, v in doc["options"].items():
        if v is not None:
            options += k + ". " + v + "\n"

    question = doc["question"].strip()
    response = question + "\n" + options + "Answer:"

    # replacement_tracker = {}

    if keyword_replace is not None and keyword_map is not None:
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                count = response.count(old_keyword)
                response = response.replace(old_keyword, new_keyword)
                # if old_keyword in replacement_tracker:
                #     replacement_tracker[old_keyword] += count
                # else:
                #     replacement_tracker[old_keyword] = count
            elif keyword_replace == "generic_to_brand":
                count = response.count(new_keyword)
                response = response.replace(new_keyword, old_keyword)
                # if new_keyword in replacement_tracker:
                #     replacement_tracker[new_keyword] += count
                # else:
                #     replacement_tracker[new_keyword] = count

    # # Format today's date
    # today_date = datetime.now().strftime("%Y-%m-%d")
    # daily_output_dir = os.path.join(output_dir, today_date)

    # # Ensure the output directory exists
    # os.makedirs(daily_output_dir, exist_ok=True)
    # replacement_file = os.path.join(
    #     daily_output_dir, f"{keyword_replace}_replacements.json"
    # )

    # # Load or initialize the replacement tracker
    # if os.path.exists(replacement_file):
    #     with open(replacement_file, "r") as f:
    #         existing_data = json.load(f)
    # else:
    #     existing_data = {}

    # # Update the existing data with new counts
    # for keyword, count in replacement_tracker.items():
    #     if keyword in existing_data:
    #         existing_data[keyword] += count
    #     else:
    #         existing_data[keyword] = count

    # with open(replacement_file, "w") as f:
    #     json.dump(existing_data, f, indent=4)

    return response
