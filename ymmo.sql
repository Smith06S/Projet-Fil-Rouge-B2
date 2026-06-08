--
-- PostgreSQL database dump
--

\restrict LYo5pX6H0OGfTd2wgq5HMYIzRPuqkMWSXEgtLeE4sgWAp3JAW5I3HKLt0b47aFN

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agence; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agence (
    id_agence integer NOT NULL,
    nom character varying(100) NOT NULL,
    ville character varying(100) NOT NULL,
    adresse character varying(255) NOT NULL,
    image_url character varying(255) DEFAULT 'static/images/default_agence.jpg'::character varying
);


ALTER TABLE public.agence OWNER TO postgres;

--
-- Name: agence_id_agence_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agence_id_agence_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.agence_id_agence_seq OWNER TO postgres;

--
-- Name: agence_id_agence_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agence_id_agence_seq OWNED BY public.agence.id_agence;


--
-- Name: bien; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bien (
    id_bien integer NOT NULL,
    ville character varying(100) NOT NULL,
    adresse character varying(255) NOT NULL,
    description text,
    nbr_pieces integer NOT NULL,
    surface numeric(6,2) NOT NULL,
    type_bien character varying(50) NOT NULL,
    prix numeric(12,2) NOT NULL,
    statut character varying(20) DEFAULT 'Disponible'::character varying,
    id_commercial integer NOT NULL,
    id_agence integer NOT NULL,
    nbr_chambres integer DEFAULT 0,
    a_balcon boolean DEFAULT false,
    a_parking boolean DEFAULT false,
    type_chauffage character varying(50) DEFAULT 'Non renseigné'::character varying,
    etage character varying(50) DEFAULT 'Rez-de-chaussée'::character varying,
    a_ascenseur boolean DEFAULT false,
    etat_logement character varying(50) DEFAULT 'Bon état'::character varying,
    annee_construction integer,
    CONSTRAINT bien_statut_check CHECK (((statut)::text = ANY ((ARRAY['Disponible'::character varying, 'Vendu'::character varying, 'Retiré'::character varying])::text[])))
);


ALTER TABLE public.bien OWNER TO postgres;

--
-- Name: bien_id_bien_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bien_id_bien_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bien_id_bien_seq OWNER TO postgres;

--
-- Name: bien_id_bien_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bien_id_bien_seq OWNED BY public.bien.id_bien;


--
-- Name: client; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client (
    id_client integer NOT NULL,
    type_client character varying(50) DEFAULT 'Particulier'::character varying,
    budget_max numeric(12,2) DEFAULT 0.00,
    id_utilisateur integer NOT NULL
);


ALTER TABLE public.client OWNER TO postgres;

--
-- Name: client_id_client_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_id_client_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_id_client_seq OWNER TO postgres;

--
-- Name: client_id_client_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_id_client_seq OWNED BY public.client.id_client;


--
-- Name: commercial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.commercial (
    id_commercial integer NOT NULL,
    date_embauche date DEFAULT CURRENT_DATE,
    matricule character varying(50) NOT NULL,
    id_agence integer NOT NULL,
    id_utilisateur integer NOT NULL
);


ALTER TABLE public.commercial OWNER TO postgres;

--
-- Name: commercial_id_commercial_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.commercial_id_commercial_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.commercial_id_commercial_seq OWNER TO postgres;

--
-- Name: commercial_id_commercial_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.commercial_id_commercial_seq OWNED BY public.commercial.id_commercial;


--
-- Name: discussion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discussion (
    id_discussion integer NOT NULL,
    titre character varying(150) NOT NULL,
    date_creation timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_bien integer NOT NULL,
    id_client integer NOT NULL,
    id_commercial integer NOT NULL
);


ALTER TABLE public.discussion OWNER TO postgres;

--
-- Name: discussion_id_discussion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discussion_id_discussion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.discussion_id_discussion_seq OWNER TO postgres;

--
-- Name: discussion_id_discussion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discussion_id_discussion_seq OWNED BY public.discussion.id_discussion;


