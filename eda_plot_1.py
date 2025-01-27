import pandas as pd
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

def plot_invasives_by_waterbody(df):
    """
    Creates a horizontal bar chart showing the total number of invasives by waterbody.
    """
    counts = df['waterbody'].value_counts()
    plt.figure(figsize=(10, 6))
    counts.plot(kind='barh')
    plt.xlabel('Number of Observations')
    plt.ylabel('Waterbody')
    plt.title('Total Number of Invasives Observed by Waterbody')
    plt.tight_layout()
    plt.savefig('Plots/invasives_by_waterbody.png')
    plt.show()

def plot_observations_over_time_by_waterbody(df):
    """
    Creates a line plot of observations per year for each waterbody.
    """
    df['year'] = pd.to_datetime(df['date']).dt.year
    yearly_counts = df.groupby(['year', 'waterbody']).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 6))
    yearly_counts.plot()
    plt.xlabel('Year')
    plt.ylabel('Number of Observations')
    plt.title('Observations Over Time by Waterbody')
    plt.legend(title='Waterbody', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('Plots/observations_over_time_by_waterbody.png')
    plt.show()

def plot_invasives_by_group(df):
    """
    Creates a horizontal bar chart showing the total number of invasives by group.
    """
    counts = df['group'].value_counts()
    plt.figure(figsize=(10, 6))
    counts.plot(kind='barh')
    plt.xlabel('Number of Observations')
    plt.ylabel('Group')
    plt.title('Total Number of Invasives Observed by Group')
    plt.tight_layout()
    plt.savefig('Plots/invasives_by_group.png')
    plt.show()

def plot_observations_over_time_by_group(df):
    """
    Creates a line plot of observations per year for each group.
    """
    df['year'] = pd.to_datetime(df['date']).dt.year
    yearly_counts = df.groupby(['year', 'group']).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 6))
    yearly_counts.plot()
    plt.xlabel('Year')
    plt.ylabel('Number of Observations')
    plt.title('Observations Over Time by Group')
    plt.legend(title='Group', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('Plots/observations_over_time_by_group.png')
    plt.show()

def calculate_density(df, area_ac_dict):
    """
    Calculates invasive density (observations per acre) for each waterbody.
    """
    counts = df['waterbody'].value_counts()
    density = {wb: counts.get(wb, 0) / area_ac_dict[wb] for wb in area_ac_dict.keys()}
    return density

def plot_invasive_density_by_waterbody(df, area_ac_dict):
    """
    Creates a horizontal bar chart showing invasive density (observations per acre) by waterbody.
    """
    density = calculate_density(df, area_ac_dict)
    density_series = pd.Series(density).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    density_series.plot(kind='barh')
    plt.xlabel('Observations per Acre')
    plt.ylabel('Waterbody')
    plt.title('Invasive Density by Waterbody')
    plt.tight_layout()
    plt.savefig('Plots/invasive_density_by_waterbody.png')
    plt.show()

def main():
    # Plot 1: Total number of invasives by waterbody
    plot_invasives_by_waterbody(df)
    
    # Plot 2: Observations over time by waterbody
    plot_observations_over_time_by_waterbody(df)
    
    # Plot 3: Total number of invasives by group
    plot_invasives_by_group(df)
    
    # Plot 4: Observations over time by group
    plot_observations_over_time_by_group(df)
    
    # Plot 5: Invasive density by waterbody
    plot_invasive_density_by_waterbody(df, waterbody_area_ac)

if __name__ == "__main__":
    main()
