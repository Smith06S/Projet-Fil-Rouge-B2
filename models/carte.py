import folium
from models.bien import BienRepository
from database import Database

def generer_carte_biens():
	db = Database().get_connection()
	repo = BienRepository(db)
	biens = repo.find_all()  # suppose que chaque bien a ville et adresse

	# Centre de la carte (France)
	center = [46.5, 2.5]
	m = folium.Map(location=center, zoom_start=5)

	for bien in biens:
		# Ici, il faut que chaque bien ait latitude et longitude. Si tu n'as que la ville, il faut géocoder.
		# Pour l'exemple, on suppose bien.latitude et bien.longitude
		if hasattr(bien, 'latitude') and hasattr(bien, 'longitude') and bien.latitude and bien.longitude:
			folium.Marker(
				location=[bien.latitude, bien.longitude],
				popup=f"{bien.ville}, {bien.adresse}",
				tooltip=bien.description
			).add_to(m)
	# Sauvegarde la carte dans templates/carte_dyn.html
	m.save("templates/carte_dyn.html")
	db.close()






import folium
import requests
import webbrowser
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union
import geojson

# Centre de la carte
center = [46.5, 2.5]
m = folium.Map(location=center, zoom_start=5)

# GeoJSON des régions
url_regions = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"
regions_geojson = requests.get(url_regions).json()

# Fusionner toutes les régions en un seul polygone
polygons = []
for feature in regions_geojson['features']:
    geom = shape(feature['geometry'])
    if isinstance(geom, Polygon):
        polygons.append(geom)
    elif isinstance(geom, MultiPolygon):
        polygons.extend(geom.geoms)

france_union = unary_union(polygons)

# Créer un grand polygone du monde
world = Polygon([[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]])

# Soustraire la France pour créer le masque
mask = world.difference(france_union)

# Ajouter le masque sombre
folium.GeoJson(
    geojson.Feature(geometry=mask),
    style_function=lambda x: {
        "fillColor": "black",
        "fillOpacity": 0.6,
        "color": "black",
        "weight": 0
    }
).add_to(m)

# Ajout des contours des régions
folium.GeoJson(
    regions_geojson,
    style_function=lambda x: {
        "fillColor": "transparent",
        "weight": 0
    }
).add_to(m)

# --- Ajout du pin personnalisé à Paris ---
paris_coords = [48.8566, 2.3522]  # latitude et longitude de Paris

icon = folium.CustomIcon(
    "images/pin_rouge.png",  # chemin vers ton image
    icon_size=(50, 50)  # taille du pin
)

folium.Marker(
    location=paris_coords,
    icon=icon,
    tooltip="Paris"
).add_to(m)

# Sauvegarde et ouverture
m.save("carte_france_masque_pin.html")
webbrowser.open("carte_france_masque_pin.html")