--
-- Name: favoris; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favoris (
    id_favoris integer NOT NULL,
    id_client integer NOT NULL,
    id_bien integer NOT NULL,
    date_ajout timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.favoris OWNER TO postgres;

--
-- Name: favoris_id_favoris_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.favoris_id_favoris_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favoris_id_favoris_seq OWNER TO postgres;

--
-- Name: favoris_id_favoris_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.favoris_id_favoris_seq OWNED BY public.favoris.id_favoris;


--
-- Name: message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message (
    id_message integer NOT NULL,
    message text NOT NULL,
    date_heure timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_discussion integer NOT NULL,
    id_expediteur integer NOT NULL
);


ALTER TABLE public.message OWNER TO postgres;

--
-- Name: message_id_message_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_message_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.message_id_message_seq OWNER TO postgres;

--
-- Name: message_id_message_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_message_seq OWNED BY public.message.id_message;


--
-- Name: photo_bien; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.photo_bien (
    id_photo integer NOT NULL,
    image_url character varying(255) NOT NULL,
    id_bien integer NOT NULL
);


ALTER TABLE public.photo_bien OWNER TO postgres;

--
-- Name: photo_bien_id_photo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.photo_bien_id_photo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.photo_bien_id_photo_seq OWNER TO postgres;

--
-- Name: photo_bien_id_photo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.photo_bien_id_photo_seq OWNED BY public.photo_bien.id_photo;


--
-- Name: utilisateur; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.utilisateur (
    id_utilisateur integer NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    mdp character varying(255) NOT NULL,
    telephone character varying(20),
    role character varying(20) NOT NULL,
    CONSTRAINT utilisateur_role_check CHECK (((role)::text = ANY ((ARRAY['admin'::character varying, 'commercial'::character varying, 'client'::character varying])::text[])))
);


ALTER TABLE public.utilisateur OWNER TO postgres;

--
-- Name: utilisateur_id_utilisateur_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.utilisateur_id_utilisateur_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.utilisateur_id_utilisateur_seq OWNER TO postgres;

--
-- Name: utilisateur_id_utilisateur_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.utilisateur_id_utilisateur_seq OWNED BY public.utilisateur.id_utilisateur;


--
-- Name: agence id_agence; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agence ALTER COLUMN id_agence SET DEFAULT nextval('public.agence_id_agence_seq'::regclass);


--
-- Name: bien id_bien; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bien ALTER COLUMN id_bien SET DEFAULT nextval('public.bien_id_bien_seq'::regclass);


--
-- Name: client id_client; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client ALTER COLUMN id_client SET DEFAULT nextval('public.client_id_client_seq'::regclass);


--
-- Name: commercial id_commercial; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commercial ALTER COLUMN id_commercial SET DEFAULT nextval('public.commercial_id_commercial_seq'::regclass);


--
-- Name: discussion id_discussion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion ALTER COLUMN id_discussion SET DEFAULT nextval('public.discussion_id_discussion_seq'::regclass);


--
-- Name: favoris id_favoris; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris ALTER COLUMN id_favoris SET DEFAULT nextval('public.favoris_id_favoris_seq'::regclass);


--
-- Name: message id_message; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message ALTER COLUMN id_message SET DEFAULT nextval('public.message_id_message_seq'::regclass);


--
-- Name: photo_bien id_photo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photo_bien ALTER COLUMN id_photo SET DEFAULT nextval('public.photo_bien_id_photo_seq'::regclass);


--
-- Name: utilisateur id_utilisateur; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur ALTER COLUMN id_utilisateur SET DEFAULT nextval('public.utilisateur_id_utilisateur_seq'::regclass);


--
-- Data for Name: agence; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agence (id_agence, nom, ville, adresse, image_url) FROM stdin;
1	Agence d'Aix-en-Provence	Aix-en-Provence	2 Place de l'Hôtel de Ville	static/images/AgenceAix.webp
2	Agence de Bordeaux	Bordeaux	10 Place de la Bourse	static/images/AgenceBordeaux.webp
3	Agence de Lille	Lille	25 Place du Général de Gaulle	static/images/AgenceLille.webp
4	Agence de Lyon	Lyon	1 Place Bellecour	static/images/AgenceLyon.webp
5	Agence de Marseille	Marseille	1 Quai du Port	static/images/AgenceMarseille.webp
6	Agence de Nantes	Nantes	2 Place du Commerce	static/images/AgenceNantes.webp
7	Agence de Nice	Nice	1 Place Masséna	static/images/AgenceNice.webp
8	Agence de Paris	Paris	2 Place de l'Hôtel de Ville	static/images/AgenceParis.webp
9	Agence de Rennes	Rennes	1 Place de la Mairie	static/images/AgenceRennes.webp
10	Agence de Strasbourg	Strasbourg	1 Place de la Cathédrale	static/images/AgenceStrasbourg.webp
11	Agence de Toulon	Toulon	1 Avenue de la République	static/images/AgenceToulon.webp
12	Agence de Toulouse	Toulouse	1 Place du Capitole	static/images/AgenceToulouse.webp
\.


--
-- Data for Name: bien; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bien (id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_commercial, id_agence, nbr_chambres, a_balcon, a_parking, type_chauffage, etage, a_ascenseur, etat_logement, annee_construction) FROM stdin;
21	La Trinité	54 Boulevard du Mont-Boron, 06300 Nice	 Située dans un environnement calme et recherché du secteur de La Trinité, cette charmante maison individuelle saura vous séduire par son cadre paisible et ses prestations fonctionnelles.\r\nÉdifiée sur un terrain agréable, elle bénéficie de plusieurs stationnements, d'un jardin et d'une belle terrasse pour profiter des beaux jours en toute tranquillité.\r\nAu rez-de-chaussée, vous découvrirez un espace de vie convivial composé d'un séjour lumineux avec cuisine ouverte, ainsi qu'un WC indépendant.	4	80.00	Appartement	500000.00	Disponible	7	7	3	f	f	Individuel Électrique	Rez-de-chaussée	t	Neuf	\N
3	Cannes	42 Boulevard de la Source, 06400 Cannes	Appartement avec vue sur la mer	3	75.00	Appartement	2000000.00	Disponible	1	1	2	t	t	Individuel Électrique	3ème	t	Bon état	1960
4	Aix-en-Provence	1850 Rte de Berre, 13090 Aix-en-Provence	Maison avec une superbe vue sur son immense terrain. Piscine, nombreuses chambres, ...	16	500.00	Maison	8900000.00	Disponible	1	1	7	t	t	Individuel Électrique		f	Bon état	1980
5	Nice	118 Bd Carnot, 06300 Nice	Appartement duplex de luxe avec vue sur la mer.	4	161.00	Maison	8900000.00	Disponible	1	1	2	t	t	Individuel Électrique	Rez-de-chaussée	t	Bon état	1980
6	Bordeau	17 Place de la Bourse, 33000 Bordeaux	L'agence Ymmo-Bordeau vous propose à la vente cette superbe échoppe en pierre de plain pied et non mitoyenne sur une parcelle de plus de 400 m², idéalement située dans une rue calme au centre de Caudéran.\r\nEn retrait de rue avec jardin d'accueil, l'entrée centrale avec carreaux de ciment distribue 3 belles chambres avec de beaux parquets, 2 salles d'eau et une pièce de vie de 40m² baignée de lumière, climatisée, donnant de plain-pied sur un grand jardin bien exposé, sans vis à vis. La cuisine séparée par une vitre d'atelier ouvre également sur le jardin. Arrière cuisine / buanderie .\r\nPossibilité de stationner 3 véhicules sur la parcelle.\r\nMaison lumineuse en excellent état située dans une rue calme, à proximité immédiate des commodités du centre de Caudéran, des établissements scolaires, et des transports lignes 2-33-73.\r\nPrix : 787.000 € (4.93 % d'honoraires TTC à la charge de l'acquéreur.)	4	113.00	Maison	787000.00	Disponible	2	2	3	t	f	Individuel Électrique	Rez-de-chaussée	f	Neuf	\N
7	La Bastide, Bordeaux	112 Rue Jules Ferry, 33200 Bordeaux	Ymmo-Bordeau vous propose cette maison individuelle d'environ 120 m² habitables située Rue de Saint-Émilion à Bordeaux, sur une parcelle de 270 m². Ce bien se distingue par son agréable jardin végétalisé, son exposition Sud-Ouest offrant une belle luminosité naturelle, ainsi que son extension bois réalisée en 2018. Cette propriété sera un vrai havre de paix pour vous et votre famille.	5	120.00	Maison	569000.00	Disponible	2	2	3	t	t	Pompe à chaleur	Rez-de-chaussée	f	Neuf	2018
8	Villa dans le quartier La Bastide	8 Rue de la Renaissance, 33200 Bordeaux	Située à la Bastide, cette maison loft à l'architecture unique et aux volumes spectaculaires a été récemment réhabilitée par un architecte en loft de 270 m², avec un jardin/terrasse privatif de 90 m².\r\n\r\nDès l'entrée dans les lieux, on accède, par un escalier, à un studio indépendant avec salle d'eau et rangements, idéal pour recevoir ou développer une activité indépendante.\r\nUne vaste cour couverte privative, offrant un stationnement sécurisé pouvant accueillir jusqu'à trois véhicules, nous mène à l'habitation principale.\r\n\r\nAu rez-de-chaussée, le séjour cathédrale d'environ 70 m² impressionne par ses près de 7 mètres de hauteur sous plafond et sa spectaculaire façade vitrée, largement ouverte sur le jardin exposé Est. La cuisine ouverte, prolongée par une arrière-cuisine et une buanderie attenante, s'intègre harmonieusement à cet espace de vie aux volumes remarquables. Une vaste suite parentale avec dressing, salle d'eau et WC complète ce niveau avec confort et intimité.	8	271.00	Maison	1150000.00	Disponible	2	2	4	t	t	Collectif Gaz	Rez-de-chaussée	f	Neuf	2020
9	Les Pierres Blanches, Sète	42 Rue de la Bassée, 59000 Lille	Découvrez cette villa d'architecte dont l'emplacement est un privilège absolu.\r\n\r\nElle conjugue une vue mer imprenable et une accessibilité immédiate : les plages et les commerces animés sont à quelques pas seulement.\r\n\r\nPensée pour un mode de vie moderne, cette propriété d'exception a été conçue pour l'autonomie et dans un esprit éco-responsable.\r\n\r\nSon agencement est l'un de ses atouts majeurs : deux habitations distinctes, séparées par un garage, offrent une flexibilité d'habitation maximale, idéale pour l'accueil, un projet locatif, ou une vie familiale préservant l'intimité de chacun.\r\n\r\nLa Résidence Principale (130 m² env.), véritable cocon de raffinement, cet espace séduit par ses prestations haut de gamme. Il s'ouvre sur une superbe cuisine moderne, véritable pièce maîtresse, et un salon-séjour baigné de lumière, réchauffé par une belle cheminée.	9	210.00	Maison	1199000.00	Disponible	3	3	6	t	t	Individuel Électrique	Rez-de-chaussée	f	Neuf	2013
10	Villa • Pignan	115 Rue de Toul, 59000 Lille	Située aux portes de Montpellier, cette propriété de 4ha 79a 79ca offre un cadre paisible avec vue panoramique allant jusqu'à la mer.\r\n\r\nEntièrement de plain-pied, la villa de 287 m² comprend deux grands salons, une cuisine équipée, six chambres, et plusieurs salles de bain.\r\n\r\nCette magnifique demeure de prestige, parfaitement exposée et de plain-pied, offre un agencement élégant et des volumes généreux.\r\n\r\nElle convient aussi bien à une résidence principale qu'à une résidence secondaire.\r\n\r\nGrandes dépendances attenantes.	9	287.00	Maison	2490000.00	Disponible	3	3	6	f	t	Individuel Électrique	Rez-de-chaussée	f	Neuf	\N
11	Centre, Lille	89 Rue de la République, 59800 Lille	Située en hyper-centre de Lille, à deux pas de la place de la République Beaux-Arts, des commerces et des écoles, cette élégante maison bourgeoise baignée de lumière de 231,34m² séduit par son cachet préservé, ses volumes généreux et son parfait état technique.\r\nDès l’entrée, la double distribution dessert un magnifique double séjour de 43m², sublimé par un parquet ancien, une cheminée, de délicates moulures et une belle hauteur sous plafond, offrant un cadre de réception raffiné.\r\nLe rez-de-chaussée propose également un bureau, une cuisine avec espace salle à manger, une buanderie ainsi que des toilettes séparées.\r\nDesservis par un superbe escalier en ormes, les étages accueillent quatre chambres spacieuses, deux salles de bains, ainsi qu’un vaste espace de 43 m² à imaginer selon vos envies : suite supplémentaire, salle de cinéma, atelier d’artiste ou bureau.\r\nÀ l’extérieur, un superbe jardin arboré, exposé sud-est, au calme et parfaitement préservé des regards, vous offre un cadre paisible et intimiste.\r\nCe bien rare est complété par quatre caves. Possibilité d’acquérir un stationnement en sus.\r\nUne adresse prisée, une maison en excellent état, un charme authentique et un potentiel remarquable pour cette élégante demeure familiale au cœur de Lille.	7	232.00	Maison	1190000.00	Disponible	3	3	5	f	f	Collectif Gaz	Rez-de-chaussée	f	Bon état	1900
12	Saint Rambert, Lyon 9ème	45 Rue Henri Gorjus, 69003 Lyon	Idéalement située dans une rue paisible, cette maison individuelle sur deux niveaux représente une opportunité rare de conjuguer vie citadine et tranquillité. Bénéficiant d'un emplacement de choix à proximité des commerces, des écoles et des activités du quartier, elle s'inscrit dans un environnement résidentiel recherché pour sa qualité de vie.\r\n\r\nLa maison s'ouvre sur une belle pièce de vie baignée de lumière, où la cuisine indépendante et le salon avec cheminée forment un ensemble convivial et chaleureux. Cet espace de réception, communique directement avec l'extérieur par de larges baies vitrées.\r\nOn découvre alors un jardin particulièrement cosy, à la fois fleuri et arboré, dont l'agencement intimiste invite à la détente. Un bel olivier apporte une touche végétale apaisante à ce jardin clos, qui profite d'un calme absolu et d'une absence totale de vis-à-vis. Un bureau et un cellier viennent compléter ce niveau.	6	194.00	Maison	895000.00	Disponible	4	4	9	t	t	Individuel Électrique	Rez-de-chaussée	f	Neuf	\N
13	Monplaisir-Le Bachut, Lyon 8ème	112 Rue Ferdinand Buisson, 69003 Lyon	Nouvelle exclusivité victoire Immobilier, Au cœur du très recherché quartier de Monplaisir, dans une rue pavillonnaire calme et prisée du 8 € arrondissement de Lyon, à proximité immédiate des commerces, écoles et transports (tram T2, T6, bus et métro D Monplaisir-Lumière à 6 min à pied). Venez découvrir cette magnifique maison d'architecte en ossature bois de 200 m².\r\n\r\nÉdifiée sur 3 niveaux, cette maison familiale séduit immédiatement par ses volumes, sa luminosité omniprésente et la qualité remarquable de ses prestations.\r\n\r\nDès l'entrée, vous serez charmés par une superbe pièce de vie de près de 70 m² bénéficiant d'une hauteur sous plafond de 2,75 m s'ouvrant harmonieusement sur le jardin, l'impression d'étre en dehors de la ville tout en étant à quelques pas du métro et des commerces. Un cellier, un vestiaire ainsi qu'un WC complètent ce niveau pensé pour un confort de vie optimal.\r\n	6	200.00	Maison	1450000.00	Disponible	4	4	5	t	t	Individuel Électrique	Rez-de-chaussée	f	Bon état	2000
14	Bompard, Marseille 7ème	45 Chemin du Roucas-Blanc, 13007 Marseille	Une remarquable villa d'architecte idéalement située au cœur du très prisé quartier de Bompard. Nichée dans un environnement résidentiel recherché, cette propriété bénéficie d'un calme absolu tout en étant à proximité immédiate du centre-ville et du littoral, offrant ainsi un cadre de vie rare où se conjuguent sérénité, élégance et art de vivre méditerranéen.\r\n\r\nBaignée de lumière tout au long de la journée grâce à son exposition idéale et à ses larges ouvertures, cette propriété se distingue par sa configuration unique. Elle est aujourd'hui divisée en deux habitations indépendantes, pouvant être réunies très facilement afin de créer une seule et même demeure familiale de standing, selon les besoins et les projets de ses futurs acquéreurs.	6	276.00	Maison	2680000.00	Disponible	5	5	5	t	f	Individuel Électrique	Rez-de-chaussée	f	Neuf	2015
15	La Calade, Marseille 15ème	54 Rue d'Endoume, 13007 Marseille	Ymmo vous présente à la vente dans le secteur de la CALADE\r\nUne maison T5 de 152m2 avec piscine et dépendances face à la mer, dans le 15e arrondissement de Marseille, découvrez cette charmante maison en excellent état, offrant un cadre de vie privilégié entre confort et modernité.	3	70.00	Bureau	70000.00	Disponible	5	5	2	f	t	Pompe à chaleur		t	Neuf	2023
16	Laparade	34 Avenue de Saint-Barnabé, 13012 Marseille	A Laparade - Lot-et-Garonne. À Laparade - découvrez cet ancien moulin en pierre du XVIIIe siècle - entièrement rénové et implanté sur une parcelle de plus de 11 000 m² avec ruisseau - prairies et arbres. La maison - d'une surface habitable confortable répartie sur 2 niveaux - se compose aujourd'hui de 2 chambres et offre la possibilité d'en créer une troisième. La pièce de vie est lumineuse - avec de beaux volumes et l'alliance de l'ancien avec le contemporain. Les prestations comprennent : le chauffage électrique - une microstation neuve conforme - des menuiseries bois double vitrage sur une grande partie du bien	4	95.00	Maison	198000.00	Disponible	5	5	2	t	f	Individuel Électrique	Rez-de-chaussée	f	Neuf	\N
17	Rond-Point de Rennes, Nantes	45 Rue de la Bastille, 44000 Nantes	PETIT BIJOU\r\nSituée entre le quartier SAINT PASQUIER et le Boulevard LELASSEUR, proche ROND POINT DE RENNES, nichée au fond d'une impasse avec entrée privée Maison moderne de plain-pied. Elle offre une surface de 80 m², édifiée sur une parcelle de 436 m²\r\nL' univers de vie se compose d'un joli salon, un espace repas avec cuisine aménagée et équipée, ouvrant sur la terrasse de 43 m² exposée SUD\r\nUn couloir dessert trois chambres dont une aménagée en dressing, une salle d'eau, toilettes\r\nToutes les pièces ont accès à l' extérieur. Un garage complète le bien. Vous profiterez d'un ravissant jardin, avec terrasse, dépendances. Le tout sur parcelle boisée\r\nIntimité assurée, tous les commerces et transports en quelques minutes à pieds. Idéal pour aller au marché de Talensac en vélo. Aucun travaux à prévoir.	5	80.00	Maison	497000.00	Disponible	6	6	3	f	t	Pompe à chaleur	Rez-de-chaussée	f	À rafraîchir	2012
18	Centre Ville, Nantes	63 Rue de la Brasserie, 44000 Nantes	Cette maison de caractère de 120 m² habitables et plus de 150 m2 au sol située en plein cœur de Nantes, entre le quartier Bastille et la place Aristide Briand, à proximité immédiate des écoles, des commerces et des transports.\r\n\r\nDès l'entrée la maison séduit par son authenticité. Le rez-de-chaussée offre un espace de vie comprenant un salon, un séjour et une cuisine indépendante pouvant être repensé selon vos besoins du quotidien.\r\n\r\nLes deux étages distribuent l'espace nuit avec 3 à 4 chambres possibles ainsi qu'une salle de bains. La quatrième chambre peut évoluer au gré de vos envies en bureau, salle de jeux..	5	150.00	Maison	499500.00	Disponible	6	6	4	f	f	Individuel Électrique	Rez-de-chaussée	f	Bon état	2020
19	Saint-Fiacre-sur-Maine	78 Boulevard de Longchamp, 44000 Nantes	Maison familiale de caractère avec logement indépendant – 207,84 m² – 6 pièces – 4 chambres – Terrain de 2 360 m²\r\n\r\nConstruite en 1978, cette maison familiale est idéalement située au cœur du quartier prisé de la Ramée à Saint-Fiacre-sur-Maine, un village recherché offrant un cadre de vie idyllique aux portes de Vertou. L’environnement séduit par sa tranquillité, son esprit nature et son accès privilégié à de superbes balades en pleine campagne ainsi qu’aux bords de la Sèvre Nantaise.\r\n	7	208.00	Maison	499200.00	Disponible	6	6	4	f	f	Pompe à chaleur	Rez-de-chaussée	f	Neuf	2000
20	Le Port, Villefranche-sur-Mer	45 Avenue de Flirey, 06000 Nice	Maison individuelle de caractère, rare et confidentielle, située au cœur de la vieille ville de Villefranche-sur-Mer, offrant un aperçu mer raffiné ainsi qu’une vue remarquable sur l’église historique et les toits du village.\r\n\r\nEntièrement repensée avec soin, la maison propose des volumes optimisés, une cuisine contemporaine équipée ouverte sur l’espace de vie, ainsi que de nombreux rangements intégrés parfaitement dissimulés. Un balcon complète cet ensemble, invitant à profiter de l’atmosphère unique du quartier.	2	47.72	Maison	490000.00	Disponible	7	7	1	f	t	Collectif Gaz	Rez-de-chaussée	f	Bon état	\N
22	Èze	63 Avenue de Fabron, 06200 Nice	Surplombant la Mer, dans une réserve naturelle, en dessous du fameux restaurant la Chèvre d'or, à 15 mn à pied du village ,sans aucun autre accès qu' un chemin, venez découvrir cette exceptionnelle et rarissime Villa entièrement rénovée, unique par son emplacement, seul au monde, dans un écrin de verdure, avec vue mer et foret au soleil Levant.	3	68.00	Maison	495000.00	Disponible	7	7	2	f	f	Individuel Électrique	Rez-de-chaussée	f	Neuf	2010
23	Breuil-Magné	14 Villa de l'Adour, 75019 Paris	Belle propriété familiale de 178 m² habitables, idéalement située sur la commune de Breuil-Magné, dans un environnement calme et résidentiel, à l'abri des regards.\r\n\r\nImplantée sur une parcelle de 1 144 m² sans vis-à-vis, cette maison offre un cadre de vie privilégié, pensé pour accueillir une grande famille ou pour recevoir dans les meilleures conditions.	7	178.00	Maison	499000.00	Disponible	8	8	6	f	t	Collectif Gaz	Rez-de-chaussée	f	À rafraîchir	2001
24	Archives, Paris 3ème	25 Square de Montsouris, 75014 Paris	Coldwell Banker Paris propose à la vente un studio de caractère au dernier étage d'un immeuble classé du XVIIème siècle, dans le Marais. Poutres apparentes, cheminées, escalier d'époque .. Ce studio présente le charme unique du Vieux Paris dans l'un des quartiers les plus prestigieux et les plus attractifs de la Capitale, riche de ses monuments emblématiques et ses boutiques réputées. Une grande pièce de vie partiellement séparée en deux parties permet d'accueillir un coin chambre avec un grand lit double, ainsi qu'un canapé dans le coin salon. La salle d'eau tout confort et la cuisine équipée confèrent à ce bien le confort et le charme d'un pied-à-terre idéal pour des séjours enchanteurs !\r\n	1	29.00	Appartement	498750.00	Disponible	8	8	1	f	f	Pompe à chaleur	3ème	t	Bon état	2010
\.


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client (id_client, type_client, budget_max, id_utilisateur) FROM stdin;
1	Particulier	0.00	1
2	Particulier	0.00	2
3	Particulier	0.00	3
4	Particulier	0.00	4
5	Particulier	0.00	5
6	Particulier	0.00	6
7	Particulier	0.00	7
8	Particulier	0.00	8
9	Particulier	0.00	9
10	Particulier	0.00	10
11	Particulier	0.00	11
12	Particulier	0.00	12
13	Particulier	0.00	13
14	Particulier	0.00	14
15	Particulier	0.00	15
16	Particulier	0.00	16
17	Particulier	0.00	17
18	Particulier	0.00	18
19	Particulier	0.00	19
20	Particulier	0.00	20
21	Particulier	0.00	21
22	Particulier	0.00	22
23	Particulier	0.00	23
24	Particulier	0.00	24
25	Particulier	0.00	25
\.


--
-- Data for Name: commercial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.commercial (id_commercial, date_embauche, matricule, id_agence, id_utilisateur) FROM stdin;
1	2026-06-04	COMM_SARA_001	1	2
2	2026-06-07	COMM_15	2	15
3	2026-06-07	COMM_16	3	16
4	2026-06-07	COMM_17	4	17
5	2026-06-07	COMM_18	5	18
6	2026-06-07	COMM_19	6	19
7	2026-06-07	COMM_20	7	20
8	2026-06-07	COMM_21	8	21
9	2026-06-07	COMM_22	9	22
10	2026-06-07	COMM_23	10	23
11	2026-06-07	COMM_24	11	24
12	2026-06-07	COMM_25	12	25
13	2026-06-07	COMM_14	1	14
\.


--
-- Data for Name: discussion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discussion (id_discussion, titre, date_creation, id_bien, id_client, id_commercial) FROM stdin;
2	Discussion - Maison à Nice	2026-06-07 14:06:01.408477	5	5	1
3	Discussion - Appartement à Cannes	2026-06-07 14:41:55.956722	3	5	1
\.


--
-- Data for Name: favoris; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favoris (id_favoris, id_client, id_bien, date_ajout) FROM stdin;
3	5	5	2026-06-07 14:05:55.687098
7	5	4	2026-06-07 14:16:32.688844
18	5	3	2026-06-07 14:41:12.565339
\.


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.message (id_message, message, date_heure, id_discussion, id_expediteur) FROM stdin;
2	Bonjour	2026-06-07 18:21:41.353285	2	2
\.


--
-- Data for Name: photo_bien; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photo_bien (id_photo, image_url, id_bien) FROM stdin;
7	static/uploads/bien_3_Capture_decran_2026-06-05_145442.png	3
8	static/uploads/bien_3_Capture_decran_2026-06-05_145544.png	3
9	static/uploads/bien_4_Capture_decran_2026-06-06_181721.png	4
10	static/uploads/bien_4_Capture_decran_2026-06-06_181735.png	4
11	static/uploads/bien_4_Capture_decran_2026-06-06_181755.png	4
12	static/uploads/bien_4_Capture_decran_2026-06-06_181810.png	4
13	static/uploads/bien_4_Capture_decran_2026-06-06_181827.png	4
14	static/uploads/bien_4_Capture_decran_2026-06-06_181846.png	4
15	static/uploads/bien_4_Capture_decran_2026-06-06_181901.png	4
16	static/uploads/bien_4_Capture_decran_2026-06-06_181921.png	4
17	static/uploads/bien_4_Capture_decran_2026-06-06_181936.png	4
18	static/uploads/bien_5_Capture_decran_2026-06-06_183000.png	5
19	static/uploads/bien_5_Capture_decran_2026-06-06_183017.png	5
20	static/uploads/bien_5_Capture_decran_2026-06-06_183030.png	5
21	static/uploads/bien_5_Capture_decran_2026-06-06_183043.png	5
22	static/uploads/bien_5_Capture_decran_2026-06-06_183054.png	5
23	static/uploads/bien_5_Capture_decran_2026-06-06_183106.png	5
24	static/uploads/bien_5_Capture_decran_2026-06-06_183115.png	5
25	static/uploads/bien_5_Capture_decran_2026-06-06_183126.png	5
26	static/uploads/bien_5_Capture_decran_2026-06-06_183138.png	5
27	static/uploads/bien_5_Capture_decran_2026-06-06_183152.png	5
28	static/uploads/bien_6_bordeau1.1.webp	6
29	static/uploads/bien_6_bordeau1.2.webp	6
30	static/uploads/bien_6_bordeau1.webp	6
31	static/uploads/bien_7_bordeau2.1.webp	7
32	static/uploads/bien_7_bordeau2.2.webp	7
33	static/uploads/bien_7_bordeau2.3.webp	7
34	static/uploads/bien_7_bordeau2.webp	7
35	static/uploads/bien_8_Bordeau3.1.webp	8
36	static/uploads/bien_8_Bordeau3.2.webp	8
37	static/uploads/bien_8_Bordeau3.webp	8
38	static/uploads/bien_9_lille.webp	9
39	static/uploads/bien_9_lille1.2.webp	9
40	static/uploads/bien_9_lille1.3.webp	9
41	static/uploads/bien_9_lille1.4.webp	9
42	static/uploads/bien_9_lille1.5.webp	9
43	static/uploads/bien_10_lille2.1.webp	10
44	static/uploads/bien_10_lille2.3.webp	10
45	static/uploads/bien_10_lille2.4.webp	10
46	static/uploads/bien_10_lille2.webp	10
47	static/uploads/bien_11_lille3.1.webp	11
48	static/uploads/bien_11_lille3.3.webp	11
49	static/uploads/bien_11_lille3.webp	11
50	static/uploads/bien_12_lyon1.1.webp	12
51	static/uploads/bien_12_lyon1.2.webp	12
52	static/uploads/bien_12_lyon1.3.webp	12
53	static/uploads/bien_12_lyon1.4.webp	12
54	static/uploads/bien_12_lyon1.webp	12
55	static/uploads/bien_13_lyon2.1.webp	13
56	static/uploads/bien_13_lyon2.webp	13
57	static/uploads/bien_14_marseille1.1.webp	14
58	static/uploads/bien_14_marseille1.2.webp	14
59	static/uploads/bien_14_marseille1.webp	14
60	static/uploads/bien_15_marseille2.1.webp	15
61	static/uploads/bien_15_marseille2.webp	15
62	static/uploads/bien_16_marseille3.1.webp	16
63	static/uploads/bien_16_marseille3.2.webp	16
64	static/uploads/bien_16_marseille3.webp	16
65	static/uploads/bien_17_nantes1.1.webp	17
66	static/uploads/bien_17_nantes1.2.webp	17
67	static/uploads/bien_17_nantes1.webp	17
68	static/uploads/bien_18_nantes2.1.webp	18
69	static/uploads/bien_18_nantes2.2.webp	18
70	static/uploads/bien_18_nantes2.webp	18
71	static/uploads/bien_19_nantes3.1.webp	19
72	static/uploads/bien_19_nantes3.2.webp	19
73	static/uploads/bien_19_nantes3.webp	19
74	static/uploads/bien_20_nice1.1.webp	20
75	static/uploads/bien_20_nice1.2.webp	20
76	static/uploads/bien_20_nice1.webp	20
77	static/uploads/bien_21_nice2.1.webp	21
78	static/uploads/bien_21_nice2.webp	21
79	static/uploads/bien_22_nice3.1.webp	22
80	static/uploads/bien_22_nice3.2.webp	22
81	static/uploads/bien_22_nice3.webp	22
82	static/uploads/bien_23_paris1.webp	23
83	static/uploads/bien_23_paris1.1.webp	23
84	static/uploads/bien_24_paris2.1.webp	24
85	static/uploads/bien_24_paris2.webp	24
86	static/uploads/bien_24_paris2.2.webp	24
\.


--
-- Data for Name: utilisateur; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.utilisateur (id_utilisateur, nom, prenom, email, mdp, telephone, role) FROM stdin;
3	smith	lola	lola@gmail.com	$2b$12$k3s4KM7qfNNtKdZjegQzeu4eCeQypKC3hcOCYMCQ0wM9WZa2Xkdiy	0584938243	client
1	smith	admin	admin@gmail.com	$2b$12$lZHHLiVv3jLKW.bfCVIAaOJ5DkEgJ3aMEInm7OW1bDZFdIETBDheu	0584938243	admin
2	smith	sara1	sara@gmail.com	$2b$12$dwx9pR3FI7r2XryuQUmUP.yyZ4W7IBLs/TZdEG2D5WBs/WE6fZvyG	0584938243	commercial
4	ori	fabien	fabien@gmail.com	$2b$12$s.607WUyppj0rkO7RaKEceP73Bzc72Z5r86BLMlt66fFf08rQtvfW	0602504824	client
5	campello	juliette	juliette@gmail.com	$2b$12$gSIceyIff5jAtufCo7mTR.pnz4DOJSe5u0OBrd/DiMHndGg/7S3JK	0607244762	client
6	ferrusi	enzo	enzo@gmail.com	$2b$12$i2lfE1JNKMRSLNRJyAcNPeN5Hu1JQmUeDkgzS0r4SV71PzOTevxcy	0752489625	client
7	removille	ewan	ewan@gmail.com	$2b$12$OSCU78JPMydmR9P.gaeXn.PPA6Y7OfCK3LqQ6Hv6OanqohAlXsM5i	0709823495	client
8	Germain	Cyllia	cyllia@gmail.com	$2b$12$JF0f4kIZKQ5FZ69c9uyGVewf3lYDstfcmCVWcTQCSNDZYFEG5F7Bi	0584938243	client
9	Smith	Alessia	alessia@gmail.com	$2b$12$1IUZtS3dVhZm7Bhb8Immc.kYaTppQeH62iDJfuWVodJIvIH9K/0pO	0584938243	client
10	Smith	Matteo	matteo@gmail.com	$2b$12$wzJx1ynF4uu6s5YrnDBZ7OmuxxHkQ2a.rb/8P43HsH092KnQcov4S	0584938243	client
11	Smith	Melissa	meli@gmail.com	$2b$12$GAodwU1kE1QrD15nIqWN1e1VMVbXgPkXVgLXFMfoz0SPhn.U./Uzq	0584938243	client
12	Stoppani	Tiziana	tizi@gmail.com	$2b$12$cSaMj80LKgfe2U8WQFnxQ.txjuzPsmBK2hKOkCVX44E8azyssuoja	0584938243	client
13	Ori	Ange	ange@gmail.com	$2b$12$WKXAVRjaHnsOpWc7jG7wwe6LmzJxPmv45idM.RVdOOMqd5QfiCdmK	0584938243	client
15	Lucien	Baptiste	bordeaux@gmail.com	$2b$12$jSs2WrKuwqHW9oymzjmo1.qIcSpNYODBmuT/kdCcXDaVcHzhpnYs.	0584938243	commercial
16	Soli	Camille	lille@gmail.com	$2b$12$Ko.RlI0V4bTZ4lm4R2ivLuhQMykxN34NdYgh3E424HIzGdMllhxqe	0584938243	commercial
17	Huggins	Mika	lyon@gmail.com	$2b$12$Z3byqZ6Uu2Q84kLdomAuqeqEiJ1WMVweY07EFP/gcxoxtAPVBRl6y	0584938243	commercial
18	Tolner	Evan	marseille@gmail.com	$2b$12$uE2BnNDt30txNvJt7YtUY.bUZHTX6pnnuQbjYPIRoeFynxWjfAQ6K	0584938243	commercial
19	Pilan	Romeo	nantes@gmail.com	$2b$12$7/R0AnS3o2ADRhNQE5qWUea2Dm8PtG05NLFN0ejpeNvnEylftXaRe	0584938243	commercial
20	Welz	Nathan	nice@gmail.com	$2b$12$mOzRp4mR69.um5HIxB/p2.zIJZp6vxvjUfYjYo5YnAu3R7LyI8Wn2	0584938243	commercial
21	Manfredi	Tina	paris@gmail.com	$2b$12$Q8Ipv1qs9Xyx.li92lPR8.D1Lry1fKng0/5zmMS7M8nB0r.vEJAJu	0584938243	commercial
22	Blino	Mael	rennes@gmail.com	$2b$12$anV2bDk9b8kzAZvecs5Ig.p1C79yP0QoMirqT23hCaxORZxQH1y3q	0584938243	commercial
23	Sovant	Luca	strasbourg@gmail.com	$2b$12$iPYtL43DkxX450xdMtHC5eEe0WqYQOpGLk5DRSSWYVaNHM6r4oaFK	0584938243	commercial
24	Beufli	Benoit	toulon@gmail.com	$2b$12$QX9wriCLSbMGHDAKhhA0fubEeOMtDMs0JqFel6JZlMaXutiGmHkfS	0584938243	commercial
25	Riquier	Pierre	toulouse@gmail.com	$2b$12$9h9veDaA7dOHJTVnDUKr4O0ZfqpThiJ/MaKQseebPrTwMF7HN7Yt.	0584938243	commercial
14	Romain	Lucie	aix@gmail.com	$2b$12$gEDqve3uDjWm6MJJ2MFkde5LuzleuKm9tdXOvhKaa4abprnbnyxJq	0584938243	commercial
\.


--
-- Name: agence_id_agence_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agence_id_agence_seq', 12, true);


--
-- Name: bien_id_bien_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bien_id_bien_seq', 24, true);


--
-- Name: client_id_client_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_id_client_seq', 25, true);


--
-- Name: commercial_id_commercial_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.commercial_id_commercial_seq', 13, true);


--
-- Name: discussion_id_discussion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discussion_id_discussion_seq', 3, true);


--
-- Name: favoris_id_favoris_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favoris_id_favoris_seq', 18, true);


--
-- Name: message_id_message_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.message_id_message_seq', 2, true);


--
-- Name: photo_bien_id_photo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photo_bien_id_photo_seq', 86, true);


--
-- Name: utilisateur_id_utilisateur_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.utilisateur_id_utilisateur_seq', 25, true);


--
-- Name: agence agence_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agence
    ADD CONSTRAINT agence_pkey PRIMARY KEY (id_agence);


--
-- Name: bien bien_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bien
    ADD CONSTRAINT bien_pkey PRIMARY KEY (id_bien);


--
-- Name: client client_id_utilisateur_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_id_utilisateur_key UNIQUE (id_utilisateur);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id_client);


