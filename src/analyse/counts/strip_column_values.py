import os
import pandas as pd

PATH = os.path.dirname(__file__)
C_REPORTS_PATH = os.path.abspath(f"{PATH}/../../data/reports-corrected.csv")
A_REPORTS_PATH = os.path.abspath(f"{PATH}/../../data/reports-analysed.csv")


def clean_csv_with_pandas(file: str):
    df = pd.read_csv(file)
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    df.to_csv(file, index=False)
    print(f"{file} cleaned successfully.")


clean_csv_with_pandas(C_REPORTS_PATH)
clean_csv_with_pandas(A_REPORTS_PATH)
