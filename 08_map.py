import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
name = list(data["NAME"])
elev = list(data["ELEV"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_maker(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 2000:
        return "orange"
    elif 2000 <= elevation < 3000:
        return "red"
    else:
        return "darkred"

map = folium.Map(
    location=(35.5, -98), 
    zoom_start=6, 
    tiles="OpenStreetMap")  # No requiere clave, siquiera se requiere esta línea, es DEFAULT

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                            style_function = lambda x: {"fillColor":"green" if x ["properties"]["POP2005"] < 7500000
                                                         else "yellow" if 7500000 <= x ["properties"]["POP2005"] < 15000000
                                                         else "orange" if 15000000 <= x ["properties"]["POP2005"] < 22500000
                                                           else "red"}))
#los diccionarios son keys de PROPERTIES

fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(
        location=[lt, ln],
        radius=6,
        popup=folium.Popup(iframe),
        fill=True,
        color="grey",
        fill_color=color_maker(el),
        fill_opacity=0.7
    ))




map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())

map.save("Map8.html")