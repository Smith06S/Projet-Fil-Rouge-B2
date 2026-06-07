import bcrypt

class Utilisateur:
    def __init__(self, id_utilisateur, nom, prenom, email, mdp, telephone, role):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.telephone = telephone
        self.role = role

class Client(Utilisateur):
    def __init__(self, id_utilisateur, nom, prenom, email, mdp, telephone, role, id_client, type_client, budget_max):
        super().__init__(id_utilisateur, nom, prenom, email, mdp, telephone, role)
        self.id_client = id_client
        self.type_client = type_client
        self.budget_max = budget_max

class Commercial(Utilisateur):
    def __init__(self, id_utilisateur, nom, prenom, email, mdp, telephone, role, id_commercial, date_embauche, matricule, id_agence):
        super().__init__(id_utilisateur, nom, prenom, email, mdp, telephone, role)
        self.id_commercial = id_commercial
        self.date_embauche = date_embauche
        self.matricule = matricule
        self.id_agence = id_agence

class UtilisateurRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verifier_password(self, password_propose, password_hache):
        return bcrypt.checkpw(password_propose.encode('utf-8'), password_hache.encode('utf-8'))

    def get_by_email(self, email):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
            row = cur.fetchone()
            return Utilisateur(**row) if row else None
    
    def get_by_id(self, id_utilisateur):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM utilisateur WHERE id_utilisateur = %s", (id_utilisateur,))
            row = cur.fetchone()
            return Utilisateur(**row) if row else None

    def create_client(self, nom, prenom, email, mdp_clair, telephone, budget_max):
        mdp_hache = self.hash_password(mdp_clair)
        with self.db.cursor() as cur:
            cur.execute("""INSERT INTO utilisateur (nom, prenom, email, mdp, telephone, role) VALUES (%s, %s, %s, %s, %s, 'client') RETURNING id_utilisateur""", (nom, prenom, email, mdp_hache, telephone))
            id_user = cur.fetchone()['id_utilisateur']
            cur.execute("""INSERT INTO client (type_client, budget_max, id_utilisateur) VALUES ('Particulier', %s, %s)""", (budget_max, id_user))
        self.db.commit()

    def create_commercial(self, nom, prenom, email, mdp_clair, telephone, id_agence, matricule):
        mdp_hache = self.hash_password(mdp_clair)
        with self.db.cursor() as cur:
            cur.execute("""INSERT INTO utilisateur (nom, prenom, email, mdp, telephone, role) VALUES (%s, %s, %s, %s, %s, 'commercial') RETURNING id_utilisateur""", (nom, prenom, email, mdp_hache, telephone))
            id_user = cur.fetchone()['id_utilisateur']   
            cur.execute("""INSERT INTO commercial (matricule, id_agence, id_utilisateur) VALUES (%s, %s, %s)""", (matricule, id_agence, id_user))
        self.db.commit()

    def get_client_id(self, id_utilisateur):
        with self.db.cursor() as cur:
            cur.execute("SELECT id_client FROM client WHERE id_utilisateur = %s", (id_utilisateur,))
            row = cur.fetchone()
            return row['id_client'] if row else None

    def get_commercial_details(self, id_utilisateur):
        with self.db.cursor() as cur:
            cur.execute("SELECT id_commercial, id_agence FROM commercial WHERE id_utilisateur = %s", (id_utilisateur,))
            return cur.fetchone()
        
    def update_profil(self, id_utilisateur, nom, prenom, email, telephone):
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE utilisateur 
                SET nom = %s, prenom = %s, email = %s, telephone = %s
                WHERE id_utilisateur = %s
            """, (nom, prenom, email, telephone, id_utilisateur))
        self.db.commit()
    def get_all_users(self):
        with self.connection.cursor() as cur:
            cur.execute("SELECT id_utilisateur, nom, prenom, email, telephone, role FROM utilisateur")
            return cur.fetchall()