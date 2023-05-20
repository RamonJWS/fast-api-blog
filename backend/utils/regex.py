import re


def replace_special_characters(input_string: str, replacement_character: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', replacement_character, input_string)
