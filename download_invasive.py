import requests
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Updated HUC8 list
huc8_list = ["03100202", "03100203", "03100204", "03100205", "03100206", "03100207"]

# Paths to shapefiles
aoi_path = "AOI/tb_aoi_1mi_4326.shp"
waterbody_path = "AOI/tb_wb_1mi_4326.shp"

# Base API URL
base_url = "https://nas.er.usgs.gov/api/v2/occurrence/search"

# Mapping for group name changes
group_name_changes = {
    "Amphibians-Frogs": "Amphibians",
    "Crustaceans-Crabs": "Crustaceans",
    "Marine Fishes": "Fishes",
    "Mollusks-Bivalves": "Mollusks",
    "Mollusks-Gastropods": "Mollusks",
    "Reptiles-Lizards": "Reptiles",
    "Reptiles-Snakes": "Reptiles",
    "Reptiles-Turtles": "Reptiles",
}

def fetch_invasive_species_data(huc8_list):
    """
    Fetches invasive species data from the API for a list of HUC8 basins.
    """
    combined_results = []
    for huc8 in huc8_list:
        response = requests.get(f"{base_url}?huc8={huc8}")
        if response.status_code == 200:
            data = response.json()
            combined_results.extend(data.get("results", []))
        else:
            print(f"Failed to fetch data for HUC8: {huc8}")
    return combined_results

def clean_and_format_dates(df):
    """
    Cleans and formats the date field using year, month, and day.
    - Drops rows with missing year.
    - Fills missing months with 6 (June).
    - Fills missing days with 15.
    """
    # Drop rows with missing year
    df = df[df['year'].notna()]
    
    # Fill missing months and days
    df['month'] = df['month'].fillna(6).astype(int)
    df['day'] = df['day'].fillna(15).astype(int)
    
    # Construct a consistent date field
    df['date'] = df.apply(lambda row: f"{int(row['year'])}-{row['month']:02d}-{row['day']:02d}", axis=1)
    return df

def rename_groups(df, group_name_changes):
    """
    Renames the group field based on a mapping of old to new names.
    """
    df['group'] = df['group'].replace(group_name_changes)
    return df

def clip_to_aoi(gdf, aoi_path):
    """
    Clips the GeoDataFrame to the extent of an area-of-interest (AOI) shapefile.
    """
    # Load the AOI shapefile
    aoi = gpd.read_file(aoi_path)
    
    # Ensure both datasets have the same CRS
    gdf = gdf.to_crs(aoi.crs)
    
    # Clip the GeoDataFrame to the AOI
    clipped_gdf = gpd.clip(gdf, aoi)
    return clipped_gdf

def filter_by_year(gdf, min_year=2000):
    """
    Filters the GeoDataFrame to include only observations since the specified year.
    """
    gdf = gdf[gdf['year'] >= min_year]
    return gdf

def add_waterbody_name(gdf, waterbody_path):
    """
    Adds a waterbody name to each feature based on the waterbody shapefile.
    """
    # Load the waterbody shapefile
    waterbodies = gpd.read_file(waterbody_path)
    
    # Ensure both datasets have the same CRS
    gdf = gdf.to_crs(waterbodies.crs)
    
    # Perform spatial join to assign waterbody names
    gdf = gpd.sjoin(gdf, waterbodies[['geometry', 'WATERBODYN']], how="left", predicate="intersects")
    
    # Rename the waterbody name column
    gdf.rename(columns={'WATERBODYN': 'waterbody'}, inplace=True)
    
    return gdf

def json_to_geojson_and_csv(data):
    """
    Converts JSON data to a GeoDataFrame, clips it to the AOI, filters, adds waterbody names, and outputs GeoJSON and CSV.
    """
    # Create a DataFrame from the results
    df = pd.DataFrame(data)
    
    # Clean and format the date field
    df = clean_and_format_dates(df)
    
    # Rename groups
    df = rename_groups(df, group_name_changes)
    
    # Create GeoDataFrame using latitude and longitude
    gdf = gpd.GeoDataFrame(
        df,
        geometry=df.apply(lambda row: Point(row['decimalLongitude'], row['decimalLatitude']), axis=1),
        crs="EPSG:4326"
    )
    
    # Clip the GeoDataFrame to the AOI
    gdf = clip_to_aoi(gdf, aoi_path)
    
    # Filter observations since the year 2000
    gdf = filter_by_year(gdf, min_year=2000)
    
    # Add waterbody name
    gdf = add_waterbody_name(gdf, waterbody_path)
    
    # Select and rename columns for the GeoJSON and CSV output
    columns_to_include = [
        'speciesID', 'group', 'family', 'genus', 'species', 'scientificName', 'commonName',
        'decimalLatitude', 'decimalLongitude', 'date', 'status', 'recordType', 'freshMarineIntro',
        'waterbody', 'geometry'
    ]
    gdf = gdf[columns_to_include]
    
    # Save GeoJSON
    geojson_file = "Invasives/invasive_species.geojson"
    gdf.to_file(geojson_file, driver="GeoJSON")
    print(f"GeoJSON saved to {geojson_file}")
    
    # Save CSV (drop the geometry column)
    csv_file = "Invasives/invasive_species.csv"
    gdf.drop(columns=['geometry']).to_csv(csv_file, index=False)
    print(f"CSV saved to {csv_file}")

def main():
    # Step 1: Fetch data
    data = fetch_invasive_species_data(huc8_list)
    
    # Step 2: Convert JSON to GeoJSON and CSV
    json_to_geojson_and_csv(data)

if __name__ == "__main__":
    main()