--
-- Name: commercial commercial_id_utilisateur_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commercial
    ADD CONSTRAINT commercial_id_utilisateur_key UNIQUE (id_utilisateur);


--
-- Name: commercial commercial_matricule_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commercial
    ADD CONSTRAINT commercial_matricule_key UNIQUE (matricule);


--
-- Name: commercial commercial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commercial
    ADD CONSTRAINT commercial_pkey PRIMARY KEY (id_commercial);


--
-- Name: discussion discussion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_pkey PRIMARY KEY (id_discussion);


--
-- Name: favoris favoris_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT favoris_pkey PRIMARY KEY (id_favoris);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id_message);


--
-- Name: photo_bien photo_bien_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photo_bien
    ADD CONSTRAINT photo_bien_pkey PRIMARY KEY (id_photo);


--
-- Name: discussion unique_discussion_tchat; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT unique_discussion_tchat UNIQUE (id_bien, id_client);


--
-- Name: favoris unique_favoris; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT unique_favoris UNIQUE (id_client, id_bien);


--
-- Name: utilisateur utilisateur_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_email_key UNIQUE (email);


--
-- Name: utilisateur utilisateur_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_pkey PRIMARY KEY (id_utilisateur);


--
-- Name: bien bien_id_agence_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bien
    ADD CONSTRAINT bien_id_agence_fkey FOREIGN KEY (id_agence) REFERENCES public.agence(id_agence) ON DELETE CASCADE;


