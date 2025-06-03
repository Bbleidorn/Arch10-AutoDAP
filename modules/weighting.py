import pandas as pd
import numpy as np

def rake_weights(df_sample: pd.DataFrame, df_target: pd.DataFrame, columns: list, max_iter:int=20, tol:float=1e-6) -> pd.Series:
    """
    Rakes df_sample to match the unweighted marginal distributions in df_target.

    Parameters:
    - df_sample: DataFrame to reweight
    - df_target: Target population DataFrame (unweighted)
    - columns: List of column names to rake on (in order)
    - max_iter: Max iterations per variable
    - tol: Convergence tolerance

    Returns:
    - Series of weights indexed like df_sample
    """

    target_distributions = [
        df_target[col].value_counts(normalize=True) for col in columns
    ]

    return _rake(df_sample, columns, target_distributions, max_iter=max_iter, tol=tol)

def rake_weights_with_obs_sums(df_sample: pd.DataFrame, df_target: pd.DataFrame, columns:list, obs_col:str, max_iter:int=20, tol:float=1e-6) -> pd.Series:
    """
    Rakes df_sample to match weighted marginal distributions derived from aggregated census data.

    Parameters:
    - df_sample: DataFrame to reweight
    - df_target: Target population DataFrame with one row per unique combination of variables
    - columns: List of column names to rake on (in order)
    - obs_col: Column in df_target_joint with counts for each combination
    - max_iter: Max iterations per variable
    - tol: Convergence tolerance

    Returns:
    - Series of weights indexed like df_sample
    """
    target_distributions = [
        df_target.groupby(col)[obs_col].sum() / df_target[obs_col].sum()
        for col in columns
    ]
    
    return _rake(df_sample, columns, target_distributions, max_iter=max_iter, tol=tol)


def _rake(df_sample: pd.DataFrame, columns: pd.DataFrame, target_distributions: list, max_iter:int, tol:float) -> pd.Series:
    """
    Shared raking logic. Matches df_sample marginals to the given target distributions.

    Parameters:
    - df_sample: DataFrame to reweight
    - columns: Columns to rake on (in order)
    - target_distributions: List of Series of target proportions (one per column)
    - max_iter: Max iterations per column
    - tol: Convergence tolerance

    Returns:
    - Dataframe with a new column "Rake_Weights" containing the calculated weights.
    """
    weights = pd.Series(np.ones(len(df_sample)), index=df_sample.index)

    for col, target_dist in zip(columns, target_distributions):
        for _ in range(max_iter):
            # Current weighted marginal
            sample_dist = (
                df_sample[col]
                .groupby(df_sample[col])
                .apply(lambda g: weights[g.index].sum())
            )
            sample_dist /= weights.sum()

            # Adjustment factors
            adjustment = target_dist / sample_dist
            adjustment = adjustment.replace([np.inf, -np.inf], 0).fillna(0)

            new_weights = weights.copy()
            for category, factor in adjustment.items():
                new_weights[df_sample[col] == category] *= factor

            if np.max(np.abs(new_weights - weights)) < tol:
                break

            weights = new_weights
    df_sample["Rake_Weights"] = weights
    return df_sample


def poststratify_weights(df_sample: pd.DataFrame, df_target: pd.DataFrame, columns: list) -> pd.Series:
    """
    Post-stratifies df_sample to match the marginal distributions in df_target.
    Parameters:
    - df_sample: DataFrame to reweight
    - df_target: Target population DataFrame (unweighted)
    - columns: List of column names to post-stratify on (in order)
    Returns:
    - Series of weights indexed like df_sample
    """
    target_dist = df_target.groupby(columns).size() / len(df_target)
    return _poststratify(df_sample, columns, target_dist)

def poststratify_weights_with_obs_sums(df_sample: pd.DataFrame, df_target: pd.DataFrame, columns: list, obs_col: str) -> pd.Series: 
    """
    Post-stratifies df_sample to match the weighted marginal distributions derived from aggregated census data.
    Parameters:
    - df_sample: DataFrame to reweight
    - df_target: Target population DataFrame with one row per unique combination of variables
    - columns: List of column names to post-stratify on (in order)
    - obs_col: Column in df_target with counts for each combination
    Returns:
    - Series of weights indexed like df_sample
    """
    target_dist = df_target.groupby(columns)[obs_col].sum() / df_target[obs_col].sum()
    return _poststratify(df_sample, columns, target_dist)

def _poststratify(df_sample: pd.DataFrame, columns: list, target_dist: pd.Series) -> pd.Series:
    """
    Shared post-stratification logic. Matches df_sample marginals to the given target distribution.
    Parameters:
    - df_sample: DataFrame to reweight
    - columns: Columns to post-stratify on (in order)
    - target_dist: Series of target proportions indexed by the unique combinations of the columns
    Returns:
    - Series of weights indexed like df_sample
    """
    sample_dist = df_sample.groupby(columns).size() / len(df_sample)
    weight_factors = target_dist / sample_dist
    weight_factors = weight_factors.replace([np.inf, -np.inf], 0).fillna(0)

    df_sample_key = df_sample[columns].apply(lambda row: tuple(row), axis=1)
    return df_sample_key.map(weight_factors)

