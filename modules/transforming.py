import pandas as pd

def absolute_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Applies absolute transformation to specified columns in a DataFrame.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be transformed.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns transformed to their absolute values.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].abs()
    return df

def square_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Applies square transformation to specified columns in a DataFrame.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be transformed.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns transformed by squaring their values.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col] ** 2
    return df

def square_root_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Applies square root transformation to specified columns in a DataFrame.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - columns: list
        List of column names to be transformed.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns transformed by taking their square roots.
    """
    for col in columns:
        if col in df.columns and (df[col] >= 0).all():
            df[col] = df[col].apply(lambda x: x**0.5 if x >= 0 else None)
    return df