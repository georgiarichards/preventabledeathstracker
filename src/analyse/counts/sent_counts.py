# %% [markdown]
# ## Process
# We count the number of reports in each death category, ignoring reports that
# don't match any known category. We then save the results to a .csv file.
# %% [markdown]
# ### Importing libraries

import os
import re
from datetime import datetime, timedelta

import pandas as pd

from create_badge import create_badge
from helpers import percent, toml_stats
from src.analyse.counts.data.html.elements import CounterType
from src.analyse.counts.data.html.get_html_counter import get_html_counter
from src.analyse.counts.data.html.html_percent_types import StatusCounter, get_status_html_counter

TOP_N = 30
QUARTER_MONTHS = [1, 4, 7, 10]

vbar = re.compile(r"\s*\|\s*")

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(f"{PATH}/data")
REPORTS_PATH = os.path.abspath(f"{PATH}/../../data")
CORRECT_PATH = os.path.abspath(f"{PATH}/../../correct")


# %% [markdown]
# ### Reading the reports
def filter_last_month_records(df):
    today_date = datetime.now()
    first_day_of_current_month = today_date.replace(day=1)
    first_day_of_last_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    df_copy = df.copy()
    df_copy["date_added"] = pd.to_datetime(df_copy["date_added"], format="%d/%m/%Y")
    filtered_df = df_copy[
        (df_copy["date_added"] >= first_day_of_last_month) & (df_copy["date_added"] <= last_day_of_last_month)
        ]
    # filtered_df["date_added"] = filtered_df["date_added"].dt.strftime("%d/%m/%Y")
    filtered_df.loc[:, "date_added"] = filtered_df["date_added"].dt.strftime("%d/%m/%Y")
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df, today_date


def select_and_rename_columns(df):
    selected_columns = [
        "Status",
        "Date added",
        "Date of report",
        "Ref",
        "Deceased name",
        "Coroner name",
        "Coroner area",
        "Category",
        "Sent to",
        "Sent to count",
        "Replies count",
        "URL",
    ]
    df.rename(
        columns={
            "response status": "Status",
            "date_of_report": "Date of report",
            "date_added": "Date added",
            "ref": "Ref",
            "deceased_name": "Deceased name",
            "coroner_name": "Coroner name",
            "coroner_area": "Coroner area",
            "category": "Category",
            "no. replies": "Replies count",
            "no. recipients": "Sent to count",
            "this_report_is_being_sent_to": "Sent to",
            "report_url": "URL",
        },
        inplace=True,
    )
    return df[selected_columns]


reports = pd.read_csv(f"{REPORTS_PATH}/reports-analysed.csv")
fetched = pd.read_csv(f"{REPORTS_PATH}/reports.csv")

reports["replies"] = (
    reports["reply_urls"]
    .fillna("")
    .str.split(vbar)
    .apply(lambda replies: [reply for reply in replies if "https" in reply])
)
reports["no. replies"] = 0
reports["no. replies"] = reports["replies"].str.len()

fetched_non_na = fetched.dropna(subset=["this_report_is_being_sent_to"])

# %% [markdown]
# ### Calculating the due status for each report

today = pd.to_datetime("today")
report_date = pd.to_datetime(reports["date_of_report"], dayfirst=True)
report_due = (today - report_date).dt.days > 56

# %% [markdown]
# ### Splitting the sent to and reply urls

non_na = reports.assign(year=report_date.dt.year).dropna(subset=["this_report_is_being_sent_to"]).copy()
non_na["status"] = "overdue"
non_na["sent_to"] = non_na["this_report_is_being_sent_to"].str.split(vbar)
non_na["no. recipients"] = non_na["sent_to"].str.len()

non_na["replies"] = (
    reports["reply_urls"]
    .fillna("")
    .str.split(vbar)
    .apply(lambda replies: [reply for reply in replies if "Response" in reply])
)
non_na["no. replies"] = non_na["replies"].str.len()

non_na["escaped_urls"] = non_na["reply_urls"].str.replace(r"[-_]|%20", " ", regex=True).fillna("")

