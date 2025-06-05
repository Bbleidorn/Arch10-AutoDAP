import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def data_overview(df):
    """
    Prints basic information about the DataFrame including shape, data types,
    missing values, and descriptive statistics.
    
    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    """
    print("Shape:", df.shape)
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nDescriptive Statistics:\n", df.describe(include='all'))

def plot_missing_values(df):
    """
    Displays a heatmap indicating the location of missing values in the DataFrame.
    
    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    """
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title("Missing Values Heatmap")
    plt.show()

def plot_distributions(df, columns=None):
    """
    Plots the distribution of each numeric column in the DataFrame using histograms with KDE.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - columns (list, optional): List of column names to plot. If None, all numeric columns are used.
    """
    columns = columns or df.select_dtypes(include='number').columns
    for col in columns:
        plt.figure()
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribution of {col}")
        plt.show()

def plot_value_counts(df, columns=None):
    """
    Plots bar charts for the value counts of each categorical column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - columns (list, optional): List of column names to plot. If None, all object-type columns are used.
    """
    columns = columns or df.select_dtypes(include='object').columns
    for col in columns:
        plt.figure()
        df[col].value_counts().plot(kind='bar')
        plt.title(f"Value Counts of {col}")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.show()

def plot_boxplots(df, columns=None):
    """
    Plots boxplots for the specified numeric columns to visualize distribution and outliers.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - columns (list, optional): List of column names to plot. If None, all numeric columns are used.
    """
    columns = columns or df.select_dtypes(include='number').columns
    for col in columns:
        plt.figure()
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot of {col}")
        plt.show()
    
def plot_pairplot(df, hue=None):
    """
    Creates a pairplot (scatterplot matrix) for all numeric features in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - hue (str, optional): Column name for color grouping.
    """
    sns.pairplot(df, hue=hue)
    plt.show()

def plot_categorical_target_relation(df, target, cat_columns=None):
    """
    Plots bar charts showing the average target value for each category in the specified columns.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - target (str): The target variable name.
    - cat_columns (list, optional): List of categorical columns. If None, all object-type columns are used.
    """
    cat_columns = cat_columns or df.select_dtypes(include='object').columns
    for col in cat_columns:
        plt.figure()
        sns.barplot(x=col, y=target, data=df)
        plt.title(f"{col} vs {target}")
        plt.xticks(rotation=45)
        plt.show()

def correlation_with_target(df, target):
    """
    Returns the correlation of all numeric features with the specified target column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - target (str): The target variable name.

    Returns:
    - pd.Series: Correlation coefficients sorted in descending order.
    """
    return df.corr()[target].sort_values(ascending=False)

def plot_target_distribution(df, target):
    """
    Plots the distribution of the target variable using a histogram or bar plot,
    depending on the number of unique values.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - target (str): The target variable name.
    """
    plt.figure()
    if df[target].nunique() < 10:
        sns.countplot(x=target, data=df)
    else:
        sns.histplot(df[target], kde=True)
    plt.title(f"Distribution of Target: {target}")
    plt.show()

def plot_correlation_matrix(df, method='pearson', figsize=(10, 8), annot=True, cmap='coolwarm'):
    """
    Plots a correlation matrix heatmap for a given DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - method (str): Correlation method - 'pearson', 'spearman', or 'kendall'.
    - figsize (tuple): Size of the heatmap figure.
    - annot (bool): Whether to annotate the heatmap cells with correlation coefficients.
    - cmap (str): Colormap to use for the heatmap.
    """
    # Compute the correlation matrix
    corr = df.corr(method=method)

    # Plot the heatmap
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot, fmt=".2f", cmap=cmap, square=True, cbar=True)
    plt.title(f'{method.capitalize()} Correlation Matrix')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()