--
-- Name: bien bien_id_commercial_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bien
    ADD CONSTRAINT bien_id_commercial_fkey FOREIGN KEY (id_commercial) REFERENCES public.commercial(id_commercial) ON DELETE CASCADE;


--
-- Name: client client_id_utilisateur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_id_utilisateur_fkey FOREIGN KEY (id_utilisateur) REFERENCES public.utilisateur(id_utilisateur) ON DELETE CASCADE;


--
-- Name: commercial commercial_id_agence_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commercial
    ADD CONSTRAINT commercial_id_agence_fkey FOREIGN KEY (id_agence) REFERENCES public.agence(id_agence) ON DELETE CASCADE;


--
-- Name: commercial commercial_id_utilisateur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commercial
    ADD CONSTRAINT commercial_id_utilisateur_fkey FOREIGN KEY (id_utilisateur) REFERENCES public.utilisateur(id_utilisateur) ON DELETE CASCADE;


--
-- Name: discussion discussion_id_bien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_id_bien_fkey FOREIGN KEY (id_bien) REFERENCES public.bien(id_bien) ON DELETE CASCADE;


--
-- Name: discussion discussion_id_client_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_id_client_fkey FOREIGN KEY (id_client) REFERENCES public.client(id_client) ON DELETE CASCADE;


