import os
from datetime import datetime, timedelta

import pandas as pd

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(f"{PATH}/data")


def filter_last_quarter_records(df, today_day):
    today_day = today_day.replace(month=1, day=1)
    first_day_of_quarter = today_day - timedelta(days=3 * 30)
    first_day_of_quarter = first_day_of_quarter.replace(day=1)
    last_day_of_quarter = (today_day - timedelta(days=1))
    df_copy = df.copy()
    df_copy["Date added"] = pd.to_datetime(df_copy["Date added"], format="%d/%m/%Y")
    print(first_day_of_quarter)
    print(last_day_of_quarter)
    filtered_df = df_copy[
        (df_copy["Date added"] >= first_day_of_quarter) & (df_copy["Date added"] <= last_day_of_quarter)
    ]
    filtered_df.loc[:, "Date added"] = pd.to_datetime(filtered_df["Date added"], format="%d/%m/%Y")
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df


reports = pd.read_csv(f"{DATA_PATH}/sent/database.csv")
today_date = datetime.now()
filtered_quarter_reports = filter_last_quarter_records(reports, today_date)

filtered_quarter_reports.to_csv(f"{DATA_PATH}/sent/last_quarter_reports.csv", index=False)
print("Quarterly report created.")
