import folium
from folium import GeoJson
from streamlit_folium import st_folium

import streamlit as st
st.set_page_config(layout="wide")


# # # # # # # # # # # # # # # # #
#   Setting Layers
# # # # # # # # # # # # # # # # #

levels = 3
heatLevels = []
for i in range(levels):
    heatLevels.append(f"heatLevel{i+1}.geojson")


# # # # # # # # # # # # # # # # #
#   Setting Layers
# # # # # # # # # # # # # # # # #

# MAP
starteZoom = 10.5


# # # # # # # # # # # # # # # # #
#   Layout of Website
# # # # # # # # # # # # # # # # #

text, mapCol = st.columns([1, 3])
with text:
    pass

with mapCol:

    m = folium.Map(location=[48.137154, 11.576124], zoom_start=starteZoom, min_zoom=starteZoom, max_zoom=17)

    for i in range(levels):
        folium.GeoJson(heatLevels[i], zoom_on_click=True).add_to(m)

    st_folium(m)






