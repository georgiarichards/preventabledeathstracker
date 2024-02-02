import json
import os

import pandas as pd
import re


def find_matches(_input_string, pattern):
    if _input_string:
        _input_string = _input_string.strip('| ')
        matches = re.finditer(pattern, _input_string)
        list_of_match = [match.group() for match in matches if match.group()]
        cleaned_values = [value.replace(r'\ ', ' ') for value in list_of_match]
        a = ' | '.join(cleaned_values)
        cleaned_string = a.strip('| ')
        return cleaned_string
    return None


def get_pattern(file):
    with open(file, 'r') as f:
        dictionary_json = f.read()
    list_of_dicts = json.loads(dictionary_json)
    dictionary = {k: v for d in list_of_dicts for k, v in d.items()}
    pattern = '|'.join(re.escape(key) for key in dictionary.values())
    return pattern


def process_csv(file, pattern):
    df = pd.read_csv(file)
    df['this_report_is_being_sent_to'] = df['this_report_is_being_sent_to'].apply(lambda x: find_matches(str(x), pattern))
    df.to_csv(file, index=False)
    print("Done...")


input_csv = os.path.abspath(f"{os.path.dirname(__file__)}/../../data/reports-corrected.csv")
pattern_path = os.path.abspath(f"{os.path.dirname(__file__)}/../../correct/manual_replace/destinations.json")

pattern = get_pattern(pattern_path)
process_csv(input_csv, pattern)
