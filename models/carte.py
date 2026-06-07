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
    m = folium.Map(location=[lat_principal, lon_principal], zoom_start=11, tiles="OpenStreetMap")

    with db_connection.cursor() as cur:
        cur.execute("SELECT * FROM bien WHERE id_agence = %s AND statut = 'Disponible'", (bien_principal['id_agence'],))
        tous_les_biens = cur.fetchall()
        
    for b in tous_les_biens:
        est_le_bien_principal = (b['id_bien'] == bien_principal['id_bien'])        
        lat, lon = obtenir_coordonnees(b['adresse'], b['ville'])
        
        if est_le_bien_principal:
            couleur_pin = "#534E47"
            icone_style = "fa-star"
        else:
            couleur_pin = "#918575"
            icone_style = "fa-home"
            
        lien_detail = url_for('bien.detail_bien', id_bien=b['id_bien'])
        popup_content = f"""
            <div style="font-family: 'Segoe UI', sans-serif; min-width: 160px; text-align: center; color: #21221F;">
                <h4 style="margin: 0 0 5px 0; color: #534E47;">{b['type_bien']}</h4>
                <p style="margin: 0 0 10px 0; font-weight: bold; color: #918575;">{b['prix']} €</p>
                <a href="{lien_detail}" target="_top" 
                style="display: block; background: #21221F; color: #DBD7D1; padding: 8px; 
                        text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 0.9em;">
                    Voir ce bien
                </a>
            </div>
            """
        html_icon = f"""
            <div style="color: {couleur_pin}; font-size: 24px; text-shadow: 0px 0px 3px white;">
                <i class="fa {icone_style}"></i>
            </div>"""
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(html=html_icon)
        ).add_to(m)
        
    return m._repr_html_()