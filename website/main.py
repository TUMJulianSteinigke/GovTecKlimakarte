import folium
from folium import GeoJson
from streamlit_folium import st_folium
import geopandas as gpd

import streamlit as st
st.set_page_config(layout="wide")

st.title("HeatTropolis")

# # # # # # # # # # # # # # # # #
#   Setting Layers
# # # # # # # # # # # # # # # # #

def styleGen(color: int):

    return (lambda feature: {f"fillColor": f'"#{0xFFFFFF}"',
        "color": f'"{hex(color)}"',
        "weight": 3})


levels = 3
heatLevels = []
for i in range(levels):
    heatLevels.append(f"heatLevel{i+1}.geojson")


levelColors = [
    "#ffeda0",
    "#feb24c",
    "#f03b20"
    
]

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

    # st.map()
    m = folium.Map(location=[48.137154, 11.576124], zoom_start=starteZoom, min_zoom=starteZoom, max_zoom=17)

    folium.GeoJson(heatLevels[2],
                   zoom_on_click=True,
                   style_function=lambda feature: {
                       "fillColor": levelColors[2],
                       "color": "black",
                       "weight": 2,
                       "dashArray": "5, 5",
                   }
                   ).add_to(m)
    folium.GeoJson(heatLevels[1],
                   zoom_on_click=True,
                   style_function=lambda feature: {
                       "fillColor": levelColors[1],
                       "color": "black",
                       "weight": 2,
                       "dashArray": "5, 5",
                   }
                   ).add_to(m)
    folium.GeoJson(heatLevels[0],
                   zoom_on_click=True,
                   style_function=lambda feature: {
                       "fillColor": levelColors[0],
                       "color": "black",
                       "weight": 2,
                       "dashArray": "5, 5",
                   }
                   ).add_to(m)
    # for i in range():
    #     folium.GeoJson(heatLevels[i],
    #                    zoom_on_click=True,
    #                    style_function=lambda feature: {
    #                        "fillColor": levelColors[i],
    #                        "color": "black",
    #                        "weight": 2,
    #                        "dashArray": "5, 5",
    #                    }
    #                    ).add_to(m)

    st_folium(m)

st.markdown(
    """
    <style>
    .st-emotion-cache-1jicfl2 {
width: 0%;
height:0%;
padding: 100000000rem 10000000rem 100000000rem;
min-width: auto;
max-width: initial;
}
    """,
    unsafe_allow_html=True,
)




