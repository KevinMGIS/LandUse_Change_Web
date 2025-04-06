import geopandas as gpd

# Path to your original GeoJSON file (replace with your actual file path)
input_file = 'data/2011.geojson'

# Read the GeoJSON using GeoPandas
gdf = gpd.read_file(input_file)

# Check the original CRS
print("Original CRS:", gdf.crs)

# Reproject to EPSG:4326 (latitude/longitude)
gdf_4326 = gdf.to_crs(epsg=4326)

# Verify the new CRS
print("Reprojected CRS:", gdf_4326.crs)

# Path for the new GeoJSON file
output_file = 'data/2011_reprojected.geojson'

# Save the reprojected GeoDataFrame as a new GeoJSON file
gdf_4326.to_file(output_file, driver='GeoJSON')

print(f"Reprojected GeoJSON saved to {output_file}")