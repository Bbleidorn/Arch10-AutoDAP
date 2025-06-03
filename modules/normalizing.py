import pandas as pd
import numpy as np

def z_normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Standardizes specified columns in a DataFrame using z-score normalization.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be standardized.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns standardized.
    """
    for col in columns:
        if col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            df[col] = (df[col] - mean) / std
    return df

def min_max_normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalizes specified columns in a DataFrame using min-max normalization.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be normalized.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns normalized.
    """
    for col in columns:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            df[col] = (df[col] - min_val) / (max_val - min_val)
    return df

def robust_normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalizes specified columns in a DataFrame using robust normalization (median and IQR).

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be normalized.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns normalized.
    """
    for col in columns:
        if col in df.columns:
            median = df[col].median()
            iqr = df[col].quantile(0.75) - df[col].quantile(0.25)
            df[col] = (df[col] - median) / iqr
    return df

def log_normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Applies log normalization to specified columns in a DataFrame.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be log normalized.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns log normalized.
    """
    for col in columns:
        if col in df.columns and (df[col] > 0).all():
            df[col] = df[col].apply(lambda x: np.log(x))
    return df

def quantile_normalize(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Applies quantile normalization to specified columns in a DataFrame.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be quantile normalized.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns quantile normalized.
    """
    for col in columns:
        if col in df.columns:
            sorted_col = np.sort(df[col])
            rank = np.argsort(np.argsort(df[col]))
            df[col] = sorted_col[rank]
    return df
