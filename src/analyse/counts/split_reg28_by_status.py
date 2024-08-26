import os
from datetime import datetime

import pandas as pd

from create_badge import create_badge

PATH = os.path.dirname(__file__)
ALL_DF_PATH = os.path.abspath(f"{PATH}/data/sent/database.csv")
recipient_counts = pd.read_csv(f"{PATH}/data/sent/rcpt-statuses.csv")


def process_completed_df(_main_df: pd.DataFrame) -> None:
    _df_completed = _main_df[(_main_df['Status'] == 'completed')]
    _df_completed.to_csv(f"{PATH}/data/sent/reg28_by_status/completed.csv", index=False)
    _df_completed.loc[:, 'Status'] = _df_completed["Status"].apply(create_badge)
    _df_completed.to_csv(f"{PATH}/data/sent/reg28_by_status/completed_with_badges.csv", index=False)
    counts = recipient_counts.copy()
    counts = counts[['sent_to', 'no. complete responses']]
    filtered_counts = counts[counts['no. complete responses'] != 0]
    sorted_df = filtered_counts.sort_values(by='no. complete responses', ascending=False)
    sorted_df.to_csv(f"{PATH}/data/sent/reg28_by_status/counts/completed_counts.csv", index=False)
    top_30_df = sorted_df.head(30)
    top_30_df.to_csv(f"{PATH}/data/sent/reg28_by_status/counts/top30/top_30_completed_counts.csv", index=False)


def process_overdue_df(_main_df: pd.DataFrame) -> None:
    df = _main_df[(_main_df['Status'] == 'overdue') | (_main_df['Status'] == 'partial')]
    _df_overdue = df.copy()
    _df_overdue.loc[:, 'Date of report'] = pd.to_datetime(_df_overdue['Date of report'], dayfirst=True, format="%d/%m/%Y")
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    _df_overdue.loc[:, 'Days overdue'] = (today - _df_overdue['Date of report'])
    _df_overdue.loc[:, 'Days overdue'] = _df_overdue['Days overdue'].apply(lambda x: x.days - 56)
    _df_overdue = change_col_position("Days overdue", _df_overdue)
    _df_overdue.loc[:, 'Date of report'] = _df_overdue['Date of report'].apply(lambda x: x.strftime("%d/%m/%Y"))
    _df_overdue = _df_overdue.sort_values(by='Days overdue', ascending=False)
    _df_overdue.to_csv(f"{PATH}/data/sent/reg28_by_status/overdue.csv", index=False)
    _df_overdue.loc[:, 'Status'] = _df_overdue["Status"].apply(create_badge)
    _df_overdue.to_csv(f"{PATH}/data/sent/reg28_by_status/overdue_with_badges.csv", index=False)
    counts = recipient_counts.copy()
    counts = counts[['sent_to', 'no. partial responses', 'no. overdue responses']]
    counts.loc[:, 'sum'] = counts['no. partial responses'] + counts['no. overdue responses']
    filtered_counts = counts[(counts['no. partial responses'] != 0) | (counts['no. overdue responses'] != 0)]
    sorted_df = filtered_counts.sort_values(by='sum', ascending=False)
    sorted_df = sorted_df[['sent_to', 'no. overdue responses', 'no. partial responses']]
    sorted_df.to_csv(f"{PATH}/data/sent/reg28_by_status/counts/overdue_counts.csv", index=False)
    top_30_df = sorted_df.head(30)
    top_30_df.to_csv(f"{PATH}/data/sent/reg28_by_status/counts/top30/top_30_overdue_counts.csv", index=False)


def change_col_position(col_name: str, df: pd.DataFrame) -> pd.DataFrame:
    status_idx = df.columns.get_loc("Status")
    cols = df.columns.tolist()
    cols.insert(status_idx + 1, cols.pop(cols.index(col_name)))
    new_df = df[cols]
    return new_df


def process_pending_df(_main_df: pd.DataFrame) -> None:
    df = _main_df[(_main_df["Status"] == "pending")]
    _df_pending = df.copy()
    _df_pending.loc[:, 'Date of report'] = pd.to_datetime(_df_pending['Date of report'], dayfirst=True, format="%d/%m/%Y")
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    _df_pending.loc[:, 'Days left'] = (today - _df_pending['Date of report'])
    _df_pending.loc[:, 'Days left'] = _df_pending['Days left'].apply(lambda x: -(x.days - 56))
    _df_pending = change_col_position("Days left", _df_pending)
    _df_pending.loc[:, 'Date of report'] = _df_pending['Date of report'].apply(lambda x: x.strftime("%d/%m/%Y"))
    _df_pending = _df_pending.sort_values(by='Days left', ascending=True)
    _df_pending.to_csv(f"{PATH}/data/sent/reg28_by_status/pending.csv", index=False)
    _df_pending.loc[:, 'Status'] = _df_pending["Status"].apply(create_badge)
    _df_pending.to_csv(f"{PATH}/data/sent/reg28_by_status/pending_with_badges.csv", index=False)
    counts = recipient_counts.copy()
    counts = counts[['sent_to', 'no. pending responses']]
    sorted_df = counts.sort_values(by='no. pending responses', ascending=False)
    filtered_counts = sorted_df[sorted_df['no. pending responses'] != 0]
    filtered_counts.to_csv(f"{PATH}/data/sent/reg28_by_status/counts/pending_counts.csv", index=False)
    top_30_df = filtered_counts.head(30)
    top_30_df.to_csv(f"{PATH}/data/sent/reg28_by_status/counts/top30/top_30_pending_counts.csv", index=False)


main_df = pd.read_csv(ALL_DF_PATH)

process_overdue_df(main_df)
process_pending_df(main_df)
process_completed_df(main_df)
