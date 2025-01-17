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
                            console.log('fid', properties.fid); 

                            const url = new URL('/clickEvent', window.location.origin);
                            url.searchParams.append('level', JSON.stringify(properties.level));
                            url.searchParams.append('size', JSON.stringify(properties.area));
                            url.searchParams.append('district', JSON.stringify(properties.district));

                            fetch(url, {
                                method: 'GET'
                            })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                response.text().then(data => {
                                    document.getElementById("clickText").innerHTML = data;
                                })
                                return response.text();
                            })
                            .then(data => {
                                console.log('Server response:', data);
                            })
                            .catch(error => {
                                console.error('There was a problem with the fetch operation:', error);
                            });
                        });
                    }
                });
            }
        });
    } else {
        console.error('Map object not found. Ensure your Folium map is correctly initialized.');
    }
});