# %% [markdown]
# ### Status based on no. recipients vs replies

equal_replies = non_na.apply(lambda x: len(x["sent_to"]) == len(x["replies"]) and len(x["sent_to"]) > 0, axis=1)
non_na.loc[equal_replies, "status"] = "received"
non_na.loc[~report_due, "status"] = "pending"

# %% [markdown]
# ### Status based on recipients in replies

exploded = non_na.explode("sent_to", ignore_index=True)
responded = exploded.apply(lambda x: str(x["sent_to"]) in str(x["escaped_urls"]), axis=1)
exploded["status"] = exploded["status"].mask(responded, "received")

# %% [markdown]
# ### Calculating the counts for each recipient
# exploded["year"] = exploded['year'].astype(int)
sent_to_yearly = exploded['sent_to'].groupby(exploded['year']).value_counts().unstack(fill_value=0)
sent_to_yearly = sent_to_yearly.transpose()
sent_to_yearly.index.name = 'Addressed to'
sent_to_yearly['Total no. PFDs'] = sent_to_yearly.sum(axis=1)

sent_to_yearly.to_csv(f"{DATA_PATH}/sent/sent_to_yearly.csv")

sent_types = exploded.value_counts(["sent_to", "status"]).unstack(fill_value=0)
sent_types["no. PFDs"] = exploded["sent_to"].value_counts()
sent_types = sent_types[["no. PFDs", "overdue", "pending", "received"]].sort_values("no. PFDs", ascending=False)
sent_types["% received"] = sent_types["received"] / sent_types["no. PFDs"] * 100
sent_types["% received"] = sent_types["% received"].apply(lambda el: int(round(el, 0)))

sent_types_with_partial = exploded.value_counts(["sent_to", "response status"]).unstack(fill_value=0)
sent_types_with_partial["no. PFDs"] = exploded["sent_to"].value_counts()
sent_types_with_partial = sent_types_with_partial[["no. PFDs", "overdue", "pending", "completed", "partial"]].sort_values("no. PFDs", ascending=False)
sent_types_with_partial["% completed"] = sent_types_with_partial["completed"] / sent_types["no. PFDs"] * 100
sent_types_with_partial["% completed"] = sent_types_with_partial["% completed"].apply(lambda el: int(round(el, 0)))



sent_counts = exploded.value_counts("sent_to")
sent_years = exploded.value_counts(["year", "status"]).unstack(fill_value=0)
type_counts = exploded.value_counts("status")

# %% [markdown]
# ### Calculating the status of each report

non_na.loc[:, "response status"] = "partial"
reports.loc[:, "response status"] = "partial"

# for each report, calculate the list of recipients with responses


# reports["escaped_urls"] = reports["reply_urls"].str.replace(r"[-_]|%20", " ", regex=True).fillna("")
# reports["sent_to"] = reports["this_report_is_being_sent_to"].str.split(vbar)
#
responses_from = lambda row: [sent for sent in row["sent_to"] if sent in row["escaped_urls"]]
with_responses = non_na.apply(responses_from, axis=1)
# with_responses_r = reports.apply(responses_from, axis=1)

# if there's none, mark overdue
no_responses = (with_responses.str.len() == 0) & (non_na["replies"].str.len() == 0)
non_na.loc[no_responses, "response status"] = "overdue"

no_responses_r = (reports["no. recipients"] > 0) & (reports["no. replies"] == 0)
reports.loc[no_responses_r, "response status"] = "overdue"

# no_responses_r = (with_responses_r.str.len() == 0) & (reports["replies"].str.len() == 0)
# reports.loc[no_responses_r, "response status"] = "overdue"


no_sent_to = (reports["no. recipients"] == 0) & (reports["no. replies"] > 0)
reports.loc[no_sent_to, "response status"] = "no sent_to"

# if there's an equal number of recipients and replies, mark completed
equal_len = (non_na["sent_to"].str.len() <= non_na["replies"].str.len()) & (non_na["sent_to"].str.len() > 0)
non_na.loc[equal_len, "response status"] = "completed"

