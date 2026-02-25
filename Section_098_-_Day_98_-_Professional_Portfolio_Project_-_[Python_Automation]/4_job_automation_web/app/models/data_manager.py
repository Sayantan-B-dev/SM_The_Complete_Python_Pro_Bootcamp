import os
import pandas as pd
from app.config import Config
from pandas.errors import EmptyDataError

INPUT_CSV = os.path.join(Config.INPUT_DIR, 'data.csv')
DEFAULT_COLUMNS = ['Name', 'Email', 'Department', 'Score']  # Customize as needed

def read_data():
    """Return DataFrame from input CSV. If file missing or empty, return default DataFrame."""
    if not os.path.exists(INPUT_CSV) or os.path.getsize(INPUT_CSV) == 0:
        # Create default DataFrame with specified columns
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.to_csv(INPUT_CSV, index=False)
        return df
    try:
        return pd.read_csv(INPUT_CSV)
    except EmptyDataError:
        # File exists but has no columns
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.to_csv(INPUT_CSV, index=False)
        return df

def write_data(df):
    """Write DataFrame to input CSV."""
    df.to_csv(INPUT_CSV, index=False)

def add_row(row_dict):
    df = read_data()
    # Ensure all columns exist (in case row_dict has missing keys)
    new_row = {col: row_dict.get(col, '') for col in df.columns}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    write_data(df)

def update_row(index, row_dict):
    df = read_data()
    if index < len(df):
        for col, val in row_dict.items():
            if col in df.columns:
                df.at[index, col] = val
        write_data(df)

def delete_row(index):
    df = read_data()
    if index < len(df):
        df = df.drop(index).reset_index(drop=True)
        write_data(df)

def append_data(new_df):
    """Append new rows from new_df to existing CSV, aligning columns."""
    existing_df = read_data()
    # Combine, keeping all columns (union)
    combined = pd.concat([existing_df, new_df], ignore_index=True, sort=False)
    # Drop duplicate columns if any (just in case)
    combined = combined.loc[:, ~combined.columns.duplicated()]
    write_data(combined)