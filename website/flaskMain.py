import os

from flask import Flask, request, session, redirect, render_template, render_template_string
import folium
from folium import GeoJson
from folium import FeatureGroup
import geopandas as gpd

app = Flask(__name__)


levels = 3
heatLevels = []
for i in range(levels):
    heatLevels.append(f"heatLevel{i+1}.geojson")
    gp = gpd.read_file(heatLevels[i])
    gp["level"] = i
    os.remove(heatLevels[i])
    gp.to_file(heatLevels[i], driver="GeoJson")


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
    return render_template("frontpage.html")

@app.route('/map')
def map():

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
    m.get_root().width= "100%"
    m.get_root().height= "100%"

    m._name = 'map'
    m._id = '1'
    m.get_root().html.add_child(folium.JavascriptLink('static/js/polygonListener.js'))
    
    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    # return render_template_string(
    #     """
    #         <!DOCTYPE html>
    #         <html>
    #             <head>
    #                 {{ header|safe }}
    #             </head>
    #             <body>
    #                 <h1>Using components</h1>
    #                 {{ body_html|safe }}
    #                 <script>
    #                     {{ script|safe }}
    #                 </script>
    #             </body>
    #         </html>
    #     """,
    #     header=header,
    #     body_html=body_html,
    #     script=script,
    # )
    return render_template("index.html", foliumHeader=header, foliumBody=body_html,foliumJs=script)

@app.route('/clickEvent')
def click():
    params = request.args
    
    level = int(params.get("level"))
    size = int(params.get("size"))
    district = params.get("district")
    print(f"Level: {level}")
    print(f"Size: {size}")
    print(f"district: {district}")
    if(level == 0):
        level_string = ' Level ' + str(level + 1) + ' (Low)'
    if(level == 1):
        level_string = ' Level ' + str(level + 1) + ' (Medium)' 
    if(level == 2):
        level_string = ' Level ' + str(level + 1) + ' (High)'    

    size_string = ' ' + str(size / 1000000) +'km²'

    district_string = ' ' + str(district)

    return render_template('sideElement.html', level = level_string, size = size_string, district = district_string)
app.run()
