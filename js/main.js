// Create three separate map instances for the three views
var map2011 = L.map('map2011').setView([27.9, -82.5], 8);
var map2023 = L.map('map2023').setView([27.9, -82.5], 8);
var mapChange = L.map('mapChange').setView([27.9, -82.5], 8);

// Add NLCD tile layers to the respective maps
var nlcd2011 = L.tileLayer('tiles/2011/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'NLCD 2011'
}).addTo(map2011);

var nlcd2023 = L.tileLayer('tiles/2023/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'NLCD 2023'
}).addTo(map2023);

// For the change map, load the GeoJSON change layer asynchronously and add it to mapChange
fetch('data/2011.geojson')
  .then(response => response.json())
  .then(geojsonData => {
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
    }).addTo(mapChange);

    // Bring the change layer to the front so it is visible above any base imagery
    changeLayer.bringToFront();
  })
  .catch(error => console.error('Error loading GeoJSON:', error));