import os
from datetime import datetime, timedelta

import pandas as pd
from helpers import toml_stats

PATH = os.path.dirname(__file__)


def get_complete_percents():
    file_path = os.path.abspath(f"{PATH}/data/sent/received_percents.csv")
    date = (datetime.now() - timedelta(days=1)).strftime("%b %y")
    percent = ",".join(str(toml_stats["this report is sent to"]["reports completed"][1]).split("."))
    new_data = pd.DataFrame({"Date": [date], "Requests Received Percent": [percent]})
    if os.path.exists(file_path):
        existing_data = pd.read_csv(file_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data
    updated_data.to_csv(file_path, index=False)


def get_overdue_percents():
    file_path = os.path.abspath(f"{PATH}/data/sent/overdue_percents.csv")
    date = (datetime.now() - timedelta(days=1)).strftime("%b %y")
    percent_overdue = ",".join(str(toml_stats["this report is sent to"]["reports overdue"][1]).split("."))
    percent_partial = ",".join(str(toml_stats["this report is sent to"]["reports partial"][1]).split("."))
    new_data = pd.DataFrame({"Date": [date], "Overdue Percent": [percent_overdue], "Partial Percent": [percent_partial]})
    if os.path.exists(file_path):
        existing_data = pd.read_csv(file_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data
    updated_data.to_csv(file_path, index=False)


get_complete_percents()
get_overdue_percents()
