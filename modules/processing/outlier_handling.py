import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def detect_outliers_zscore(df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.DataFrame:
    """
    Detect univariate outliers using Z-score method.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to check.
        threshold (float): Z-score threshold for outlier detection.

    Returns:
        pd.DataFrame: Rows where the column value is an outlier.
    """
    z_scores = zscore(df[column].dropna())
    outliers = df.loc[df[column].dropna().index[np.abs(z_scores) > threshold]]
    return outliers


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Detect univariate outliers using IQR method.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to check.

    Returns:
        pd.DataFrame: Rows where the column value is an outlier.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers


def detect_outliers_isolation_forest(df: pd.DataFrame, contamination: float = 0.01) -> pd.DataFrame:
    """
    Detect multivariate outliers using Isolation Forest.

    Parameters:
        df (pd.DataFrame): Input DataFrame with numeric columns.
        contamination (float): Proportion of expected outliers.

    Returns:
        pd.DataFrame: Rows detected as outliers.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)

    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    preds = iso_forest.fit_predict(scaled_data)
    outliers = df[preds == -1]
    return outliers


def remove_outliers(df: pd.DataFrame, outliers: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows identified as outliers.

    Parameters:
        df (pd.DataFrame): Original DataFrame.
        outliers (pd.DataFrame): DataFrame containing outlier rows.

    Returns:
        pd.DataFrame: Cleaned DataFrame without outliers.
    """
    return df.drop(outliers.index)


def cap_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Cap outliers in a column using the IQR method (Winsorization).

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to cap.

    Returns:
        pd.DataFrame: DataFrame with capped column values.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_copy = df.copy()
    df_copy[column] = df_copy[column].clip(lower=lower_bound, upper=upper_bound)
    return df_copy


def replace_outliers_with_median(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Replace outliers in a column with the median value using IQR method.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to process.

    Returns:
        pd.DataFrame: DataFrame with outliers replaced by the median.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    median = df[column].median()
    df_copy = df.copy()
    mask = (df_copy[column] < lower_bound) | (df_copy[column] > upper_bound)
    df_copy.loc[mask, column] = median
    return df_copy
