import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data_path = "Invasives/invasive_species.csv"
df = pd.read_csv(data_path)

# Waterbody acreage data
waterbody_area_ac = {
    "OTB": 85541,
    "MTB": 96122,
    "HB": 50774,
    "LTB": 163250
}

# Constants for mean and standard deviation
mean_rate = 0.000063
std_dev = 0.000033

def preprocess_data(df):
    """
    Preprocesses the data to extract year and ensure valid date handling.
    """
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    return df.dropna(subset=['year'])  # Drop rows without valid year

def compute_observations_per_acre(df, waterbody_area_ac):
    """
    Computes the number of observations per acre per year for each waterbody.
    """
    # Count observations per year and waterbody
    yearly_counts = df.groupby(['year', 'waterbody']).size().unstack(fill_value=0)

    # Normalize by waterbody acreage
    obs_per_acre = yearly_counts.div(pd.Series(waterbody_area_ac), axis=1)
    return obs_per_acre

def assign_ryg(obs_per_acre, mean_rate, std_dev):
    """
    Assigns R, Y, or G based on the observations per acre per year.
    """
    # Define thresholds
    high_threshold = mean_rate + std_dev
    low_threshold = mean_rate - std_dev

    # Apply thresholds to assign R, Y, G
    def categorize(value):
        if value > high_threshold:
            return "R"
        elif value < low_threshold:
            return "G"
        else:
            return "Y"

    ryg = obs_per_acre.applymap(categorize)
    return ryg

def plot_report_card(ryg):
    """
    Plots the R/Y/G report card as a color-coded table with a subtitle,
    using equal column widths and scaling the table for better use of space.
    """
    # Define color mapping
    color_map = {"R": "red", "Y": "yellow", "G": "green"}

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8.5, 11))  # Portrait-oriented figure size

    # Convert R/Y/G to colors
    colors = ryg.replace(color_map)

    # Create the table
    table = ax.table(
        cellText=ryg.values,
        rowLabels=ryg.index,
        colLabels=ryg.columns,
        cellColours=colors.values,
        loc="center",
        cellLoc="center",
        bbox=[0, 0, 1, 0.95]  # Adjust to fill figure while leaving space for titles
    )

    # Set equal column widths
    num_cols = len(ryg.columns)
    for col_idx in range(num_cols):
        for (row, col), cell in table.get_celld().items():
            if col < num_cols:  # Avoid modifying row label cells
                cell.set_width(1 / num_cols)

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Remove axes
    ax.axis("off")

    # Add titles
    plt.title("Waterbody Invasive Species Abundance Report Card", fontsize=16)
    plt.suptitle("Based on invasive species observations per acre per year", fontsize=12, y=0.92)
    plt.tight_layout()

    # Save and show the plot
    plt.savefig("Plots/abundance_report_card.png")
    plt.show()


def main():
    # Preprocess the data
    df_clean = preprocess_data(df)

    # Compute observations per acre per year
    obs_per_acre = compute_observations_per_acre(df_clean, waterbody_area_ac)

    # Assign R/Y/G values
    ryg = assign_ryg(obs_per_acre, mean_rate, std_dev)

    # Plot the report card
    plot_report_card(ryg)

if __name__ == "__main__":
    main()
