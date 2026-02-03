# data_loader.py
import pandas as pd
from .. import config

def load_sheet(sheet_name: str, usecols=None) -> pd.DataFrame | None:
    """
    Load a worksheet from the configured Excel file.

    Args:
        sheet_name: Name of the sheet to load.
        usecols: Range of columns to load.

    Returns:
        A Pandas DataFrame, or None if failed.
    """
    print(f"Loading sheet: '{sheet_name}'...")
    try:
        df = pd.read_excel(config.INPUT_FILE, sheet_name=sheet_name, usecols=usecols)
        # Replace ODPS null value '\N' with 0
        df = df.replace(r'\N', 0).infer_objects(copy=False)
        print(f"Successfully loaded and cleaned sheet: '{sheet_name}'.")
        return df
    except FileNotFoundError:
        print(f"ERROR: Input file not found at '{config.INPUT_FILE}'.")
        print("Please check the INPUT_FILE path in config.py.")
        return None
    except ValueError as e:
        print(f"ERROR: Sheet '{sheet_name}' not found in the Excel file. Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading sheet '{sheet_name}': {e}")
        return None