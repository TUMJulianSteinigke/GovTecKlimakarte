from flask import Flask, request, session, redirect, render_template
import folium
from folium import GeoJson
from folium import FeatureGroup

app = Flask(__name__)


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
@app.route('/')
def index():

    m = folium.Map(tiles='stamentoner' ,location=[48.137154, 11.576124], zoom_start=starteZoom, min_zoom=starteZoom, max_zoom=17)


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
    m.get_root().width= "100%"
    m.get_root().height= "100%"

    m._name = 'map'
    m._id = '1'
    m.get_root().html.add_child(folium.JavascriptLink('static/js/polygonListener.js'))
    iframe = m.get_root()._repr_html_()

    return render_template("index.html",iframe=iframe, sideText=render_template("sideElement.html"))

@app.route('/clickEvent', methods=['POST'])
def click():
    cordinates = request.form['cords']
    polygonType = request.form['type']
    print(cordinates)
    print(polygonType)
    pass



app.run()
