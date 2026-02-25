import os
import pandas as pd
from app.config import Config
from pandas.errors import EmptyDataError

REPORT_CSV = os.path.join(Config.OUTPUT_DIR, 'report.csv')

def read_report():
    """Return DataFrame from report CSV. If file missing or empty, return empty DataFrame."""
    if not os.path.exists(REPORT_CSV) or os.path.getsize(REPORT_CSV) == 0:
        return pd.DataFrame()
    try:
        # Read with first column as index (because describe() writes the index)
        df = pd.read_csv(REPORT_CSV, index_col=0)
        return df
    except (EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame()

def write_report(df):
    """Write DataFrame to report CSV (including index)."""
    df.to_csv(REPORT_CSV, index=True)  # index=True is default, but explicit is clear