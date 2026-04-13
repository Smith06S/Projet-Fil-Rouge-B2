import folium

center = [46.5, 2.5]

m = folium.Map(location=center, zoom_start=5)

url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"

folium.GeoJson(
    url,
    style_function=lambda x: {
    "fillColor": "transparent",
    "color": "transparent",
    "weight": 0,
    "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["nom"],
        aliases=["Département:"]
    )
).add_to(m)

m.save("carte_france.html")

import webbrowser
webbrowser.open("carte_france.html")