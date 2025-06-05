import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

def compare_distributions(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    strata: list,
    weight_col_a: str = None,
    weight_col_b: str = None,
    normalize: bool = True
) -> pd.DataFrame:
    """
    Compares the marginal distributions of given features between two DataFrames.

    Parameters:
    - df_a: First DataFrame (e.g., sample)
    - df_b: Second DataFrame (e.g., target)
    - strata: List of columns (stratification variables) to compare
    - weight_col_a: Optional, weight column for df_a
    - weight_col_b: Optional, weight column for df_b
    - normalize: If True, show proportions (else raw counts)

    Returns:
    - A DataFrame with the distributions from both DataFrames and their absolute differences.
    """
    results = []

    for var in strata:
        if var not in df_a.columns:
            warnings.warn(f"Strata variable '{var}' not found in df_a. Skipping.")
            continue
        if var not in df_b.columns:
            warnings.warn(f"Strata variable '{var}' not found in df_b. Skipping.")
            continue

        if weight_col_a:
            dist_a = df_a.groupby(var)[weight_col_a].sum()
        else:
            dist_a = df_a[var].value_counts()

        if weight_col_b:
            dist_b = df_b.groupby(var)[weight_col_b].sum()
        else:
            dist_b = df_b[var].value_counts()

        if normalize:
            dist_a = dist_a / dist_a.sum()
            dist_b = dist_b / dist_b.sum()

        all_cats = sorted(set(dist_a.index).union(set(dist_b.index)))
        dist_a = dist_a.reindex(all_cats, fill_value=0)
        dist_b = dist_b.reindex(all_cats, fill_value=0)

        merged = pd.DataFrame({
            "Variable": var,
            "Category": all_cats,
            "Dist_A": dist_a.values,
            "Dist_B": dist_b.values
        })
        merged["Abs_Diff"] = (merged["Dist_A"] - merged["Dist_B"]).abs()

        results.append(merged)

    return pd.concat(results, ignore_index=True)


def plot_distribution_comparison(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    strata: list,
    weight_col_a: str = None,
    weight_col_b: str = None,
    normalize: bool = True,
    figsize: tuple = (6, 4)
):
    """
    Plots the marginal distributions of given features for two DataFrames.

    Parameters:
    - df_a, df_b: DataFrames to compare
    - strata: List of columns to compare
    - weight_col_a, weight_col_b: Optional weighting columns for df_a and df_b
    - normalize: Show proportions (default) or raw counts
    - figsize: Size of each subplot
    """
    for var in strata:
        if var not in df_a.columns:
            warnings.warn(f"Strata variable '{var}' not found in df_a. Skipping plot.")
            continue
        if var not in df_b.columns:
            warnings.warn(f"Strata variable '{var}' not found in df_b. Skipping plot.")
            continue

        if weight_col_a:
            dist_a = df_a.groupby(var)[weight_col_a].sum()
        else:
            dist_a = df_a[var].value_counts()

        if weight_col_b:
            dist_b = df_b.groupby(var)[weight_col_b].sum()
        else:
            dist_b = df_b[var].value_counts()

        if normalize:
            dist_a = dist_a / dist_a.sum()
            dist_b = dist_b / dist_b.sum()

        all_cats = sorted(set(dist_a.index).union(set(dist_b.index)))
        dist_a = dist_a.reindex(all_cats, fill_value=0)
        dist_b = dist_b.reindex(all_cats, fill_value=0)

        x = np.arange(len(all_cats))
        width = 0.35

        plt.figure(figsize=figsize)
        plt.bar(x - width / 2, dist_a, width, label='A')
        plt.bar(x + width / 2, dist_b, width, label='B')
        plt.xticks(ticks=x, labels=all_cats, rotation=45)
        plt.ylabel('Proportion' if normalize else 'Count')
        plt.title(f"Distribution of '{var}' in A vs. B")
        plt.legend()
        plt.tight_layout()
        plt.show()
