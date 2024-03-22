# %% [markdown]
# ## Process
# We count the number of reports in each year, ignoring reports that don't
# parse properly. We then save the results to a .csv file.
import datetime
import os

import pandas as pd
from helpers import toml_stats

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(f"{PATH}/data")
REPORTS_PATH = os.path.abspath(f"{PATH}/../../data")

# %% [markdown]
# ### Reading the reports

reports = pd.read_csv(f"{REPORTS_PATH}/reports-analysed.csv")

# %% [markdown]
# ### Extracting the dates of reports

# use a regex to extract the year from the date of report
reports["year"] = reports["date_of_report"].str.extract(r"\d{2}\/\d{2}\/(\d{4})")
reports["datetime"] = pd.to_datetime(reports["date_of_report"], format="%d/%m/%Y", errors="coerce")

earliest = reports["datetime"].min()
now = datetime.datetime.now()
year_diff = round((now.year - earliest.year + (now.month - earliest.month) / 12 + (now.day - earliest.day) / 365), 1)

# %% [markdown]
# ### Counting the number of reports in each year

# group by the year and count the number of reports
year_counts = reports.value_counts("year").sort_index()

toml_stats["year"] = statistics = {
    "no. reports parsed": reports.count()["year"],
    "no. years covered": year_diff,
    "mean per year": round(reports.count()["year"] / year_diff, 1),
    "median per year": year_counts.median(),
    "IQR of years": list(year_counts.quantile([0.25, 0.75])),
}

print(f"Year counts statistics: {statistics}")
print(f"Sorted counts: {year_counts}")

# %% [markdown]
# ### Saving the results

year_counts.to_csv(f"{DATA_PATH}/year/year-counts.csv")
