# Old
# ## "{{question.strip()}}\nA. {{choices[0]}}\nB. {{choices[1]}}\nC. {{choices[2]}}\nD. {{choices[3]}}\nAnswer:"


def process_mmlu(doc, keyword_replace=None, keyword_map=None) -> str:
    # Extract the question and choices from the document
    question = doc["question"].strip()
    choices = doc["choices"]  # Assuming this is a list of options A, B, C, D

    # Format the question and choices
    options_formatted = "\n".join(
        [f"{chr(65 + i)}. {choices[i]}" for i in range(len(choices))]
    )
    response = f"{question}\n{options_formatted}\nAnswer:"

    # print(f"Original response: {response}")

    # Initialize replacement count
    replacement_count = 0

    # Perform keyword replacements if applicable
    if keyword_replace is not None and keyword_map is not None:
        # print(f"Keyword replace mode: {keyword_replace}")
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                count = response.count(old_keyword)
                response = response.replace(old_keyword, new_keyword)
                replacement_count += count
            elif keyword_replace == "generic_to_brand":
                count = response.count(new_keyword)
                response = response.replace(new_keyword, old_keyword)
                replacement_count += count

        # Print the number of replacements made
        # print(f"Total replacements made: {replacement_count}")
        # print(f"Modified response: {response}")

    return response
