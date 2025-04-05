// Initialize the map centered on SWFWMD region
var map = L.map('map').setView([27.9, -82.5], 8);

// Define NLCD tile layers using relative paths
var nlcd2011 = L.tileLayer('tiles/2011/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'NLCD 2011'
});

var nlcd2023 = L.tileLayer('tiles/2023/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'NLCD 2023'
});

// Add one NLCD layer by default (e.g., 2023)
nlcd2023.addTo(map);

// Create an object for base layers to use in the layer control
var baseLayers = {
  "NLCD 2011": nlcd2011,
  "NLCD 2023": nlcd2023
};

// Initialize layer control without overlays for now
var layerControl = L.control.layers(baseLayers, {}, { collapsed: false }).addTo(map);

// Load the external GeoJSON change layer asynchronously using fetch
fetch('data/2011.geojson')
  .then(response => response.json())
  .then(geojsonData => {
    // Create the GeoJSON layer with custom styling
    var changeLayer = L.geoJSON(geojsonData, {
      style: function(feature) {
        return {
          color: 'red',
          weight: 2,
          fillOpacity: 0.4
        };
      },
      onEachFeature: function(feature, layer) {
        layer.bindPopup("Change Area");
      }
    }).addTo(map);

    // Bring the change layer to the front
    changeLayer.bringToFront();

    // Add the change layer to the layer control as an overlay
    layerControl.addOverlay(changeLayer, "Change Areas (2011-2023)");
  })
  .catch(error => console.error('Error loading GeoJSON:', error));