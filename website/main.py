import folium
from folium import GeoJson
from folium import FeatureGroup
from streamlit_folium import st_folium
import geopandas as gpd
import streamlit as st

st.set_page_config(layout="wide")

st.title("HeatTropolis")

my_js = """
alert("Hola mundo");
"""

# Wrapt the javascript as html code
my_html = f"<script>{my_js}</script><h1>TEST</h1>"
st.text(my_html)


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
   # "#ffeda0",
   # "#feb24c",
   # "#f03b20"
    '#ffd100',
    '#ff7400',
    '#ff0000'
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
    st.write("**Urban Heat Island Analysis**")
    st.write("""
**Location:** Munich City Center, Maxvorstadt District  
**Estimated Temperature Deviation:** +4.2°C above city average  
**Severity Level:** High (Red Zone)  

**Mitigation Measures:**  
- **Urban Greening:** Plant 250+ trees (€120,000) to reduce temperatures by 1.5°C.  
- **Cool Roofs Initiative:** Retrofit 60,000 m² of rooftops (€450,000) with reflective materials.  
- **Water Features:** Install public fountains (€95,000) for localized cooling.  

**Total Cost:** €665,000  
**Implementation Timeline:** 18 months  
""")


with mapCol:

    # st.map()
    m = folium.Map(location=[48.137154, 11.576124], zoom_start=starteZoom, min_zoom=starteZoom, max_zoom=17)


    folium.GeoJson(heatLevels[0],
                   zoom_on_click=True,
                   style_function=lambda feature: {
                       "fillColor": levelColors[0]+"75",
                       "fillOpacity":1.0,
                       "color": "black",
                       "weight": 2,
                       "dashArray": "5, 5",

                   }
                   ).add_to(m)
    folium.GeoJson(heatLevels[1],
                   zoom_on_click=True,
                   style_function=lambda feature: {
                       "fillColor": levelColors[1]+"75",
                       "fillOpacity":1.0,
                       "color": "black",
                       "weight": 2,
                       "dashArray": "5, 5",

                   }
                   ).add_to(m)
    g = folium.GeoJson(heatLevels[2],
                   zoom_on_click=True,
                   style_function=lambda feature: {
                       "fillColor": levelColors[2]+"75",
                       "fillOpacity":1.0,
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

    st_folium(m, width=1000, height=600)

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




