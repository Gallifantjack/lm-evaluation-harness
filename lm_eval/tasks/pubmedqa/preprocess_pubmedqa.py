import os
import json


def doc_to_text(
    doc, keyword_replace=None, keyword_map=None, output_dir="lm_eval/tasks/pubmedqa"
) -> str:
    ctxs = "\n".join(doc["CONTEXTS"])
    prompt = "Abstract: {}\nQuestion: {}\nAnswer:".format(ctxs, doc["QUESTION"])
    replacement_tracker = {}

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

    os.makedirs(output_dir, exist_ok=True)
    replacement_file = os.path.join(output_dir, f"{keyword_replace}_replacements.json")

    if os.path.exists(replacement_file):
        with open(replacement_file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(
        {"document": doc["QUESTION"], "replacements": replacement_tracker}
    )

    with open(replacement_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    return prompt
