// Create two separate map instances, one for each year
var map2011 = L.map('map2011').setView([27.9, -82.5], 8);
var map2023 = L.map('map2023').setView([27.9, -82.5], 8);

// Add NLCD 2011 tile layer to the 2011 map
L.tileLayer('tiles/2011/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'NLCD 2011'
}).addTo(map2011);

// Add NLCD 2023 tile layer to the 2023 map
L.tileLayer('tiles/2023/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'NLCD 2023'
}).addTo(map2023);