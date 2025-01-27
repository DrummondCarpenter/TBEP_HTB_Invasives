import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

# File paths
aoi_path = "AOI/tb_aoi_1mi_4326.shp"
invasives_path = "Invasives/invasive_species.geojson"
landscape_score_path = "Landscape/flam_aoi_4326.tif"

def plot_map(aoi_path, invasives_path, landscape_score_path):
    """
    Plots a map with the area of interest, invasives, and landscape score raster.
    """
    # Load AOI shapefile
    aoi = gpd.read_file(aoi_path)

    # Load invasives GeoJSON
    invasives = gpd.read_file(invasives_path)

    # Load landscape score raster
    raster = rasterio.open(landscape_score_path)

    # Define custom colormap for the raster
    cmap = LinearSegmentedColormap.from_list(
        "landscape_score",
        [(0, "purple"), (0.5, "white"), (1, "darkgreen")]
    )

    # Create a plot
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plot raster with the custom colormap
    show(raster, ax=ax, cmap=cmap, alpha=0.75)

    # Plot AOI as a red polygon with no fill
    aoi.boundary.plot(ax=ax, color="red", linewidth=2, label="Area of Interest")

    # Plot invasives as large yellow dots with a black outline
    invasives.plot(
        ax=ax,
        color="yellow",
        edgecolor="black",
        linewidth=0.5,
        markersize=50,
        label="Invasive Species"
    )

    # Add custom legend entries
    raster_patch = mpatches.Patch(
        color=cmap(0.25), label="Landscape Score (0-10)"
    )
    invasive_patch = mpatches.Patch(
        color="yellow", edgecolor="black", label="Invasive Species"
    )
    aoi_patch = mpatches.Patch(
        edgecolor="red", facecolor="none", label="Area of Interest"
    )

    # Combine legend handles
    legend_handles = [raster_patch, aoi_patch, invasive_patch]

    # Add legend
    plt.legend(
        handles=legend_handles,
        loc="upper left",
        title="Legend",
        fontsize=8
    )

    # Add title
    plt.title("Data Sources for Invasive Species Priority Management", fontsize=16)

    # Hide axes for cleaner visualization
    ax.axis("off")

    # Save and show the plot
    plt.savefig("Plots/map_data_sources_priority_management.png", dpi=300, bbox_inches="tight")
    plt.show()

def main():
    plot_map(aoi_path, invasives_path, landscape_score_path)

if __name__ == "__main__":
    main()
