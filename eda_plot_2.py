import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data_path = "Invasives/invasive_species.csv"
df = pd.read_csv(data_path)

# Total study area in acres
total_acres = 395687

def preprocess_data(df):
    """
    Preprocesses the data to extract year and ensure valid date handling.
    """
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    return df.dropna(subset=['year'])  # Drop rows without valid year

def plot_observations_per_year(df):
    """
    Plots the number of observations per year as a line plot.
    """
    yearly_counts = df['year'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    yearly_counts.plot(kind='line', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Number of Observations')
    plt.title('Number of Observations Per Year')
    plt.tight_layout()
    plt.savefig('Plots/observations_per_year.png')
    plt.show()

def plot_unique_genus_per_year(df):
    """
    Plots the count of unique genus per year as a line plot.
    """
    unique_genus_per_year = df.groupby('year')['genus'].nunique()
    plt.figure(figsize=(10, 6))
    unique_genus_per_year.plot(kind='line', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Count of Unique Genus')
    plt.title('Count of Unique Genus Per Year')
    plt.tight_layout()
    plt.savefig('Plots/unique_genus_per_year.png')
    plt.show()

def boxplot_observations_per_year(df, total_acres):
    """
    Creates a box and whisker plot of observations per year (normalized by acres)
    and outputs the mean and standard deviation of observations/year/acre.
    """
    yearly_counts = df['year'].value_counts().sort_index() / total_acres
    mean_obs = yearly_counts.mean()
    std_obs = yearly_counts.std()

    plt.figure(figsize=(8, 6))
    plt.boxplot(yearly_counts, vert=False, patch_artist=True)
    plt.xlabel('Observations Per Year Per Acre')
    plt.title('Box and Whisker Plot of Observations Per Year Per Acre')
    plt.tight_layout()
    plt.savefig('Plots/boxplot_observations_per_year_per_acre.png')
    plt.show()

    print(f"Mean Observations Per Year Per Acre: {mean_obs:.6f}")
    print(f"Standard Deviation of Observations Per Year Per Acre: {std_obs:.6f}")

def boxplot_unique_genus_per_year(df, total_acres):
    """
    Creates a box and whisker plot of the count of unique genus per year (normalized by acres)
    and outputs the mean and standard deviation of genus/year/acre.
    """
    unique_genus_per_year = df.groupby('year')['genus'].nunique() / total_acres
    mean_genus = unique_genus_per_year.mean()
    std_genus = unique_genus_per_year.std()

    plt.figure(figsize=(8, 6))
    plt.boxplot(unique_genus_per_year, vert=False, patch_artist=True)
    plt.xlabel('Unique Genus Per Year Per Acre')
    plt.title('Box and Whisker Plot of Unique Genus Per Year Per Acre')
    plt.tight_layout()
    plt.savefig('Plots/boxplot_unique_genus_per_year_per_acre.png')
    plt.show()

    print(f"Mean Unique Genus Per Year Per Acre: {mean_genus:.6f}")
    print(f"Standard Deviation of Unique Genus Per Year Per Acre: {std_genus:.6f}")

def main():
    # Preprocess the data
    df_clean = preprocess_data(df)

    # Plot 1: Observations per year (line plot)
    plot_observations_per_year(df_clean)

    # Plot 2: Unique genus per year (line plot)
    plot_unique_genus_per_year(df_clean)

    # Plot 3: Boxplot of observations per year per acre
    boxplot_observations_per_year(df_clean, total_acres)

    # Plot 4: Boxplot of unique genus per year per acre
    boxplot_unique_genus_per_year(df_clean, total_acres)

if __name__ == "__main__":
    main()
