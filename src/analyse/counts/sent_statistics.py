import logging
import os

import pandas as pd
import toml

from helpers import percent, monthly_toml_stats

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(f"{PATH}/data")

reports = pd.read_csv(f"{DATA_PATH}/sent/last_month_reports.csv")

fetched_non_na = reports.dropna(subset=["Sent to"])
today = pd.to_datetime("today")
report_date = pd.to_datetime(reports["Date of report"], dayfirst=True)
report_due = (today - report_date).dt.days > 56
non_na = reports.assign(year=report_date.dt.year).dropna(subset=["Sent to"]).copy()
exploded = non_na.explode("Sent to", ignore_index=True)
sent_counts = exploded.value_counts("Sent to")
sent_years = exploded.value_counts(["year", "Status"]).unstack(fill_value=0)
type_counts = exploded.value_counts("Status")

status_counts = reports.value_counts("Status")

without = len(reports) - len(fetched_non_na)
failed = len(fetched_non_na) - len(non_na)

monthly_toml_stats["this report is sent to"] = statistics = {
    "reports parsed": [float(len(non_na)), percent(len(non_na), len(reports))],
    "reports without recipients": [float(without), percent(without, len(reports))],
    "reports failed": [float(failed), percent(failed, len(reports))],
    "reports pending": [float(status_counts.get("pending", 0)),
                        percent(status_counts.get("pending", 0), len(reports))],
    "reports overdue": [float(status_counts["overdue"]),
                        percent(status_counts["overdue"], len(reports))],
    "reports partial": [float(status_counts.get('partial', 0)),
                        percent(status_counts.get("partial", 0), len(reports))],
    "reports completed": [float(status_counts.get("completed", 0)),
                          percent(status_counts.get("completed", 0), len(reports))],
}

monthly_toml_stats["requests for response"] = {
    "no. recipients with requests": len(sent_counts),
    "no. requests for response": len(exploded),
    "requests pending": [float(type_counts.get("pending", 0)),
                         percent(type_counts.get("pending", 0), len(exploded))],
    "requests received": [float(type_counts.get("completed", 0)),
                           percent(type_counts.get("completed", 0), len(exploded))],
    "requests overdue": [float(type_counts.get("overdue", 0)),
                         percent(type_counts.get("overdue", 0), len(exploded))],
    "mean no. requests per recipient": round(sent_counts.mean(), 1),
    "median no. requests per recipient": sent_counts.median(),
    "IQR of requests per recipients": list(sent_counts.quantile([0.25, 0.75])),
}


def toml_to_log(toml_file, log_file):
    # logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    try:
        with open(toml_file, 'r', encoding='utf-8') as file:
            data = toml.load(file)
    except FileNotFoundError:
        logging.error(f'File {toml_file} not found.')
        return
    except Exception as e:
        logging.error(f'Error while reading file - {toml_file}: {e}')
        return

    try:
        with open(log_file, 'w') as file:
            for key, value in data.items():
                file.write(key + '\n')
                file.write("=" * 20 + '\n')
                for k, v in value.items():
                    file.write(f"{k}: {v}\n")
                file.write('\n\n')
    except Exception as e:
        logging.error(f'Error while writing file - {log_file}: {e}')


toml_to_log('src/data/monthly_statistics.toml', 'src/data/monthly_statistics.log')
toml_to_log('src/data/statistics.toml', 'src/data/statistics.log')