# if all are responded to, mark completed
all_responses = with_responses.str.len() >= non_na["sent_to"].str.len()
non_na.loc[all_responses, "response status"] = "completed"

# if a report is pending or overdue and less than 56 days old, mark pending
non_na.loc[~report_due & (non_na["response status"] == "overdue"), "response status"] = "pending"
non_na.loc[~report_due & (non_na["response status"] == "partial"), "response status"] = "pending"

reports.loc[~report_due & (reports["response status"] == "overdue"), "response status"] = "pending"
reports.loc[~report_due & (reports["response status"] == "partial"), "response status"] = "pending"

equal_len_r = (
        (reports["no. recipients"] <= reports["no. replies"])
        & (reports["no. recipients"] != 0)
        & (reports["no. replies"] != 0)
)
reports.loc[equal_len_r, "response status"] = "completed"
# %% [markdown]
# ### Adding the non_na rows back to the reports

# mask_abc_zero = reports["no. replies"] == 0
# mask_update = mask_abc_zero & reports.index.isin(reports.index)
# reports.loc[mask_update, "response status"] = reports["response status"]

# empty_requests = reports["this_report_is_being_sent_to"].isna()
current_date = pd.Timestamp.now()
condition_overdue = (reports["no. replies"] == 0) & (reports["no. recipients"] == 0) & ((current_date - pd.to_datetime(reports["date_of_report"], dayfirst=True)).dt.days > 56)
condition_pending = (reports["no. replies"] == 0) & (reports["no. recipients"] == 0) & ((current_date - pd.to_datetime(reports["date_of_report"], dayfirst=True)).dt.days <= 56)
reports.loc[condition_overdue, "response status"] = "overdue"
reports.loc[condition_pending, "response status"] = "pending"

# reports.loc[:, "no. recipients"] = 0
# reports.loc[non_na.index, "no. recipients"] = non_na["no. recipients"]
#
# reports.loc[:, "no. replies"] = 0
# reports.loc[non_na.index, "no. replies"] = non_na["no. replies"]

print(reports[["ref", "response status"]].head(10))
print(reports["response status"].value_counts())

# %% [markdown]
# ### Calculating response status over time
statuses = reports.copy()

status_years = reports.assign(year=report_date.dt.year).value_counts(["year", "response status"]).unstack(fill_value=0)

columns_options = [
    ["no requests", "failed", "pending", "overdue", "partial", "completed"],
    ["no requests", "pending", "overdue", "partial", "completed"],
    ["pending", "overdue", "partial", "completed"],
    ["overdue", "partial", "completed"],
    ["overdue", "completed"]
]
selected_option = columns_options[0]
for columns in columns_options:
    try:
        selected_option = columns
        status_years = status_years[columns]
        break
    except KeyError:
        continue

# %% [markdown]
# ### Writing back the reports with the status

# Add our new columns to the reports
report_columns = reports.columns.tolist()
report_columns.insert(0, "response status")
count_idx = report_columns.index("this_report_is_being_sent_to") + 1
report_columns.insert(count_idx, "no. replies")
report_columns.insert(count_idx, "no. recipients")
report_columns = list(dict.fromkeys(report_columns))

reports[report_columns].to_csv(f"{REPORTS_PATH}/reports-analysed.csv", index=False)

# %% [markdown]
# ### Calculating statistics

status_counts = reports.value_counts("response status")

# %% [markdown]
# ### Calculating statistics over coroner areas

area_statuses = reports.value_counts(["coroner_area", "response status"]).unstack(fill_value=0)
area_statuses.loc[:, ["no. recipients", "no. replies"]] = reports.groupby("coroner_area")[
    ["no. recipients", "no. replies"]
].sum()

status_rename_dict = {
            "completed": "no. complete responses",
            "partial": "no. partial responses",
            "overdue": "no. overdue responses",
            "failed": "no. failed parses",
            "pending": "no. pending responses",
        }

filtred_status_rename_dict = {k: v for k, v in status_rename_dict.items() if k in selected_option}

area_statuses = area_statuses.rename(
    filtred_status_rename_dict,
    axis=1,
)
area_statuses["no. PFDs"] = reports["coroner_area"].value_counts()
area_statuses = area_statuses.sort_values("no. PFDs", ascending=False)

