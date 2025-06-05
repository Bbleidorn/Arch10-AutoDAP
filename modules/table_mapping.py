import pandas as pd
from typing import Dict, Union, List


def apply_column_name_mapping(
    df: pd.DataFrame,
    mapping: Union[Dict[str, str], pd.DataFrame]
) -> pd.DataFrame:
    """
    Rename columns in a DataFrame using a mapping dictionary or a 2-column DataFrame.

    Parameters:
      - df: pd.DataFrame  
          The input DataFrame to be renamed.  
      - mapping: Union[Dict[str, str], pd.DataFrame]  
          Either a dictionary or a 2-column DataFrame mapping original to target column names.

    Returns:
      - pd.DataFrame  
          The DataFrame with renamed columns.
    """
    if isinstance(mapping, pd.DataFrame):
        if mapping.shape[1] != 2:
            raise ValueError("Mapping DataFrame must have exactly 2 columns")
        mapping_dict = dict(zip(mapping.iloc[:, 0], mapping.iloc[:, 1]))
    else:
        mapping_dict = mapping

    return df.rename(columns=mapping_dict)


def apply_value_mapping(
    df: pd.DataFrame,
    value_mappings: Union[Dict[str, Dict], pd.DataFrame],
    columns: List[str] = None
) -> pd.DataFrame:
    """
    Map values in categorical columns using a dictionary or a 2-column DataFrame.

    Parameters:
      - df: pd.DataFrame  
          The DataFrame with values to map.  
      - value_mappings: Union[Dict[str, Dict], pd.DataFrame]  
          Dictionary of column-wise mappings or a 2-column DataFrame for flat mappings.  
      - columns: List[str]  
          Optional. List of columns to restrict value mapping to (used when passing flat 2-col DataFrame).

    Returns:
      - pd.DataFrame  
          DataFrame with values mapped.
    """
    if isinstance(value_mappings, pd.DataFrame):
        if value_mappings.shape[1] != 2:
            raise ValueError("Mapping DataFrame must have exactly 2 columns")
        if columns is None:
            raise ValueError("When using a 2-column DataFrame, you must specify the target columns")
        for col in columns:
            map_dict = dict(zip(value_mappings.iloc[:, 0], value_mappings.iloc[:, 1]))
            df[col] = df[col].map(map_dict)
    else:
        for col, mapping in value_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)

    return df
