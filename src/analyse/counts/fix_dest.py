import json
import os

import pandas as pd
import re

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(f"{PATH}/data")
REPORTS_PATH = os.path.abspath(f"{PATH}/../../data")
CORRECT_PATH = os.path.abspath(f"{PATH}/../../correct")


def sort_by_date(df):
    df["date_of_report"] = pd.to_datetime(df["date_of_report"], format='%d/%m/%Y')
    df.sort_values(by="date_of_report", inplace=True, ascending=False)
    df["date_of_report"] = df["date_of_report"].dt.strftime('%d/%m/%Y')
    df.to_csv(input_csv, index=False)


def find_matches(_input_string, _pattern):
    if _input_string:
        _input_string = _input_string.strip('| ')
        matches = re.finditer(_pattern, _input_string)
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
    return '|'.join(re.escape(key) for key in dictionary.values())


def process_csv(file, _pattern):
    df = pd.read_csv(file)
    df['this_report_is_being_sent_to'] = (df['this_report_is_being_sent_to']
                                          .apply(lambda x: find_matches(str(x), _pattern)))
    df.to_csv(file, index=False)
    print("Done...")


input_csv = os.path.abspath(f"{REPORTS_PATH}/reports-corrected.csv")

pattern = get_pattern(os.path.abspath(f"{CORRECT_PATH}/manual_replace/destinations.json"))
process_csv(input_csv, pattern)

reports = pd.read_csv(input_csv)
sort_by_date(reports)