base_list = ["no. PFDs", "no. recipients", "no. replies"]
raw_list = [
            "no. complete responses",
            "no. partial responses",
            "no. overdue responses",
            "no. pending responses",
            "no. failed parses",
        ]
list_for_extend = [i for i in raw_list if i in filtred_status_rename_dict.values()]
statuses_list = base_list.extend(list_for_extend)
area_statuses = area_statuses[base_list]

# %% [markdown]
# ### Calculating statistics over coroner names

name_statuses = reports.value_counts(["coroner_name", "response status"]).unstack(fill_value=0)
name_statuses.loc[:, ["no. recipients", "no. replies"]] = reports.groupby("coroner_name")[
    ["no. recipients", "no. replies"]
].sum()

name_statuses = name_statuses.rename(
    filtred_status_rename_dict,
    axis=1,
)

name_statuses["no. PFDs"] = reports["coroner_name"].value_counts()
name_statuses = name_statuses.sort_values("no. PFDs", ascending=False)
name_statuses = name_statuses[base_list]

# %% [markdown]
# ### Calculating statistics over recipients
exploded = exploded.drop_duplicates(subset=["report_url"], keep="first")

exploded = exploded.assign(sent_to=exploded["this_report_is_being_sent_to"].str.split(vbar)).explode(
    "sent_to", ignore_index=True
)

rcpt_statuses = exploded.value_counts(["sent_to", "response status"]).unstack(fill_value=0)
rcpt_statuses.loc[:, ["no. recipients", "no. replies"]] = exploded.groupby("sent_to")[
    ["no. recipients", "no. replies"]
].sum()
rcpt_statuses = rcpt_statuses.rename(
    {
        "completed": "no. complete responses",
        "partial": "no. partial responses",
        "overdue": "no. overdue responses",
        "pending": "no. pending responses",
    },
    axis=1,
)
rcpt_statuses["no. PFDs"] = exploded["sent_to"].value_counts()
rcpt_statuses = rcpt_statuses.sort_values("no. PFDs", ascending=False)
rcpt_statuses = rcpt_statuses[
    [
        "no. PFDs",
        "no. recipients",
        "no. replies",
        "no. complete responses",
        "no. partial responses",
        "no. overdue responses",
        "no. pending responses",
    ]
]
# Quick note here: we won't ever get the no. failed parses as a recipient is only found if the parse is successful

# %% [markdown]
# ### Various statistics about the counts

without = len(fetched) - len(fetched_non_na)
failed = len(fetched_non_na) - len(non_na)

get_html_counter(len(fetched), CounterType.COUNT)
get_html_counter(round(percent(status_counts["completed"], len(fetched))), CounterType.PERCENT)
get_html_counter(len(sent_counts), CounterType.ADDRESSEES)

toml_stats["this report is sent to"] = statistics = {
    "reports parsed": [float(len(non_na)), percent(len(non_na), len(fetched))],
    "reports without recipients": [float(without), percent(without, len(fetched))],
    "reports failed": [float(failed), percent(failed, len(fetched))],
    "reports no sent_to": [float(status_counts["no sent_to"]), percent(status_counts["no sent_to"], len(fetched))] if "no sent_to" in status_counts else 0,
    "reports pending": [float(status_counts["pending"]), percent(status_counts["pending"], len(fetched))],
    "reports overdue": [float(status_counts["overdue"]), percent(status_counts["overdue"], len(fetched))],
    "reports partial": [float(status_counts["partial"]), percent(status_counts["partial"], len(fetched))],
    "reports completed": [float(status_counts["completed"]), percent(status_counts["completed"], len(fetched))],
}

get_status_html_counter(status_counts["completed"], round(percent(status_counts["completed"], len(fetched))), StatusCounter.COMPLETED)
get_status_html_counter(status_counts["partial"], round(percent(status_counts["partial"], len(fetched))), StatusCounter.PARTIAL)
get_status_html_counter(status_counts["overdue"], round(percent(status_counts["overdue"], len(fetched))), StatusCounter.OVERDUE)
get_status_html_counter(status_counts["pending"], round(percent(status_counts["pending"], len(fetched))), StatusCounter.PENDING)

