import os

import pandas as pd

PATH = os.path.dirname(__file__)
FRONTEND_DF_PATH = os.path.abspath(f"{PATH}/data/sent/db_with_statuses.csv")
ALL_DF_PATH = os.path.abspath(f"{PATH}/data/sent/database.csv")
MONTH_DF_PATH = os.path.abspath(f"{PATH}/data/sent/last_month_reports.csv")
QUARTER_DF_PATH = os.path.abspath(f"{PATH}/data/sent/last_quarter_reports.csv")

STATIC_1_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Adolescences.xlsx")
STATIC_2_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Autism.xlsx")
STATIC_3_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Cardiovascular diseases _ Anticoagulant.xlsx")
STATIC_4_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Chronic pain.xlsx")
STATIC_5_DF_PATH = os.path.abspath(f"{PATH}/../../tags/COVID-19.xlsx")
STATIC_6_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Drug-related.xlsx")
STATIC_7_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Drug-related _ Opioids.xlsx")
STATIC_8_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Drug-related _ Suicide.xlsx")
STATIC_9_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Opioids _ Drug-related.xlsx")
STATIC_10_DF_PATH = os.path.abspath(f"{PATH}/../../tags/SARS-CoV2.xlsx")
STATIC_11_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Suicide.xlsx")
STATIC_12_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Violence Jul 2013-Jun 2022.xlsx")
STATIC_13_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Violence Jun 2022-Jun 2023.xlsx")
STATIC_14_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Violence Women & Girls_.xlsx")
STATIC_15_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Dog-related.xlsx")

STATIC_16_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Ages 2024-23.xlsx")
STATIC_17_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Cycling 2013-2021.xlsx")

STATIC_WU_18_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Falls.xlsx")
STATIC_WU_19_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Sepsis.xlsx")
STATIC_WU_20_DF_PATH = os.path.abspath(f"{PATH}/../../tags/Clots _ Bleeds.xlsx")

static_1_df = pd.read_excel(STATIC_1_DF_PATH)
static_2_df = pd.read_excel(STATIC_2_DF_PATH)
static_3_df = pd.read_excel(STATIC_3_DF_PATH)
static_4_df = pd.read_excel(STATIC_4_DF_PATH)
static_5_df = pd.read_excel(STATIC_5_DF_PATH)
static_6_df = pd.read_excel(STATIC_6_DF_PATH)
static_7_df = pd.read_excel(STATIC_7_DF_PATH)
static_8_df = pd.read_excel(STATIC_8_DF_PATH)
static_9_df = pd.read_excel(STATIC_9_DF_PATH)
static_10_df = pd.read_excel(STATIC_10_DF_PATH)
static_11_df = pd.read_excel(STATIC_11_DF_PATH)
static_12_df = pd.read_excel(STATIC_12_DF_PATH)
static_13_df = pd.read_excel(STATIC_13_DF_PATH)
static_14_df = pd.read_excel(STATIC_14_DF_PATH)
static_15_df = pd.read_excel(STATIC_15_DF_PATH)

static_16_df = pd.read_excel(STATIC_16_DF_PATH)
static_17_df = pd.read_excel(STATIC_17_DF_PATH)

static_18_df = pd.read_excel(STATIC_WU_18_DF_PATH)
static_19_df = pd.read_excel(STATIC_WU_19_DF_PATH)
static_20_df = pd.read_excel(STATIC_WU_20_DF_PATH)


def update_main_dataframe(main_df: pd.DataFrame, supplementary_dfs: list[pd.DataFrame],
                          with_urls: bool = True) -> pd.DataFrame:
    for column in ['Research tags', 'Number of deceased', 'Date of death', 'Age', 'Sex']:
        if column not in main_df.columns:
            main_df[column] = None

    for supplementary_df in supplementary_dfs:
        for index, row in supplementary_df.iterrows():
            if with_urls:
                url = str(row['URL']).replace('publications', 'prevention-of-future-death-reports')
                try:
                    matching_rows = main_df[main_df['Report URL'] == url]
                except KeyError:
                    matching_rows = main_df[main_df['URL'] == url]
            else:
                matching_rows = main_df[main_df['Deceased name'] == row['Deceased name']]

            for main_index, main_row in matching_rows.iterrows():
                if main_row['Research tags'] is None:
                    value = row.get('research tags', None)
                    if not pd.isna(value):
                        main_df.at[main_index, 'Research tags'] = row.get('research tags', None)
                else:
                    value = row.get('research tags', None)
                    if not pd.isna(value):
                        main_df.at[
                            main_index, 'Research tags'] = f"{main_row['Research tags']} | {row.get('research tags')}"
                deceased_count = row.get('number of deceased', None)
                if not pd.isna(deceased_count):
                    main_df.at[main_index, 'Number of deceased'] = int(deceased_count)
                date_of_death = row.get('date of death', None)
                if not pd.isna(date_of_death):
                    main_df.at[main_index, 'Date of death'] = date_of_death
                age = row.get('age', None)
                if not pd.isna(age):
                    main_df.at[main_index, 'Age'] = str(age)
                sex = row.get('sex', None)
                if not pd.isna(sex):
                    main_df.at[main_index, 'Sex'] = str(sex)

    return main_df


def remove_NR(df: pd.DataFrame) -> pd.DataFrame:
    def func(x):
        if x != 'NR':
            return x

    df['Date of death'] = df['Date of death'].apply(func)
    df['Age'] = df['Age'].apply(func)
    df['Sex'] = df['Sex'].apply(func)
    return df


def round_age(df: pd.DataFrame) -> pd.DataFrame:
    df['Age'] = df['Age'].round(2)
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    def func(x):
        if isinstance(x, str):
            return ' | '.join(set(x.split(' | ')))
        return x

    df['Research tags'] = df['Research tags'].apply(func)
    return df


def convert_column_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df['Date of death'] = pd.to_datetime(df['Date of death'], errors='coerce')
    df['Date of death'] = df['Date of death'].dt.strftime('%d/%m/%Y')
    return df


def new_file_name(file_path: str) -> str:
    return file_path.replace('.csv', '(with_tags).csv')


def run(file_path: str, _dfs: list[pd.DataFrame], _dfs_with_urls: list[pd.DataFrame]) -> None:
    df = pd.read_csv(file_path)
    _df = update_main_dataframe(df, dfs)
    _df = update_main_dataframe(df, _dfs_with_urls, with_urls=False)
    _df = remove_duplicates(_df)
    _df = remove_NR(_df)
    _df = round_age(_df)
    _df = convert_column_to_datetime(_df)
    columns = ['Status', 'Date added', 'Date of report', 'Ref', 'Deceased name', 'Number of deceased',
               'Date of death',
               'Age', 'Sex', 'Coroner name', 'Coroner area', 'Research tags', 'Category', 'Sent to', 'Sent to count',
               'Replies count']
    if file_path == FRONTEND_DF_PATH:
        columns.append('Report URL')
    else:
        columns.append('URL')
    _df = _df.reindex(columns=columns)
    _df.to_csv(new_file_name(file_path), index=False)


dfs = [static_1_df, static_2_df, static_3_df, static_4_df, static_5_df, static_6_df, static_7_df, static_8_df,
       static_9_df, static_10_df, static_11_df, static_12_df, static_13_df, static_14_df, static_15_df, static_16_df, static_17_df]

dfs_2 = [static_18_df, static_19_df, static_20_df]

# files = [FRONTEND_DF_PATH, ALL_DF_PATH, MONTH_DF_PATH, QUARTER_DF_PATH]
files = [ALL_DF_PATH]
for file in files:
    run(file, dfs, dfs_2)
