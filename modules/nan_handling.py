import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def drop_rows_with_nan(df: pd.DataFrame, subset=None) -> pd.DataFrame:
    """
    Drop rows that contain NaN values.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        subset (list, optional): List of column names to consider for NaN. If None, all columns are checked.

    Returns:
        pd.DataFrame: DataFrame with specified rows dropped.
    """
    return df.dropna(subset=subset)

def drop_columns_with_nan(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Drop columns with a proportion of NaN values greater than the threshold.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        threshold (float): Maximum allowed proportion of NaNs in a column (between 0 and 1).

    Returns:
        pd.DataFrame: DataFrame with specified columns dropped.
    """
    return df.loc[:, df.isnull().mean() < threshold]

def fill_with_constant(df: pd.DataFrame, value=0) -> pd.DataFrame:
    """
    Fill all NaN values in the DataFrame with a constant.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        value (any): Constant value to replace NaNs.

    Returns:
        pd.DataFrame: DataFrame with NaNs replaced by the given value.
    """
    return df.fillna(value)

def fill_with_mean(df: pd.DataFrame, columns=None) -> pd.DataFrame:
    """
    Fill NaN values in specified or all numeric columns with the column mean.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list, optional): Columns to impute. If None, all numeric columns are used.

    Returns:
        pd.DataFrame: DataFrame with NaNs filled with mean values.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
    return df_copy

def fill_with_median(df: pd.DataFrame, columns=None) -> pd.DataFrame:
    """
    Fill NaN values in specified or all numeric columns with the column median.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list, optional): Columns to impute. If None, all numeric columns are used.

    Returns:
        pd.DataFrame: DataFrame with NaNs filled with median values.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy

def fill_with_mode(df: pd.DataFrame, columns=None) -> pd.DataFrame:
    """
    Fill NaN values in specified or all columns with the column mode.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list, optional): Columns to impute. If None, all columns are used.

    Returns:
        pd.DataFrame: DataFrame with NaNs filled with mode values.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df.columns
    for col in columns:
        mode = df_copy[col].mode()
        if not mode.empty:
            df_copy[col] = df_copy[col].fillna(mode[0])
    return df_copy

def forward_fill(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forward-fill NaN values (propagate last valid value forward).

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with NaNs forward-filled.
    """
    return df.ffill()

def backward_fill(df: pd.DataFrame) -> pd.DataFrame:
    """
    Backward-fill NaN values (propagate next valid value backward).

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with NaNs backward-filled.
    """
    return df.bfill()

def knn_impute(df: pd.DataFrame, n_neighbors=5) -> pd.DataFrame:
    """
    Impute missing values using k-nearest neighbors (KNN) on numeric columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        n_neighbors (int): Number of neighbors to use for imputation.

    Returns:
        pd.DataFrame: DataFrame with numeric columns imputed using KNN.
    """
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_numeric = df.select_dtypes(include=np.number)
    imputed_array = imputer.fit_transform(df_numeric)
    df_imputed = pd.DataFrame(imputed_array, columns=df_numeric.columns, index=df.index)
    df_non_numeric = df.drop(columns=df_numeric.columns)
    return pd.concat([df_imputed, df_non_numeric], axis=1)

def iterative_impute(df: pd.DataFrame, max_iter=10, random_state=0) -> pd.DataFrame:
    """
    Impute missing values using multivariate Iterative Imputer (e.g., MICE) on numeric columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        max_iter (int): Maximum number of imputation iterations.
        random_state (int): Seed for reproducibility.

    Returns:
        pd.DataFrame: DataFrame with numeric columns imputed using iterative method.
    """
    imputer = IterativeImputer(max_iter=max_iter, random_state=random_state)
    df_numeric = df.select_dtypes(include=np.number)
    imputed_array = imputer.fit_transform(df_numeric)
    df_imputed = pd.DataFrame(imputed_array, columns=df_numeric.columns, index=df.index)
    df_non_numeric = df.drop(columns=df_numeric.columns)
    return pd.concat([df_imputed, df_non_numeric], axis=1)

def add_missing_flags(df: pd.DataFrame, columns=None, suffix="_missing") -> pd.DataFrame:
    """
    Add binary indicator columns for missing values.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list, optional): Columns to flag. If None, all columns are considered.
        suffix (str): Suffix to append to original column names for the flags.

    Returns:
        pd.DataFrame: DataFrame with added binary indicator columns.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df.columns
    for col in columns:
        df_copy[f"{col}{suffix}"] = df_copy[col].isna().astype(int)
    return df_copy