toml_stats["requests for response"] = {
    "no. recipients with requests": len(sent_counts),
    "no. requests for response": len(exploded),
    "requests pending": [float(type_counts["pending"]), percent(type_counts["pending"], len(exploded))],
    "requests received": [float(type_counts["received"]), percent(type_counts["received"], len(exploded))],
    "requests overdue": [float(type_counts["overdue"]), percent(type_counts["overdue"], len(exploded))],
    "mean no. requests per recipient": round(sent_counts.mean(), 1),
    "median no. requests per recipient": sent_counts.median(),
    "IQR of requests per recipients": list(sent_counts.quantile([0.25, 0.75])),
}

# %% [markdown]
# ### Calculating the top coroners

top_counts = sent_counts.head(TOP_N)
top_types = sent_types.loc[top_counts.index]

# %% [markdown]
# ### Create statistics with statuses

statuses.rename(
    columns={
        "response status": "Status",
        "ref": "Ref",
        "date_of_report": "Date of report",
        "deceased_name": "Deceased name",
        "coroner_name": "Coroner name",
        "category": "Category",
        "coroner_area": "Coroner area",
        "no. replies": "Replies count",
        "no. recipients": "Sent to count",
        "this_report_is_being_sent_to": "Sent to",
        "report_url": "Report URL",
        "date_added": "Date added",
    },
    inplace=True,
)

statuses["Status"] = statuses["Status"].replace({"failed": "error"})

statuses["Status"] = statuses["Status"].apply(create_badge)
# statuses['Deceased name'] = statuses.apply(lambda row: create_button(row['Deceased name'], row['report_url']), axis=1)
new_order = [
    "Status",
    "Date added",
    "Date of report",
    "Ref",
    "Deceased name",
    "Coroner name",
    "Coroner area",
    "Category",
    "Sent to",
    "Sent to count",
    "Replies count",
    "Report URL",
]
statuses = statuses[new_order]

# %% [markdown]
# ### Saving the results
exploded = exploded[exploded["response status"] != "failed"]
statuses = statuses[statuses["Status"] != "error"]

# sent_types.rename(columns={"received": "completed", "% received": "% completed"}, inplace=True)
sent_types.rename(columns={"sent_to": "Addressed to", "% no. PFDs": "Total no. PFDs"}, inplace=True)

sent_counts.to_csv(f"{DATA_PATH}/sent/sent-counts.csv")
top_counts.to_csv(f"{DATA_PATH}/sent/top-sent-counts.csv")
sent_types.to_csv(f"{DATA_PATH}/sent/sent-types.csv")
top_types.to_csv(f"{DATA_PATH}/sent/top-sent-types.csv")
sent_years.to_csv(f"{DATA_PATH}/sent/sent-types-years.csv")
status_years.to_csv(f"{DATA_PATH}/sent/status-years.csv")
exploded.to_csv(f"{DATA_PATH}/sent/statuses.csv", index=False)


new_types = sent_types_with_partial.copy()
new_types.index.rename("Addressed to", inplace=True)
new_types = new_types[["% completed", "completed", "partial", "overdue", "pending"]]
result = pd.merge(sent_to_yearly, new_types, on='Addressed to', how='inner')
result.rename(columns={"Total no. PFDs": "Total"}, inplace=True)
# result.sort_values(by=["% completed", "Total"], ascending=[False, False], inplace=True)
result.sort_values(by="Total", ascending=False, inplace=True)
result.to_csv(f"{DATA_PATH}/sent/sent_to_yearly.csv")

top_types_with_partial = sent_types_with_partial.loc[top_counts.index]
top_types_with_partial.to_csv(f"{DATA_PATH}/sent/top-sent-types-with_partial.csv")

statuses["Date of report"] = pd.to_datetime(statuses["Date of report"], format="%d/%m/%Y")
statuses.sort_values(by="Date of report", inplace=True, ascending=False)
statuses["Date of report"] = statuses["Date of report"].dt.strftime("%d/%m/%Y")


