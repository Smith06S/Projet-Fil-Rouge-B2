import folium
import requests
import geojson
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union
from models.bien import BienRepository
from database import Database

def obtenir_coordonnees(adresse, ville):
    """Transforme une adresse en coordonnées GPS via l'API Adresse gouv.fr"""
    query = f"{adresse} {ville}"
    url = f"https://api-adresse.data.gouv.fr/search/?q={query}&limit=1"
    try:
        response = requests.get(url, timeout=5).json()
        if response['features']:
            # L'API renvoie [Longitude, Latitude]
            lon, lat = response['features'][0]['geometry']['coordinates']
            return lat, lon
    except Exception as e:
        print(f"Erreur géocodage pour {query}: {e}")
    return None, None

def generer_carte_biens():
    # 1. Connexion et récupération des biens
    db = Database().get_connection()
    repo = BienRepository(db)
    biens = repo.find_all() # Récupère id, ville, adresse, description, etc.[cite: 4]

    # 2. Création de la carte
    center = [46.5, 2.5]
    m = folium.Map(location=center, zoom_start=6, tiles="OpenStreetMap")

    # 3. Masque sombre sur la France (Visuel)
    url_regions = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"
    try:
        regions_geojson = requests.get(url_regions).json()
        polygons = [shape(f['geometry']) for f in regions_geojson['features']]
        france_union = unary_union(polygons)
        world = Polygon([[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]])
        mask = world.difference(france_union)

        folium.GeoJson(
            geojson.Feature(geometry=mask),
            style_function=lambda x: {"fillColor": "black", "fillOpacity": 0.6, "color": "black", "weight": 0}
        ).add_to(m)

        folium.GeoJson(
            regions_geojson,
            style_function=lambda x: {"fillColor": "transparent", "color": "#ffffff", "weight": 1}
        ).add_to(m)
    except Exception as e:
        print(f"Erreur chargement GeoJSON: {e}")

    # 4. Ajout des marqueurs avec géocodage automatique
    for bien in biens:
        # On vérifie si l'objet bien a déjà lat/lon, sinon on cherche via l'adresse
        lat = getattr(bien, 'latitude', None)
        lon = getattr(bien, 'longitude', None)

        if not lat or not lon:
            lat, lon = obtenir_coordonnees(bien.adresse, bien.ville)

        if lat and lon:
            popup_content = f"<b>{bien.type_bien}</b><br>{bien.adresse}<br>{bien.ville}"
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"Voir : {bien.ville}",
                icon=folium.Icon(color="red", icon="home")
            ).add_to(m)

    # 5. Sauvegarde pour le template Flask[cite: 1]
    m.save("templates/carte_dyn.html")
    db.close()
    print("Carte mise à jour avec succès.")