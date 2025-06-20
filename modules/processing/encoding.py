import pandas as pd

def ordinal_to_numeric(df: pd.DataFrame, ordinal_columns: list, column_mapping: dict) -> pd.DataFrame:
    """
    Preprocess ordinal data by mapping ordinal columns to numerical values.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame containing ordinal data.
    - ordinal_columns: list
        List of columns that contain ordinal data.
    - column_mapping: dict
        Mapping of ordinal categories to numerical values.

    Returns:
    - df: pd.DataFrame
        A DataFrame with ordinal columns converted to numerical values.
    """
    for col in ordinal_columns:
        if col in column_mapping:
            df[col] = df[col].map(column_mapping[col])
    return df


def nominal_to_one_hot(df: pd.DataFrame, nominal_columns: list) -> pd.DataFrame:
    """
    One-hot encodes the specified nominal columns of a DataFrame.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - nominal_columns: list
        List of column names to be one-hot encoded.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified columns one-hot encoded.
    """
    return pd.get_dummies(df, columns=nominal_columns, drop_first=False)

def one_hot_to_nominal(df: pd.DataFrame, original_column: str, one_hot_columns: list) -> pd.DataFrame:
    df[original_column] = df[one_hot_columns].idxmax(axis=1).str.replace(f"{original_column}_", "")
    return df.drop(columns=one_hot_columns)


def numeric_to_categorical(df: pd.DataFrame, numeric_columns: list, bins: dict) -> pd.DataFrame:
    """
    Categorizes numeric columns into bins.

    Parameters:
    - df: pd.DataFrame
        The input DataFrame.
    - numeric_columns: list
        List of column names to be categorized.
    - bins: dict
        Dictionary where keys are column names and values are lists of bin edges.

    Returns:
    - pd.DataFrame
        A DataFrame with the specified numeric columns categorized.
    """
    for col in numeric_columns:
        if col in bins:
            df[col] = pd.cut(df[col], bins=bins[col], labels=False)
    return df