def write_sum_of_replies_to_log(path):
    sum_of_replies, sum_of_response = get_replies_and_responses(statuses)

    replies_pattern = re.compile(r" - All replies count: \d+")
    response_pattern = re.compile(r" - All responses count: \d+")

    new_replies_text = f" - All replies count: {sum_of_replies}"
    new_response_text = f" - All responses count: {sum_of_response}"

    try:
        with open(path, "r") as file:
            content = file.read()

        new_content = replies_pattern.sub(new_replies_text, content)
        new_content = response_pattern.sub(new_response_text, new_content)

    except FileNotFoundError:
        new_content = f"\n\n{new_response_text}\n{new_replies_text}"

    with open(f"{path}", "w") as file:
        file.write(new_content)

    print("Log updated.")


def write_monthly_data_to_log(path, df):
    sum_of_replies, _ = get_replies_and_responses(df)
    today_date_ = datetime.now()
    with open(f"{path}", "w") as file:
        log_msg = (
            f"Latest monthly fetch on {today_date_.strftime('%m/%d/%Y')} at "
            f"{today_date_.strftime('%H:%M:%S')}, for which:\n"
            f" - {len(df)} new reports were added last month.\n\n"
        )
        log_msg += f"\n - Replies counts last month: {sum_of_replies}"

        file.write(log_msg)
    print("Monthly log created.")


def get_replies_and_responses(df):
    sum_of_replies = df["Replies count"].sum()
    sum_of_response = df["Sent to count"].sum()
    return sum_of_replies, sum_of_response


statuses.to_csv(f"{DATA_PATH}/sent/db_with_statuses.csv", index=False)
filtered_monthly_reports, today_date = filter_last_month_records(reports)

filtered_monthly_reports = select_and_rename_columns(filtered_monthly_reports)
filtered_monthly_reports["Date added"] = pd.to_datetime(filtered_monthly_reports["Date added"])
filtered_monthly_reports["Date added"] = filtered_monthly_reports["Date added"].dt.strftime("%d/%m/%Y")
filtered_monthly_reports.to_csv(f"{DATA_PATH}/sent/last_month_reports.csv", index=False)

database = reports.copy()
database = select_and_rename_columns(database)
database.to_csv(f"{DATA_PATH}/sent/database.csv", index=False)

write_sum_of_replies_to_log(f"{REPORTS_PATH}/latest.log")
write_monthly_data_to_log(f"{REPORTS_PATH}/latest_last_month.log", filtered_monthly_reports)

name_statuses.rename(
    columns={
        "no. PFDs": "Total PFDs",
        "no. recipients": "sent to count",
        "no. replies": "replies count",
        "no. complete responses": "completed",
        "no. partial responses": "partial",
        "no. overdue responses": "overdue",
        "no. pending responses": "pending",
    },
    inplace=True,
)
name_statuses["% completed"] = name_statuses.apply(
    lambda row: ",".join(str((row["completed"] / row["sent to count"] * 100).round(2)).split("."))
    if row["sent to count"] != 0
    else 0,
    axis=1,
)

area_statuses.rename(
    columns={
        "no. PFDs": "Total PFDs",
        "no. recipients": "Sent to",
        "no. replies": "Replies",
        "no. complete responses": "completed",
        "no. partial responses": "partial",
        "no. overdue responses": "overdue",
        "no. pending responses": "pending",
    },
    inplace=True,
)

area_statuses.index.rename("Coroner area", inplace=True)

area_statuses["% completed"] = area_statuses.apply(
    lambda row: ",".join(str((row["completed"] / row["Sent to"] * 100).round(2)).split("."))
    if row["Sent to"] != 0
    else 0,
    axis=1,
)

area_statuses.to_csv(f"{DATA_PATH}/sent/area-statuses.csv")
name_statuses.to_csv(f"{DATA_PATH}/sent/name-statuses.csv")
rcpt_statuses.to_csv(f"{DATA_PATH}/sent/rcpt-statuses.csv")
