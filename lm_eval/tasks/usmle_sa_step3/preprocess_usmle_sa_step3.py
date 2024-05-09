def process_usmle_sa(doc, keyword_replace=None, keyword_map=None) -> str:
    print(keyword_replace)
    print(len(keyword_map))

    options = ""
    for k, v in doc["options"].items():
        if v is not None:
            options += k + ". " + v + "\n"

    question = doc["question"].strip()
    response = question + "\n" + options + "Answer:"

    # Initialize replacement count
    replacement_count = 0

    if keyword_replace is not None and keyword_map is not None:
        print(f"Keyword replace mode in loop: {keyword_replace}")
        for old_keyword, new_keyword in keyword_map.items():
            if keyword_replace == "brand_to_generic":
                # Check how many times the old keyword appears before replacing
                replacement_count += response.count(old_keyword)
                response = response.replace(old_keyword, new_keyword)
            elif keyword_replace == "generic_to_brand":
                # Check how many times the new keyword appears before replacing
                replacement_count += response.count(new_keyword)
                response = response.replace(new_keyword, old_keyword)

        # Print the number of replacements made
        print(f"Total replacements made: {replacement_count}")

    return response
