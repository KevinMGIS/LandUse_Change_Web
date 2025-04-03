import folium
import json

# ---------------------------
# Step 1: Initialize the Map
# ---------------------------
# Center the map on the SWFWMD region; adjust latitude/longitude as needed.
m = folium.Map(location=[27.9, -82.5], zoom_start=8, tiles='OpenStreetMap')

# ---------------------------
# Step 2: Add NLCD Tile Layers
# ---------------------------
nlcd_2011 = folium.raster_layers.TileLayer(
    tiles='tiles/2011/{z}/{x}/{y}.png',
    attr='NLCD 2011',
    name='NLCD 2011',
    overlay=True,
    control=True
)
nlcd_2011.add_to(m)

nlcd_2023 = folium.raster_layers.TileLayer(
    tiles='tiles/2023/{z}/{x}/{y}.png',
    attr='NLCD 2023',
    name='NLCD 2023',
    overlay=True,
    control=True
)
# Optionally, add one of these layers as the default display
nlcd_2023.add_to(m)

# ---------------------------
# Step 3: Add the Change Layer (GeoJSON)
# ---------------------------
# Load the GeoJSON file containing your vectorized change polygons.
with open('data/2011.geojson', 'r') as f:
    change_data = json.load(f)

folium.GeoJson(
    change_data,
    name='Change Areas (2011-2023)',
    style_function=lambda feature: {
        'color': 'red',
        'weight': 2,
        'fillColor': 'red',
        'fillOpacity': 0.4
    }
).add_to(m)

# ---------------------------
# Step 4: Add Layer Controls
# ---------------------------
# Create layer controls to allow toggling between the two NLCD layers and the change overlay.
folium.LayerControl(collapsed=False).add_to(m)

# ---------------------------
# Step 5: Save the Map to index.html
# ---------------------------
m.save('index.html')
print("Map has been saved to index.html")