import os

import pandas as pd

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(f"{PATH}/data")
REPORTS_PATH = os.path.abspath(f"{PATH}/../../data")
CORRECT_PATH = os.path.abspath(f"{PATH}/../../correct")

input_csv = os.path.abspath(f"{os.path.dirname(__file__)}/../../data/reports-corrected.csv")
reports = pd.read_csv(input_csv)
reports["date_of_report"] = pd.to_datetime(reports["date_of_report"], dayfirst=True)
reports = reports.sort_values(by="date_of_report", ascending=False)
reports.to_csv(input_csv, index=False)
