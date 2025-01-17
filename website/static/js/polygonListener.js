// Add this script to your project and make sure the map is initialized.

document.addEventListener('DOMContentLoaded', () => {
    // Ensure the map object is defined (replace 'map' with your map's variable name)
    if (typeof map_1 !== 'undefined') {
        map_1.eachLayer((layer) => {
            if (layer instanceof L.GeoJSON) {
                layer.eachLayer((featureLayer) => {
                    if (featureLayer.feature.geometry.type === 'Polygon') {
                        featureLayer.on('click', (e) => {
                            const coordinates = e.target.feature.geometry.coordinates;
                            const properties = e.target.feature.properties;

                            console.log('Polygon clicked!');
                            console.log('Coordinates:', coordinates);
                            console.log('Properties:', properties);

                            
                        });
                    }
                });
            }
        });
    } else {
        console.error('Map object not found. Ensure your Folium map is correctly initialized.');
    }
});