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
