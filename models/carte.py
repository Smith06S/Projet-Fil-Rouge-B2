import folium
import requests

def obtenir_coordonnees(adresse, ville):
    query = f"{adresse} {ville}"
    url = f"https://api-adresse.data.gouv.fr/search/?q={query}&limit=1"
    try:
        response = requests.get(url, timeout=5).json()
        if response['features']:
            lon, lat = response['features'][0]['geometry']['coordinates']
            return lat, lon
    except Exception as e:
        print(f"Erreur géocodage : {e}")
    return 46.5, 2.5  # Centre de la France par défaut si erreur

def generer_carte_un_bien(bien):
    lat, lon = obtenir_coordonnees(bien['adresse'], bien['ville'])
    m = folium.Map(location=[lat, lon], zoom_start=14, tiles="OpenStreetMap")
    popup_content = f"<b>{bien['type_bien']}</b><br>{bien['adresse']}<br>{bien['ville']}<br>{bien['prix']} €"
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_content, max_width=300),
        icon=folium.Icon(color="red", icon="home")
    ).add_to(m)
    return m._repr_html_()