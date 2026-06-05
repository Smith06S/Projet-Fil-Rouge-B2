import folium
import requests
from flask import url_for

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
    return 46.5, 2.5

def generer_carte_un_bien(bien_principal, db_connection):
    lat_principal, lon_principal = obtenir_coordonnees(bien_principal['adresse'], bien_principal['ville'])    
    m = folium.Map(location=[lat_principal, lon_principal], zoom_start=13, tiles="OpenStreetMap")

    with db_connection.cursor() as cur:
        cur.execute("SELECT * FROM bien WHERE id_agence = %s AND statut = 'Disponible'", (bien_principal['id_agence'],))
        tous_les_biens = cur.fetchall()
        
    for b in tous_les_biens:
        est_le_bien_principal = (b['id_bien'] == bien_principal['id_bien'])        
        lat, lon = obtenir_coordonnees(b['adresse'], b['ville'])
        
        if est_le_bien_principal:
            couleur_pin = "red"
            icone_style = "star"
        else:
            couleur_pin = "blue"
            icone_style = "home"
            
        lien_detail = url_for('bien.detail_bien', id_bien=b['id_bien'])
        popup_content = f"""
        <div style="font-family: sans-serif; min-width: 160px; text-align: center;">
            <h4 style="margin: 0 0 5px 0; color: #2c3e50;">{b['type_bien']}</h4>
            <p style="margin: 0 0 10px 0; font-weight: bold; color: green;">{b['prix']} €</p>
            <p style="margin: 0 0 10px 0; font-size: 0.85em; color: #7f8c8d;">{b['adresse']}, {b['ville']}</p>
            <a href="{lien_detail}" target="_top" style="display: block; background: #007BFF; color: white; padding: 6px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 0.9em;">
                👁️ Voir ce bien
            </a>
        </div>
        """
        
        # Ajouter le marqueur sur la carte
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=couleur_pin, icon=icone_style, prefix="fa")
        ).add_to(m)
        
    return m._repr_html_()