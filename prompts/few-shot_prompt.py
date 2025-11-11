from prompts_strict import task_prompt
# from prompts_balanced import task_prompt
# from prompts_liberal import task_prompt


easy_examples = [
    {
        "text": "", 
        "output": {
            "SDoH_categories": [""],
            "SDoH_subcategories": [""], 
        },
        "explanation": ""
    }
]


hard_examples = [
    {
        "text": "", 
        "output": {
            "SDoH_categories": [""],
            "SDoH_subcategories": [""], 
        },
        "explanation": ""
    }
]


# Format examples for the prompt
formatted_examples = ""
for i, ex in enumerate(hard_examples, 1):
    formatted_examples += f"### Example {i}\n"
    formatted_examples += "<INPUT>\n"
    formatted_examples += f"{ex['text']}\n"
    formatted_examples += "</INPUT>\n\n"

    formatted_examples += "<OUTPUT_JSON>\n"
    formatted_examples += json.dumps(ex["output"], ensure_ascii=False, indent=2)
    formatted_examples += "\n</OUTPUT_JSON>\n\n"

    formatted_examples += "<EXPLANATION>\n"
    formatted_examples += f"{ex['explanation']}\n"
    formatted_examples += "</EXPLANATION>\n\n"


task_prompt_w_examples = task_prompt + "\n## Examples:\n" + formatted_examples