--
-- Name: discussion discussion_id_commercial_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_id_commercial_fkey FOREIGN KEY (id_commercial) REFERENCES public.commercial(id_commercial) ON DELETE CASCADE;


--
-- Name: favoris favoris_id_bien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT favoris_id_bien_fkey FOREIGN KEY (id_bien) REFERENCES public.bien(id_bien) ON DELETE CASCADE;


--
-- Name: favoris favoris_id_client_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoris
    ADD CONSTRAINT favoris_id_client_fkey FOREIGN KEY (id_client) REFERENCES public.client(id_client) ON DELETE CASCADE;


--
-- Name: message message_id_discussion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_id_discussion_fkey FOREIGN KEY (id_discussion) REFERENCES public.discussion(id_discussion) ON DELETE CASCADE;


--
-- Name: message message_id_expediteur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_id_expediteur_fkey FOREIGN KEY (id_expediteur) REFERENCES public.utilisateur(id_utilisateur) ON DELETE CASCADE;


--
-- Name: photo_bien photo_bien_id_bien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photo_bien
    ADD CONSTRAINT photo_bien_id_bien_fkey FOREIGN KEY (id_bien) REFERENCES public.bien(id_bien) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict LYo5pX6H0OGfTd2wgq5HMYIzRPuqkMWSXEgtLeE4sgWAp3JAW5I3HKLt0b47aFN