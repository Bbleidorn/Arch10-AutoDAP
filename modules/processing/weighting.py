import pandas as pd
import numpy as np
import warnings

def rake_weights(sample_df: pd.DataFrame, target_df: pd.DataFrame, strata: list, max_iter:int=20, tol:float=1e-6) -> pd.Series:
    """
    Rakes sample_df to match the unweighted marginal distributions in target_df.

    Parameters:
    - sample_df: DataFrame to reweight
    - target_df: Target population DataFrame (unweighted)
    - strata: List of column names to rake on (in order)
    - max_iter: Max iterations per variable
    - tol: Convergence tolerance

    Returns:
    - Dataframe with a new column "Rake_Weights" containing the calculated weights.
    """

    target_marginals = [
        target_df[col].value_counts(normalize=True) for col in strata
    ]

    return _rake(sample_df, strata, target_marginals, max_iter=max_iter, tol=tol)

def rake_weights_weighted(sample_df: pd.DataFrame, target_df: pd.DataFrame, strata:list, weight_col:str, max_iter:int=20, tol:float=1e-6) -> pd.Series:
    """
    Rakes sample_df to match weighted marginal distributions derived from aggregated census data.

    Parameters:
    - sample_df: DataFrame to reweight
    - target_df: Target population DataFrame with one row per unique combination of variables
    - strata: List of column names to rake on (in order)
    - weight_col: Column in target_df_joint with counts for each combination
    - max_iter: Max iterations per variable
    - tol: Convergence tolerance

    Returns:
    - Dataframe with a new column "Rake_Weights" containing the calculated weights.
    """
    target_marginals = [
        target_df.groupby(col)[weight_col].sum() / target_df[weight_col].sum()
        for col in strata
    ]
    
    return _rake(sample_df, strata, target_marginals, max_iter=max_iter, tol=tol)


def _rake(sample_df: pd.DataFrame, strata: pd.DataFrame, target_marginals: list, max_iter:int, tol:float) -> pd.Series:
    """
    Shared raking logic. Matches sample_df marginals to the given target distributions.

    Parameters:
    - sample_df: DataFrame to reweight
    - strata: Columns to rake on (in order)
    - target_marginals: List of Series of target proportions (one per column)
    - max_iter: Max iterations per column
    - tol: Convergence tolerance

    Returns:
    - Dataframe with a new column "Rake_Weights" containing the calculated weights.
    """
    weights = pd.Series(np.ones(len(sample_df)), index=sample_df.index)

    for col, target_dist in zip(strata, target_marginals):
        for _ in range(max_iter):
            # Current weighted marginal
            sample_dist = weights.groupby(sample_df[col]).sum() / weights.sum()

            # Adjustment factors
            adjustment = target_dist / sample_dist
            adjustment = adjustment.replace([np.inf, -np.inf], 0).fillna(0)
            missing_categories = target_dist.index.difference(sample_df[col].unique())
            if not missing_categories.empty:
                warnings.warn(f"Missing categories in sample for column '{col}': {missing_categories.tolist()}")

            new_weights = weights * sample_df[col].map(adjustment).fillna(1)
            new_weights = new_weights.clip(upper=10 * new_weights.mean())

            if np.max(np.abs(new_weights - weights)) < tol:
                break

            weights = new_weights
    sample_df["Rake_Weights"] = weights
    return sample_df


def poststratify_weights(sample_df: pd.DataFrame, target_df: pd.DataFrame, strata: list) -> pd.Series:
    """
    Post-stratifies sample_df to match the marginal distributions in target_df.
    Parameters:
    - sample_df: DataFrame to reweight
    - target_df: Target population DataFrame (unweighted)
    - strata: List of column names to post-stratify on (in order)
    Returns:
    - Series of weights indexed like sample_df
    """
    target_dist = target_df.groupby(strata).size() / len(target_df)
    return _poststratify(sample_df, strata, target_dist)

def poststratify_weights_weighted(sample_df: pd.DataFrame, target_df: pd.DataFrame, strata: list, weight_col: str) -> pd.Series: 
    """
    Post-stratifies sample_df to match the weighted marginal distributions derived from aggregated census data.
    Parameters:
    - sample_df: DataFrame to reweight
    - target_df: Target population DataFrame with one row per unique combination of variables
    - strata: List of column names to post-stratify on (in order)
    - weight_col: Column in target_df with counts for each combination
    Returns:
    - Series of weights indexed like sample_df
    """
    target_dist = target_df.groupby(strata)[weight_col].sum() / target_df[weight_col].sum()
    return _poststratify(sample_df, strata, target_dist)

def _poststratify(sample_df: pd.DataFrame, strata: list, target_dist: pd.Series) -> pd.Series:
    """
    Shared post-stratification logic. Matches sample_df marginals to the given target distribution.
    Parameters:
    - sample_df: DataFrame to reweight
    - strata: strata to post-stratify on (in order)
    - target_dist: Series of target proportions indexed by the unique combinations of the strata
    Returns:
    - Series of weights indexed like sample_df
    """
    sample_dist = sample_df.groupby(strata).size() / len(sample_df)

    weight_factors = target_dist / sample_dist
    weight_factors = weight_factors.replace([np.inf, -np.inf], 0).fillna(0)
    max_weight = 10 * weight_factors.mean()
    weight_factors = weight_factors.clip(upper=max_weight)
    missing_strata = target_dist.index.difference(sample_dist.index)
    if not missing_strata.empty:
        warnings.warn(f"Missing strata in sample: {missing_strata.tolist()}")

    sample_df_key = pd.MultiIndex.from_frame(sample_df[strata])
    return pd.Series(sample_df_key.map(weight_factors.values), index=sample_df.index)

def apply_weights(
    sample_df: pd.DataFrame,
    target_df: pd.DataFrame,
    strata: list,
    method: str = "rake",
    weight_col: str = None,
    max_iter: int = 20,
    tol: float = 1e-6
) -> pd.DataFrame:
    """
    Applies raking or post-stratification weights to a sample DataFrame.

    Parameters:
    - sample_df: DataFrame to reweight
    - target_df: Target population DataFrame
    - strata: List of column names to weight on
    - method: 'rake' or 'poststrat'
    - weight_col: Optional, column in target_df with counts (required for weighted targets)
    - max_iter: Max iterations (only relevant for raking)
    - tol: Convergence tolerance (only relevant for raking)

    Returns:
    - sample_df with an added column 'Rake_Weights' or 'Poststrat_Weights'
    """
    # Validate method
    if method not in {"rake", "poststrat"}:
        raise ValueError("Method must be 'rake' or 'poststrat'.")

    # Validate strata exist in both dataframes
    missing_sample_cols = set(strata) - set(sample_df.strata)
    missing_target_cols = set(strata) - set(target_df.strata)

    if missing_sample_cols:
        raise ValueError(f"Missing strata in sample_df: {missing_sample_cols}")
    if missing_target_cols:
        raise ValueError(f"Missing strata in target_df: {missing_target_cols}")

    # Apply the appropriate method
    if method == "rake":
        if weight_col:
            return rake_weights_weighted(sample_df, target_df, strata, weight_col, max_iter, tol)
        else:
            return rake_weights(sample_df, target_df, strata, max_iter, tol)
    else:  # method == "poststrat"
        if weight_col:
            weights = poststratify_weights_weighted(sample_df, target_df, strata, weight_col)
        else:
            weights = poststratify_weights(sample_df, target_df, strata)
        sample_df["Poststrat_Weights"] = weights
        return sample_df