import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_bills(df: pd.DataFrame) -> bool:
    passed = True
    if df.empty:
        logger.warning("Validation failed: bills dataframe is empty.")
        return False
    null_ids = df["id"].isnull().sum()
    if null_ids > 0:
        logger.warning(f"Validation warning: {null_ids} bills missing ID.")
        passed = False
    null_titles = df["title"].isnull().sum()
    if null_titles > 0:
        logger.warning(f"Validation warning: {null_titles} bills missing title.")
    duplicate_ids = df["id"].duplicated().sum()
    if duplicate_ids > 0:
        logger.warning(f"Validation warning: {duplicate_ids} duplicate bill IDs found.")
        passed = False
    logger.info(f"Validation complete. Rows: {len(df)}. Passed: {passed}")
    return passed
