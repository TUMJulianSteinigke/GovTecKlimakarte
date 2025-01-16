import streamlit as st
import folium
from folium import GeoJson
from streamlit_folium import st_folium

import geopandas as gpd

# Load the GeoJSON file
geojson_file = "UHI_Munich.geojson"  # Path to your GeoJSON file
uhi_data = gpd.read_file(geojson_file)

# Streamlit app
st.title("Urban Heat Islands in Munich")
st.write("Explore Urban Heat Islands (UHIs) and drill down for details.")

# Initialize Folium map
m = folium.Map(location=[48.1351, 11.5820], zoom_start=12)


# Add GeoJSON to the map
def add_uhi_layer(map_obj, geo_data):
    def style_function(feature):
        """Style for the UHI polygons based on severity."""
        severity = feature["properties"]["mean"]  # Replace 'mean' with relevant property
        return {
            "fillColor": "red" if severity > 45 else "orange" if severity > 40 else "yellow",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.7,
        }

    def popup_function(feature):
        """Popup content for drill-down details."""
        return f"""
        <b>Temperature:</b> {feature["properties"]["mean"]} °C<br>
        <b>Severity:</b> High<br>
        <b>Recommended Measures:</b> Tree planting, Cool roofs
        """

    geo_layer = GeoJson(
        geo_data,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["mean"], aliases=["Temperature:"]),
        popup=folium.GeoJsonPopup(fields=[], labels=False, parse_html=True, popup_function=popup_function),
    )
    geo_layer.add_to(map_obj)


add_uhi_layer(m, uhi_data)

# Display the map in Streamlit
st_folium(m, width=700, height=500)

