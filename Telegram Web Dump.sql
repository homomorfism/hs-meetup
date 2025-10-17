--
-- PostgreSQL database dump
--

\restrict bncuI0YIA3799bibAwCy1zAr9JQKUW4SkhXXh8FoKTyYMj6Dwjczy4UW11u1g1D

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.14

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL,
    icon character varying,
    color character varying,
    slug character varying NOT NULL
);


ALTER TABLE public.categories OWNER TO meetup_user;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO meetup_user;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: conversations; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.conversations (
    id integer NOT NULL,
    participant1_id integer NOT NULL,
    participant2_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.conversations OWNER TO meetup_user;

--
-- Name: conversations_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.conversations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conversations_id_seq OWNER TO meetup_user;

--
-- Name: conversations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.conversations_id_seq OWNED BY public.conversations.id;


--
-- Name: event_attendees; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.event_attendees (
    user_id integer NOT NULL,
    event_id integer NOT NULL
);


ALTER TABLE public.event_attendees OWNER TO meetup_user;

--
-- Name: events; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.events (
    id integer NOT NULL,
    title character varying NOT NULL,
    description character varying,
    date date NOT NULL,
    "time" character varying,
    duration character varying,
    group_id integer NOT NULL,
    organizer_id integer NOT NULL,
    location character varying,
    location_city character varying,
    latitude double precision,
    longitude double precision,
    max_attendees integer,
    external_attendees_count integer,
    price character varying,
    is_online boolean,
    category character varying NOT NULL,
    image character varying
);


ALTER TABLE public.events OWNER TO meetup_user;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO meetup_user;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: friendships; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.friendships (
    user_id integer NOT NULL,
    friend_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.friendships OWNER TO meetup_user;

--
-- Name: group_members; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.group_members (
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.group_members OWNER TO meetup_user;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    category character varying NOT NULL,
    location character varying,
    members_count integer,
    organizer_id integer NOT NULL,
    image character varying,
    founded timestamp with time zone DEFAULT now()
);


ALTER TABLE public.groups OWNER TO meetup_user;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO meetup_user;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    conversation_id integer NOT NULL,
    sender_id integer NOT NULL,
    content text NOT NULL,
    sent_at timestamp with time zone DEFAULT now(),
    is_read boolean
);


ALTER TABLE public.messages OWNER TO meetup_user;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_id_seq OWNER TO meetup_user;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: saved_searches; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.saved_searches (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying NOT NULL,
    keyword character varying,
    location character varying,
    category character varying,
    is_online boolean,
    price character varying,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.saved_searches OWNER TO meetup_user;

--
-- Name: saved_searches_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.saved_searches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.saved_searches_id_seq OWNER TO meetup_user;

--
-- Name: saved_searches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.saved_searches_id_seq OWNED BY public.saved_searches.id;


--
-- Name: search_history; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.search_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    keyword character varying,
    location character varying,
    category character varying,
    is_online boolean,
    price character varying,
    searched_at timestamp without time zone NOT NULL
);


ALTER TABLE public.search_history OWNER TO meetup_user;

--
-- Name: search_history_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.search_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.search_history_id_seq OWNER TO meetup_user;

--
-- Name: search_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.search_history_id_seq OWNED BY public.search_history.id;


--
-- Name: user_interests; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.user_interests (
    user_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.user_interests OWNER TO meetup_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: meetup_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    name character varying NOT NULL,
    bio character varying,
    location character varying,
    avatar character varying,
    member_since timestamp with time zone DEFAULT now(),
    is_active boolean
);


ALTER TABLE public.users OWNER TO meetup_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: meetup_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO meetup_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: meetup_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: conversations id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.conversations ALTER COLUMN id SET DEFAULT nextval('public.conversations_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: saved_searches id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.saved_searches ALTER COLUMN id SET DEFAULT nextval('public.saved_searches_id_seq'::regclass);


--
-- Name: search_history id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.search_history ALTER COLUMN id SET DEFAULT nextval('public.search_history_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.categories (id, name, icon, color, slug) FROM stdin;
1	Technology	💻	\N	technology
2	Arts & Culture	🎨	\N	arts-culture
3	Sports & Fitness	⚽	\N	sports-fitness
4	Food & Drink	🍕	\N	food-drink
5	Social Activities	🎉	\N	social-activities
6	Travel & Outdoor	🏔️	\N	travel-outdoor
7	Music	🎵	\N	music
8	Books & Writing	📚	\N	books-writing
9	Film & Photography	📷	\N	film-photography
10	Games	🎮	\N	games
11	Health & Wellness	🧘	\N	health-wellness
12	Business & Career	💼	\N	business-career
\.


--
-- Data for Name: conversations; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.conversations (id, participant1_id, participant2_id, created_at, updated_at) FROM stdin;
1	22	21	2025-10-16 14:10:22.510076+00	2025-10-16 16:40:00.649072+00
\.


--
-- Data for Name: event_attendees; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.event_attendees (user_id, event_id) FROM stdin;
22	418
22	399
22	359
21	418
22	414
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.events (id, title, description, date, "time", duration, group_id, organizer_id, location, location_city, latitude, longitude, max_attendees, external_attendees_count, price, is_online, category, image) FROM stdin;
418	🤩❤️🍹CONSTRUYENDO EL MAYOR CHAT SINGLE DE BCN. COLABORA Y HAZ NUEVAS AMISTADES.	🤩❤️🍹CONSTRUYENDO EL MAYOR CHAT SINGLE DE BCN. COLABORA Y HAZ NUEVAS AMISTADES.\n\nPARTICIPA EN LOS CHATS DE LAS ACTIVIDADES QUE MÁS TE INTERESAN Y TAMBIÉN PROPÓN NUEVAS IDEAS. GRACIAS POR CONSTRUIR ACTIVIDAD SOCIAL PARA HACER NUEVOS AMIGOS Y AMIGAS.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311348627/)\\nmeetup_id:311348627	2025-10-22	21:00	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/525434856/highres/
419	WeRoad Afterwork: Fiesta de Halloween y premios especiales	**🚨 Para participar en este evento y conocer la ubicación exacta, es obligatorio descargarse [aquí](https://onelink.to/5fkn72) la nueva app de WeRoad, WEMEET 🚨**\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/wemeet-20-30-40-anos-barcelona/events/311438478/)\\nmeetup_id:311438478	2025-10-29	20:30	\N	105	21	Location TBD		41.3851	2.1734	12	1	0.0	f	Dining Out	https://secure-content.meetupstatic.com/images/classic-events/530762518/highres/
420	Speaking Social BCN: Intercambio de idiomas // Language exchange 	(ES abajo // CAT a sota)\n\nJoin Speaking Social Barcelona for a lively evening of cultural and language exchange. Whether you’re a Barcelona local or you’re new to the city, this event is perfect for anyone looking to practise their English, Spanish, Catalan or absolutely any other language in a relaxed, sociable setting. Our language exchange nights will not only improve your language skills, they’re also a great excuse to meet people from diverse backgrounds and experience different cultures.\nW\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/speaking-social-barcelona/events/311544249/)\\nmeetup_id:311544249	2025-10-29	20:00	\N	106	21	Location TBD		41.3851	2.1734	100	6	0.0	f	Arts & Culture	https://secure-content.meetupstatic.com/images/classic-events/524774042/highres/
421	Dinner & New Friends: Sabores de India	**🚨 Para participar en este evento y conocer la ubicación exacta, es obligatorio descargarse [aquí](https://onelink.to/5fkn72) la nueva app de WeRoad, WEMEET 🚨**\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/wemeet-20-30-40-anos-barcelona/events/311203154/)\\nmeetup_id:311203154	2025-10-23	20:45	\N	105	21	Location TBD		41.3851	2.1734	12	2	0.0	f	Dining Out	https://secure-content.meetupstatic.com/images/classic-events/529368871/highres/
422	🤩❤️🍹LOS CHICOS INVITAMOS A PIZZA A LAS CHICAS. PIZZA GRATIS PARA LAS CHICAS.	🤩❤️🍹PIZZA PREVIA AL COPEO. NOS PONEMOS DE ACUERDO PARA IR A CENAR PIZZA SENCILLA LOCAL TIPO TELEPIZZA, DOMINO, ETC. QUE SALGA BARATO.\n\nNOS PONEMOS DE ACUERDO POR EL CHAT PRO COYOTE D7 PARA ENCONTRARNOS PARA CENAR PIZZA SENCILLA PREVIA AL COPEO EN COYOTE D7.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DEL CHAT PRO COYOTE D7 DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA.\n\nCOLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311380666/)\\nmeetup_id:311380666	2025-10-24	21:05	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/526168629/highres/
423	🤩❤️🍹COMPARTIMOS SELFIES EN EL GIMNASIO PARA TENER NUEVAS IDEAS DE OUTFITS Y ..	🤩❤️🍹COMPARTIMOS SELFIES EN EL GIMNASIO PARA TENER NUEVAS IDEAS DE OUTFITS Y HACER NUEVAS AMISTADES QUE COMPARTEN NUESTRAS MISMAS AFICIONES Y VALORES DE MENTE SANA Y CORPORE SANO.\n\nLAS PUBLICAMOS EN EL CHAT SELFIE HOY\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311441664/)\\nmeetup_id:311441664	2025-10-28	17:00	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/525463957/highres/
424	🤩❤️🍹NEW SUBGRUPO AMIGOS DEL FRANKFURT Y DISCO Q EN PEDRALBES. LET'S GO DANCE!!	🤩❤️🍹NEW SUBGRUPO AMIGOS DEL FRANKFURT Y DISCO Q EN PEDRALBES\n\nNOS PONEMOS DE ACUERDO POR EL CHAT GENERAL PARA ENCONTRARNOS.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311397085/)\\nmeetup_id:311397085	2025-10-25	23:59	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/525392818/highres/
425	Dinner & New Friends: Sabores de Brasil	**🚨 Para participar en este evento y conocer la ubicación exacta, es obligatorio descargarse [aquí](https://onelink.to/5fkn72) la nueva app de WeRoad, WEMEET 🚨**\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/wemeet-20-30-40-anos-barcelona/events/311403457/)\\nmeetup_id:311403457	2025-10-30	20:45	\N	105	21	Location TBD		41.3851	2.1734	12	1	0.0	f	Dining Out	https://secure-content.meetupstatic.com/images/classic-events/529368871/highres/
426	COMIDA para conocer gente nueva + sorteo + BAILE 	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/actividades-y-eventos-en-barcelona/events/311505446/)\\nmeetup_id:311505446	2025-10-19	14:00	\N	107	21	Location TBD		41.3851	2.1734	20	16	0.0	f	Coffee	\N
427	NEW SUBGRUPO PARA IR JUNTOS A LAS COMMON PEOPLE PARTY DE RAZZMATAZZ SOLO SINGLES	NEW SUBGRUPO PARA IR JUNTOS A LAS COMMON PEOPLE PARTY DE RAZZMATAZZ SOLO SINGLES\n\nVAMOS HACIENDO GRUPITO PARA IR A LAS PARTIES\n\nCOMENTA TU INTERÉS EN EL CHAT PRO BAILA ROCK DE NUESTRA NUEVA WEB:\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT PRO DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https:\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311288844/)\\nmeetup_id:311288844	2025-10-19	18:00	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530345682/highres/
428	🤩❤️🍹FRANKFURT CENA INFORMAL JÓVENES SINGLES PARA HACER NUEVAS AMISTADES ARIBAU	🤩❤️🍹CENA INFORMAL EN UN FRANKFURT JOVENES SINGLES EN LA ZONA ARIBAU CON CERVEZA FRESQUITA Y SALCHICHAS.\n\nNOS PONEMOS DE ACUERDO POR EL CHAT PRO QUEDADAS VARIAS PARA ENCONTRARNOS Y HACER NUEVAS AMISTADES EN EL EVENTO Y QUIÉN SABE SI CONOCER A ALGUIEN ESPECIAL.\n\nCON LA AYUDA DEL CHAT PRO QUEDADAS VARIAS NOS COORDINAMOS PARA ENCONTRARNOS ALLÍ.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DEL CHAT PRO QUEDADAS VARIAS DE LA PLATAFORMA PATREON SINGLES BARCELONA.\n\nCOLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SO\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311380653/)\\nmeetup_id:311380653	2025-10-24	21:30	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/529762471/highres/
429	Biking&New Friends: Paseos, encuentros y café sorpresa	**🚨 Para participar en este evento y conocer la ubicación exacta, es obligatorio descargarse [aquí](https://onelink.to/5fkn72) la nueva app de WeRoad, WEMEET y apuntarse en el EVENTO correspondiente 🚨**\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/wemeet-20-30-40-anos-barcelona/events/311117517/)\\nmeetup_id:311117517	2025-10-18	17:45	\N	105	21	Location TBD		41.3851	2.1734	12	1	0.0	f	Bicycling	https://secure-content.meetupstatic.com/images/classic-events/529458444/highres/
430	Sunday Chess Meetup	This is a casual Sunday session for any level whether you're a daily blitzer or just getting started you'll find a friendly game and support. Just bring yourself and a chess set if you have one, if not no worries we'll make sure you get some games.\n\nTo get the latest updates about where the meetup will be (depending on the weather) check for comments on the event here in meetup.com.\n\n======== SPRING/SUMMER/AUTUMN ========\nSummer season starts April 6th 2025\n• 17:00-20:30 - Parc de la Ciutadella,\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-chess-meetup/events/311491888/)\\nmeetup_id:311491888	2025-10-31	17:00	\N	62	21	# Spring/Summer:• 17:00-21:00 - Parc de la Ciutadella, parc infantil https://bit.ly/3iEeo0w(we meet newbies 17:00-17:10 at the park gates on Pº de Pujades  # Winter and bad weather (currently under trial):• 16:00-19:00 - Restaurant Mehman Khana, Pl del Regomir, 08002, Barcelona (Barrio Gótico)		41.388123	2.1860152	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/491620901/highres/
431	🤩❤️🍹ENCUENTRO ONLINE PARA CHATEAR TODOS LOS LUNES, MIÉRCOLES Y VIERNES.	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigos-singles-barcelona/events/311429137/)\\nmeetup_id:311429137	2025-10-27	22:00	\N	103	21	Location TBD		41.3851	2.1734	0	5	0.0	f	General	\N
432	🤩❤️🍹NEW SUBGRUPO AMIGOS DEL FRANKFURT Y DISCO Q EN PEDRALBES. LET'S GO DANCE!!	🤩❤️🍹NEW SUBGRUPO AMIGOS DEL FRANKFURT Y DISCO Q EN PEDRALBES\n\nNOS PONEMOS DE ACUERDO POR EL CHAT GENERAL PARA ENCONTRARNOS.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311276515/)\\nmeetup_id:311276515	2025-10-18	23:59	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/525392818/highres/
433	NEW SUBGRUPO PARA IR JUNTOS A LAS COMMON PEOPLE PARTY DE RAZZMATAZZ SOLO SINGLES	NEW SUBGRUPO PARA IR JUNTOS A LAS COMMON PEOPLE PARTY DE RAZZMATAZZ SOLO SINGLES\n\nVAMOS HACIENDO GRUPITO PARA IR A LAS PARTIES\n\nCOMENTA TU INTERÉS EN EL CHAT PRO BAILA ROCK DE NUESTRA NUEVA WEB:\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT PRO DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https:\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311409689/)\\nmeetup_id:311409689	2025-10-26	18:00	\N	104	21	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530345682/highres/
434	Tuesday NEW Meetup - Language exchange &Social Drink&Karaoke+ Party Night)	📲💬 Join our Whatsapp group:\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n\nAre you ready for Tuesday night?\n**Today we meet at 22:30 at Red Garter Barcelona**\n\n**(Pg. de Colom, 23, Ciutat Vella, 08002 Barcelona)**\n\nIt's time to meet new people, practice languages, and have a blast!\n\nIt's close to Barceloneta and has Nice Vibes, Good Food, and Great Drink for your night.\n\nAt our meetup, you'll have the opportunity to connect with individuals from diverse backgrounds, all eager to make new frie\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/french-spanish-language/events/311328961/)\\nmeetup_id:311328961	2025-10-21	22:30	\N	64	23	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	1	0.0	f	International Friends	https://secure-content.meetupstatic.com/images/classic-events/530486889/highres/
435	Tuesday NEW Meetup -Language exchange &Social Drink+Free Party)	HI EVERYONE🤩 Are you ready for tonight? 🥳\n\n📲💬 Join our Whatsapp group:\nGeneral group\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n(only for Girls) https://chat.whatsapp.com/KyEgHsTXwBn1WeX6Yqiv3o\nJOIN OUR WHATSAPP GROUP FOR FREE PARTY INFO\nhttps://chat.whatsapp.com/L7CsDxU9Fel96XJrXYa1DH\n\n**Today we meet at 22:30 at Red Garter Barcelona**\n\n**(Pg. de Colom, 23, Ciutat Vella, 08002 Barcelona)**\n\nJoin us for an exciting Event. It's time to meet new people, practice languages, and have a blast!\n\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-night-out-event-student-local-tourista-all-mix/events/311448067/)\\nmeetup_id:311448067	2025-10-28	22:30	\N	75	23	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	2	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/519506994/highres/
436	LANGUAGE EXCHANGE & KARAOKE + HAPPY HOUR & LA BIBLIO (FREE) 🍻	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/agendaculturalbcn/events/311479267/)\\nmeetup_id:311479267	2025-10-30	19:00	\N	69	23	Location TBD		41.3851	2.1734	0	2	0.0	f	General	\N
437	[AI Alliance] Connect On-prem Solutions via NLIP	This use case showcases how Natural Language Interaction Protocol (NLIP) could facilitate the integration of on-premises resources such as Active Directory with cloud providers such as ServiceNow. Special attention is paid to moderation of communications for signs of jailbreaking, etc. to combat some regular problems.\n\n**About the presenter**\n\n**Will Witten** is a pragmatic builder and customer educator focused on AI that actually ships and sticks. He specializes in translating plain-English req\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/big-data-developers-in-barcelona/events/311567703/)\\nmeetup_id:311567703	2025-10-23	18:00	\N	108	23	Online Event		\N	\N	0	1	0.0	t	Artificial Intelligence	https://secure-content.meetupstatic.com/images/classic-events/530767067/highres/
438	Fin de semana en Andorra, el país de los Pirineos: lagos, montañas y mucho más	**Descubre Andorra y disfruta del pequeño gran país del Pirineo**\n\nUn fin de semana muy completo con alojamiento en **céntrico hotel de 4 estrellas de Andorra la Vella en régimen de media pensión** (desayuno + cena) que nos permitirá descubrir Andorra y disfrutar del pequeño gran país del Pirineo. Andorra, conocido a nivel mundial por sus **increíbles pistas de esquí**, por la **cantidad y calidad de sus tiendas** y por sus **bancos**, posee un **entorno natural espléndido**, tiene una **histori\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/enjoy-barcelona-catalonia/events/310951311/)\\nmeetup_id:310951311	2025-11-22	08:00	\N	99	23	Plaza Universitat (entrada principal de la UB)		41.38667239999999	2.1638661	30	30	0.0	f	Arts & Culture	https://secure-content.meetupstatic.com/images/classic-events/505815013/highres/
378	COMIDA para conocer gente + sorteo + baile 	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/eventosyactividades/events/311505460/)\\nmeetup_id:311505460	2025-10-19	14:00	\N	72	21	Location TBD		41.3851	2.1734	24	16	0.0	f	Coffee	\N
379	Cena para conocer gente + Baile	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/eventosyactividades/events/311505464/)\\nmeetup_id:311505464	2025-10-18	20:30	\N	72	21	Location TBD		41.3851	2.1734	30	17	0.0	f	Coffee	\N
380	The Saturday Language Exchange - Pizza Night 	**🇬🇧 The Language Exchange Meetup in Barcelona 🌍**\n\nThis event will be held at Trafalgar, a pizza and cocktail club that makes quality homemade pizzas and cocktails. This unique spot is a cocktail bar, pizza restaurant and club all in one, what more could you ask for! We look forward to meeting you there.\n\nWe are a group of enthusiastic individuals looking to improve our fluency in our second languages while meeting new friends in Barcelona. We exchange all languages at various levels!\n\n🗓️ **Whe\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelonalanguageexchange/events/311395070/)\\nmeetup_id:311395070	2025-10-25	20:00	\N	73	21	A host will welcome you and will give you a sticker. Please, always show the sticker to the bartender in order to get your offer! / Un anfitrión te dará la bienvenida y te entregará una pegatina. Por favor, ¡muestra siempre la pegatina al camarero para obtener tu oferta!		41.3851	2.1734	0	10	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/521210988/highres/
381	🎉 Brunch Roulette - Conoce gente real, en tiempo real!	**🎉 Brunch Roulette – ¡Conoce gente real, en tiempo real!**\n\nVamos a disfrutar de otro brunch o desayuno relajado y social el domingo 19 de Octubre! 🥐☕️.\n\nEmpezaremos en **mesas pequeñas de 4–5 personas max** para que sea más fácil conversar y conocerse mejor.\n\nDespués de una hora (aprox), haremos una **rotación de mesas o juntaremos las mesas** — ¡así podrás conocer a más gente en cada ronda y hablar tranquilamente!\n\nCon este formato tratamos de ofrecer la oportunidad de conectar 🙂\n\nTe esperamo\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/meet-new-friends-every-week-at-brunch-roulette/events/311404533/)\\nmeetup_id:311404533	2025-10-19	11:30	\N	74	21	Pocapots Restaurante (se entra por el parking) -  Carrer del Comte Borrell, 33, L'Eixample, 08015 Barcelona		41.3762591	2.1636037	20	10	0.0	f	Coffee and Tea Socials	\N
382	Tuesday NEW Meetup -Language exchange &Social Drink+Free Party)	HI EVERYONE🤩 Are you ready for tonight? 🥳\n\n📲💬 Join our Whatsapp group:\nGeneral group\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n(only for Girls) https://chat.whatsapp.com/KyEgHsTXwBn1WeX6Yqiv3o\nJOIN OUR WHATSAPP GROUP FOR FREE PARTY INFO\nhttps://chat.whatsapp.com/L7CsDxU9Fel96XJrXYa1DH\n\n**Today we meet at 22:30 at Red Garter Barcelona**\n\n**(Pg. de Colom, 23, Ciutat Vella, 08002 Barcelona)**\n\nJoin us for an exciting Event. It's time to meet new people, practice languages, and have a blast!\n\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-night-out-event-student-local-tourista-all-mix/events/311330189/)\\nmeetup_id:311330189	2025-10-21	22:30	\N	75	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	2	0.0	f	Arts & Culture	https://secure-content.meetupstatic.com/images/classic-events/519506994/highres/
383	Barcelona Networking Presencial con Connecting People	### 🌟 Networking Método 3C en Barcelona – Barceloneta\n\n📍 **Hard Rock Café, Plaza de Catalunya 23, Barcelona**\n🗓 **Miércoles, 23 de octubre**\n⏰ **12:00 a 14:00 h**\n💶 **Invitados: 15€ (IVA incluido)**\n¿Quieres ampliar tu red de contactos en Barcelona y generar oportunidades reales para tu negocio?\nEn **Connecting People** hemos creado el **Método 3C (Conexión, Crecimiento y Compromiso)**, una dinámica de networking práctica, cercana y diferente que ya funciona en varias ciudades de España.\n🔹 **Qué\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/networking-barcelona-con-connecting-people/events/311373502/)\\nmeetup_id:311373502	2025-10-23	12:00	\N	76	21	Location TBD		41.3851	2.1734	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530540536/highres/
384	Eat & Meet KCN Desayuno Networking Barcelona Sur - 23 de octubre	Bienvenido a EAT & MEET.\nLos eventos donde todos los jueves en KCN sacamos nuestra vena más #foodie y la combinamos con el #networking.\nSi eres de Barcelona o alrededores o vas a estar por aquí con la intención de hacer negocios, emprender y dar a conocer tu proyecto entre empresarios de la zona queremos invitarte a un evento que marca la diferencia.\nMaridajes, comidas, cenas y desayunos con un elemento común.\nHacer negocios y ampliar tu red de contactos.\nLos EAT & MEET son encuentros empresaria\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/kairoclubdenegocios/events/310902282/)\\nmeetup_id:310902282	2025-10-23	09:30	\N	77	21	Location TBD		41.3851	2.1734	0	2	0.0	f	Business & Professional	https://secure-content.meetupstatic.com/images/classic-events/530032096/highres/
385	#2 Female Networking over coffee ☕ Casual get-together in Barcelona 💜	⚠️ **RSVP Note** (The No-Ghost Policy)\n*Since space is limited, please only RSVP if you’re sure you can join us.*\n*Before each event, I’ll be sending a quick message to confirm attendance - please make sure to check your inbox and reply. If I don’t hear back by the day before the event, your spot will automatically be released to someone on the waiting list.*\n*If something comes up, that’s totally fine - just update your RSVP on time so another lovely woman can take your place.*\n*This helps keep\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/women-s-coffee-network/events/311282693/)\\nmeetup_id:311282693	2025-10-17	18:00	\N	78	21	The event poster will be placed on our table.		41.3851	2.1734	10	10	0.0	f	Coffee and Tea Socials	https://secure-content.meetupstatic.com/images/classic-events/530241899/highres/
386	Crucero de Networking - 17-21 de octubre de 2025	**CRUCERO DE NETWORKING**\n17-21 de octubre de 2025\n¡Fantástico fin de semana en el mar a bordo del Costa Favolosa!\nUn maravilloso crucero de 4 días en el que, saliendo de Barcelona, visitaremos Marsella y Génova, y pasaremos un día entero en alta mar.\nIncluye:\n\n* Crucero cabina interior\n* Régimen de pensión completa más refrescos y cervezas\n* Tasas\n\n**Precio 595€**\n**Pagos**:\n\n* Paga y señal: 50€ - hasta el 19 de junio\n* 2ª pago: 270€ - hasta el 28 de julio\n* Último pago: 275€ - hasta el 29 de a\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/kairoclubdenegocios/events/308087343/)\\nmeetup_id:308087343	2025-10-17	12:00	\N	77	21	Location TBD		41.3851	2.1734	0	1	0.0	f	Business & Professional	https://secure-content.meetupstatic.com/images/classic-events/528207958/highres/
439	🤩❤️🍹CONSTRUYENDO EL MAYOR CHAT SINGLE DE BCN. COLABORA Y HAZ NUEVAS AMISTADES.	🤩❤️🍹CONSTRUYENDO EL MAYOR CHAT SINGLE DE BCN. COLABORA Y HAZ NUEVAS AMISTADES.\n\nPARTICIPA EN LOS CHATS DE LAS ACTIVIDADES QUE MÁS TE INTERESAN Y TAMBIÉN PROPÓN NUEVAS IDEAS. GRACIAS POR CONSTRUIR ACTIVIDAD SOCIAL PARA HACER NUEVOS AMIGOS Y AMIGAS.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311463346/)\\nmeetup_id:311463346	2025-10-29	21:00	\N	104	23	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/525434856/highres/
440	🤩❤️🍹LOS CHICOS INVITAMOS A PIZZA A LAS CHICAS. PIZZA GRATIS PARA LAS CHICAS.	🤩❤️🍹PIZZA PREVIA AL COPEO. NOS PONEMOS DE ACUERDO PARA IR A CENAR PIZZA SENCILLA LOCAL TIPO TELEPIZZA, DOMINO, ETC. QUE SALGA BARATO.\n\nNOS PONEMOS DE ACUERDO POR EL CHAT PRO COYOTE D7 PARA ENCONTRARNOS PARA CENAR PIZZA SENCILLA PREVIA AL COPEO EN COYOTE D7.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DEL CHAT PRO COYOTE D7 DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA.\n\nCOLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311258238/)\\nmeetup_id:311258238	2025-10-17	21:05	\N	104	23	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/526168629/highres/
441	🤩❤️🍹COMPARTIMOS SELFIES EN EL GIMNASIO PARA TENER NUEVAS IDEAS DE OUTFITS Y ..	🤩❤️🍹COMPARTIMOS SELFIES EN EL GIMNASIO PARA TENER NUEVAS IDEAS DE OUTFITS Y HACER NUEVAS AMISTADES QUE COMPARTEN NUESTRAS MISMAS AFICIONES Y VALORES DE MENTE SANA Y CORPORE SANO.\n\nLAS PUBLICAMOS EN EL CHAT SELFIE HOY\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DE UN CHAT DENTRO DE LA PLATAFORMA PATREON SINGLES BARCELONA. COLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SOCIAL. COGE LA PALA.\n\n[https://www.patreon.com/singlesbarcelona](https://www.patreon.com/singlesbarcelona)\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311324502/)\\nmeetup_id:311324502	2025-10-21	17:00	\N	104	23	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/525463957/highres/
442	🤩❤️🍹FRANKFURT CENA INFORMAL JÓVENES SINGLES PARA HACER NUEVAS AMISTADES ARIBAU	🤩❤️🍹CENA INFORMAL EN UN FRANKFURT JOVENES SINGLES EN LA ZONA ARIBAU CON CERVEZA FRESQUITA Y SALCHICHAS.\n\nNOS PONEMOS DE ACUERDO POR EL CHAT PRO QUEDADAS VARIAS PARA ENCONTRARNOS Y HACER NUEVAS AMISTADES EN EL EVENTO Y QUIÉN SABE SI CONOCER A ALGUIEN ESPECIAL.\n\nCON LA AYUDA DEL CHAT PRO QUEDADAS VARIAS NOS COORDINAMOS PARA ENCONTRARNOS ALLÍ.\n\nESTE SUBGRUPO SE ORGANIZA A TRAVÉS DEL CHAT PRO QUEDADAS VARIAS DE LA PLATAFORMA PATREON SINGLES BARCELONA.\n\nCOLABORA, PARTICIPA Y EMPUJA. CREA ACTIVIDAD SO\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigosbarcelona/events/311259829/)\\nmeetup_id:311259829	2025-10-17	21:30	\N	104	23	Location TBD		41.3851	2.1734	0	4	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/529762471/highres/
355	Sunday Chess Meetup	This is a casual Sunday session for any level whether you're a daily blitzer or just getting started you'll find a friendly game and support. Just bring yourself and a chess set if you have one, if not no worries we'll make sure you get some games.\n\nTo get the latest updates about where the meetup will be (depending on the weather) check for comments on the event here in meetup.com.\n\n======== SPRING/SUMMER/AUTUMN ========\nSummer season starts April 6th 2025\n• 17:00-20:30 - Parc de la Ciutadella,\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-chess-meetup/events/311288148/)\\nmeetup_id:311288148	2025-10-19	17:00	\N	62	21	# Spring/Summer:• 17:00-21:00 - Parc de la Ciutadella, parc infantil https://bit.ly/3iEeo0w(we meet newbies 17:00-17:10 at the park gates on Pº de Pujades  # Winter and bad weather (currently under trial):• 16:00-19:00 - Restaurant Mehman Khana, Pl del Regomir, 08002, Barcelona (Barrio Gótico)		41.388123	2.1860152	0	2	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/491620901/highres/
356	Tuesday NEW Meetup - Language exchange &Social Drink& Beer Pong + Party Night)	📲💬 Join our Whatsapp group:\nGeneral group\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n\nJOIN OUR WHATSAPP GROUP FOR FREE PARTY INFO\nhttps://chat.whatsapp.com/L7CsDxU9Fel96XJrXYa1DH\n\nDaily activities\nhttps://chat.whatsapp.com/BDc9wlgm9V58nFs5ylmBXf\n\nGirls onlyhttps://chat.whatsapp.com/KyEgHsTXwBn1WeX6Yqiv3o\n\nAre you ready for Tuesday night?\n**Today we meet at 22:30 at Rei de Copes**\n**(Pl. Reial, 10, Ciutat Vella, 08002 Barcelona)**\n\nIt's time to meet new people, practice languages, and have \\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/make-new-friends-in-barcelona/events/311330199/)\\nmeetup_id:311330199	2025-10-21	22:30	\N	63	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	2	0.0	f	International Friends	https://secure-content.meetupstatic.com/images/classic-events/519282442/highres/
357	Sunday Chess Meetup	This is a casual Sunday session for any level whether you're a daily blitzer or just getting started you'll find a friendly game and support. Just bring yourself and a chess set if you have one, if not no worries we'll make sure you get some games.\n\nTo get the latest updates about where the meetup will be (depending on the weather) check for comments on the event here in meetup.com.\n\n======== SPRING/SUMMER/AUTUMN ========\nSummer season starts April 6th 2025\n• 17:00-20:30 - Parc de la Ciutadella,\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-chess-meetup/events/311377242/)\\nmeetup_id:311377242	2025-10-24	17:00	\N	62	21	# Spring/Summer:• 17:00-21:00 - Parc de la Ciutadella, parc infantil https://bit.ly/3iEeo0w(we meet newbies 17:00-17:10 at the park gates on Pº de Pujades  # Winter and bad weather (currently under trial):• 16:00-19:00 - Restaurant Mehman Khana, Pl del Regomir, 08002, Barcelona (Barrio Gótico)		41.388123	2.1860152	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/491620901/highres/
358	Tuesday NEW Meetup - Language exchange &Social Drink& Beer Pong + Party Night)	📲💬 Join our Whatsapp group:\nGeneral group\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n\nJOIN OUR WHATSAPP GROUP FOR FREE PARTY INFO\nhttps://chat.whatsapp.com/L7CsDxU9Fel96XJrXYa1DH\n\nDaily activities\nhttps://chat.whatsapp.com/BDc9wlgm9V58nFs5ylmBXf\n\nGirls onlyhttps://chat.whatsapp.com/KyEgHsTXwBn1WeX6Yqiv3o\n\nAre you ready for Tuesday night?\n**Today we meet at 22:30 at Rei de Copes**\n**(Pl. Reial, 10, Ciutat Vella, 08002 Barcelona)**\n\nIt's time to meet new people, practice languages, and have \\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/make-new-friends-in-barcelona/events/311448064/)\\nmeetup_id:311448064	2025-10-28	22:30	\N	63	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	2	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/519282442/highres/
359	Sunday Chess Meetup	This is a casual Sunday session for any level whether you're a daily blitzer or just getting started you'll find a friendly game and support. Just bring yourself and a chess set if you have one, if not no worries we'll make sure you get some games.\n\nTo get the latest updates about where the meetup will be (depending on the weather) check for comments on the event here in meetup.com.\n\n======== SPRING/SUMMER/AUTUMN ========\nSummer season starts April 6th 2025\n• 17:00-20:30 - Parc de la Ciutadella,\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-chess-meetup/events/311409020/)\\nmeetup_id:311409020	2025-10-26	17:00	\N	62	21	# Spring/Summer:• 17:00-21:00 - Parc de la Ciutadella, parc infantil https://bit.ly/3iEeo0w(we meet newbies 17:00-17:10 at the park gates on Pº de Pujades  # Winter and bad weather (currently under trial):• 16:00-19:00 - Restaurant Mehman Khana, Pl del Regomir, 08002, Barcelona (Barrio Gótico)		41.388123	2.1860152	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/491620901/highres/
360	Tuesday NEW Meetup - Language exchange &Social Drink& Beer Pong + Party Night)	📲💬 Join our Whatsapp group:\nGeneral group\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n\nJOIN OUR WHATSAPP GROUP FOR FREE PARTY INFO\nhttps://chat.whatsapp.com/L7CsDxU9Fel96XJrXYa1DH\n\nDaily activities\nhttps://chat.whatsapp.com/BDc9wlgm9V58nFs5ylmBXf\n\nGirls onlyhttps://chat.whatsapp.com/KyEgHsTXwBn1WeX6Yqiv3o\n\nAre you ready for Tuesday night?\n**Today we meet at 22:30 at Rei de Copes**\n**(Pl. Reial, 10, Ciutat Vella, 08002 Barcelona)**\n\nIt's time to meet new people, practice languages, and have \\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/make-new-friends-in-barcelona/events/311556754/)\\nmeetup_id:311556754	2025-11-04	22:30	\N	63	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	2	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/519282442/highres/
361	Sunday Chess Meetup	This is a casual Sunday session for any level whether you're a daily blitzer or just getting started you'll find a friendly game and support. Just bring yourself and a chess set if you have one, if not no worries we'll make sure you get some games.\n\nTo get the latest updates about where the meetup will be (depending on the weather) check for comments on the event here in meetup.com.\n\n======== SPRING/SUMMER/AUTUMN ========\nSummer season starts April 6th 2025\n• 17:00-20:30 - Parc de la Ciutadella,\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-chess-meetup/events/311521743/)\\nmeetup_id:311521743	2025-11-02	17:00	\N	62	21	# Spring/Summer:• 17:00-21:00 - Parc de la Ciutadella, parc infantil https://bit.ly/3iEeo0w(we meet newbies 17:00-17:10 at the park gates on Pº de Pujades  # Winter and bad weather (currently under trial):• 16:00-19:00 - Restaurant Mehman Khana, Pl del Regomir, 08002, Barcelona (Barrio Gótico)		41.388123	2.1860152	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/491620901/highres/
362	Monday Meetup Night(Making new friends & Language Exchange) + Free Party	Join our weekly meetup. Lets make new friends while we sing. Local & international atmosphere.\n\nJoin the fun! Top ambience always! ! You can sing in your own language!!!\n\n**What To Do When You Arrive:**\nWhen you arrive it's **important** you say"KAZU" at the entrance. We're here to make friends and meet new people and not to sit down alone in the bar.\n\n**Our Top Priority!**\n**YOU WILL NEVER DRINK ALONE / MAKE NEW FRIENDS**\nWE have a tour guide to stick you guys together.\n\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/french-spanish-language/events/311312917/)\\nmeetup_id:311312917	2025-10-20	22:30	\N	64	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530470824/highres/
363	Tuesday NEW Meetup - Language exchange &Social Drink&Karaoke+ Party Night)	📲💬 Join our Whatsapp group:\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n\nAre you ready for Tuesday night?\n**Today we meet at 22:30 at Red Garter Barcelona**\n\n**(Pg. de Colom, 23, Ciutat Vella, 08002 Barcelona)**\n\nIt's time to meet new people, practice languages, and have a blast!\n\nIt's close to Barceloneta and has Nice Vibes, Good Food, and Great Drink for your night.\n\nAt our meetup, you'll have the opportunity to connect with individuals from diverse backgrounds, all eager to make new frie\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/french-spanish-language/events/311448066/)\\nmeetup_id:311448066	2025-10-28	22:30	\N	64	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530486889/highres/
364	🏳️‍🌈FRi!NDR | Sunday Social Meetup	🇪🇸🇪🇸🇪🇸🇪🇸🇪🇸🇪🇸🇪🇸🇪🇸\n✨ **\\*¡ÚNETE A NUESTRO EVENTO!\\*** ✨\n\n📆 **\\*Todos los Domingos\\***\n🕡 Desde las 15h00 hasta las 19h00\n📍 Playa de la Barceloneta\n🎟 **\\*Evento 100% GRATUITO\\***\n\n¡Ven tal como eres! 🌈\nTrae tu sonrisa, buena energía, algo de bebida y snacks.\n\n🤝 Haz networking • 🌍 Conoce nuevos amigos • 💬 Comparte historias y experiencias\n\n¡Te estamos esperando!\n\n\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\n\n🇬🇧🇬🇧🇬🇧🇬🇧🇬🇧🇬🇧🇬🇧🇬🇧\n**✨ \\*\\*\\*JOIN OUR EVENT!\\*\\*\\*✨**\n\n\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/friindrcommunity/events/311532508/)\\nmeetup_id:311532508	2025-10-19	15:00	\N	65	21	Please sen us a Whats App +33 695 895 400 to receive th eexact location. https://wa.me/33695895400		38.7945952	-106.5348379	20	3	0.0	f	Locals & New in Town	https://secure-content.meetupstatic.com/images/classic-events/530731681/highres/
365	Tuesday NEW Meetup - Language exchange &Social Drink&Karaoke+ Party Night)	📲💬 Join our Whatsapp group:\nhttps://chat.whatsapp.com/B6OUWR7lG2658PblVQZmyN\n\nAre you ready for Tuesday night?\n**Today we meet at 22:30 at Red Garter Barcelona**\n\n**(Pg. de Colom, 23, Ciutat Vella, 08002 Barcelona)**\n\nIt's time to meet new people, practice languages, and have a blast!\n\nIt's close to Barceloneta and has Nice Vibes, Good Food, and Great Drink for your night.\n\nAt our meetup, you'll have the opportunity to connect with individuals from diverse backgrounds, all eager to make new frie\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/french-spanish-language/events/311556756/)\\nmeetup_id:311556756	2025-11-04	22:30	\N	64	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530486889/highres/
366	Monday Meetup Night(Making new friends & Language Exchange) + Free Party	Join our weekly meetup. Lets make new friends while we sing. Local & international atmosphere.\n\nJoin the fun! Top ambience always! ! You can sing in your own language!!!\n\n**What To Do When You Arrive:**\nWhen you arrive it's **important** you say"KAZU" at the entrance. We're here to make friends and meet new people and not to sit down alone in the bar.\n\n**Our Top Priority!**\n**YOU WILL NEVER DRINK ALONE / MAKE NEW FRIENDS**\nWE have a tour guide to stick you guys together.\n\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/french-spanish-language/events/311540894/)\\nmeetup_id:311540894	2025-11-03	22:30	\N	64	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530470824/highres/
367	Language Exchange Saturdays	*This event description is available in English and Spanish. English version first, Spanish version below.*\n*La descripción de este evento está disponible en inglés y español. La versión en inglés está primero, la versión en español abajo.*\n\n**English version:**\n\n### **🌍**\n\n### **Language Exchange Saturdays – Meet New People & Practice Languages in Barcelona!**\n\nLooking for a fun and friendly way to meet new people in Barcelona? Join us for **Language Exchange Saturdays**, a weekly social event \\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/friendly-vibes/events/311490232/)\\nmeetup_id:311490232	2025-10-18	21:00	\N	66	21	Location TBD		41.3851	2.1734	0	32	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530636136/highres/
368	Amigos Barcelona English Speakers Meetup, Residents only 	*Please note: a one-drink minimum per person is required.*\nWelcome to our weekly Meetup group for Expats & English speakers permanently living in Barcelona! If you're a Barcelona local looking for a laid-back way to connect with fellow English speakers & residents, this is the perfect gathering for you. Whether you've lived in Barcelona for years or are new to the city, our informal meetups provide a great opportunity to socialize, unwind, and forge connections with like-minded individuals who c\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-english-speakers-meetup/events/310654717/)\\nmeetup_id:310654717	2025-10-17	19:45	\N	67	21	We will be in front of the bar		41.3851	2.1734	0	14	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/512910403/highres/
369	Language exchange and make new friends in Barcelona at SAVANNAH	Hi everybody!\n\nGet enrolled if you want to meet new people in Barcelona. I am from Barcelona and the goal of this new group is to meet interesting people while having a few drinks.\n\nThis group is open to all nationalities.\n\nIn order to create a good atmosphere it's very important that in your profile you have a clear picture of you. If you do not have a picture of yourself, you will be kindly moved to waiting list. Even if you see waiting list try to get enrolled as I Will be accepting to keep a\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-talking-about-feelings-meetup-group/events/311134666/)\\nmeetup_id:311134666	2025-10-18	20:15	\N	68	21	Savannah, Vidrieria street, 6		32.0808989	-81.091203	0	35	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/529373998/highres/
370	Amigos 30+ Barcelona English Speakers Meetup, Residents only 	*Please note: a one-drink minimum per person is required.*\nWelcome to our weekly Meetup group for Expats & English speakers permanently living in Barcelona! If you're a Barcelona local looking for a laid-back way to connect with fellow English speakers & residents, this is the perfect gathering for you. Whether you've lived in Barcelona for years or are new to the city, our informal meetups provide a great opportunity to socialize, unwind, and forge connections with like-minded individuals who c\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-english-speakers-meetup/events/310654719/)\\nmeetup_id:310654719	2025-10-24	20:00	\N	67	21	We will be in front of the bar		41.3851	2.1734	0	3	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/512910403/highres/
371	NEW INTERNATIONAL BRUNCH 	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/agendaculturalbcn/events/311387706/)\\nmeetup_id:311387706	2025-10-25	12:30	\N	69	21	Location TBD		41.3851	2.1734	50	2	0.0	f	General	\N
372	Social Media Creators & Influencers Meetup (virtual) #51	Hi there, fellow social media enthusiasts, welcome to our meetup! We at Social Rising organize regular meetups for creators & influencer from every corner of the social media world.\n\nStay up-to-date on virtual & in-person event information by subscribing to our newsletter: https://socialrising.com/join\n\n**What do participants & speakers think?**\n"Matteo’s meetups are incredible. Every time I come, I meet people who genuinely change my life. He somehow manages to get everyone involved, and the ov\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/social-rising-barcelona/events/311539084/)\\nmeetup_id:311539084	2025-10-30	18:00	\N	70	21	Online Event		\N	\N	0	3	0.0	t	Digital Marketing	https://secure-content.meetupstatic.com/images/classic-events/530738696/highres/
373	HALLOWEEN - Let's make new friends in Barcelona at xxx	Hi everybody!\n\nGet enrolled if you want to meet new people in Barcelona. I am from Barcelona and the goal of this new group is to meet interesting people while having a few drinks.\n\nThis group is open to all nationalities.\n\nIn order to create a good atmosphere it's very important that in your profile you have a clear picture of you. If you do not have a picture of yourself, you will be kindly moved to waiting list. Even if you see waiting list try to get enrolled as I Will be accepting to keep a\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-talking-about-feelings-meetup-group/events/310895008/)\\nmeetup_id:310895008	2025-10-31	21:00	\N	68	21	SECRET PLACE (?) ;)		41.3851	2.1734	0	13	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/527027024/highres/
374	KARAOKE EDITION - Language exchange and make new friends Barcelona at TouchPlay	Hi everybody!\n\nIf you want to attend the karaoke you need to pay the ticket of 12€ beforehand. A drink is included. Send the money by Friday on the account of booking the tables. use the following links or DM if you want my number to send a Bizum.\nPayPal.me/eventsbcnfriends or revolut.me/javier0913\n\nGet enrolled if you want to meet new people in Barcelona. I am from Barcelona and the goal of this new group is to meet interesting people while having a few drinks.\n\nThis group is open to all nation\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-talking-about-feelings-meetup-group/events/310360423/)\\nmeetup_id:310360423	2025-10-25	19:30	\N	68	21	TOUCH MUSIC KARAOKE		41.3897525	2.1958731	0	11	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/529463274/highres/
375	Let's make new friends in Barcelona at GABY'S CLUB	Hi everybody!\n\nGet enrolled if you want to meet new people in Barcelona. I am from Barcelona and the goal of this new group is to meet interesting people while having a few drinks.\n\nThis group is open to all nationalities.\n\nIn order to create a good atmosphere it's very important that in your profile you have a clear picture of you. If you do not have a picture of yourself, you will be kindly moved to waiting list. Even if you see waiting list try to get enrolled as I Will be accepting to keep a\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-talking-about-feelings-meetup-group/events/310537441/)\\nmeetup_id:310537441	2025-10-24	21:00	\N	68	21	Topazi, 24		41.3851	2.1734	0	16	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/521813814/highres/
376	VERMUT para gente nueva...y no tanto😜🥃	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/bcn-gastronomic-society/events/311539713/)\\nmeetup_id:311539713	2025-10-25	12:00	\N	71	21	Location TBD		41.3851	2.1734	40	26	0.0	f	Beer	\N
377	Monday Meetup Night(Making new friends & Language Exchange) + Free Party	Join our weekly meetup. Lets make new friends while we sing. Local & international atmosphere.\n\nJoin the fun! Top ambience always! ! You can sing in your own language!!!\n\n**What To Do When You Arrive:**\nWhen you arrive it's **important** you say"KAZU" at the entrance. We're here to make friends and meet new people and not to sit down alone in the bar.\n\n**Our Top Priority!**\n**YOU WILL NEVER DRINK ALONE / MAKE NEW FRIENDS**\nWE have a tour guide to stick you guys together.\n\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/french-spanish-language/events/311430448/)\\nmeetup_id:311430448	2025-10-27	22:30	\N	64	21	SAY LISTA KAZU AT DOOR		41.3851	2.1734	0	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530470824/highres/
387	Aumenta tu potencial con n8n en la era de la IA	En InnoIT Consulting, estamos encantados de invitaros a nuestro próximo meetup, el **miércoles 22 de octubre a las 18:30h.**\n\n🎙️*Aumenta tu potencial con n8n en la era de la IA*\n\n**RESUMEN**\n\nContaremos con **[Marc Benito](https://www.linkedin.com/in/marcbenito/)** (Software Engineer).\n\n¿Sabías que la mayoría de los equipos pierden tiempo valioso en tareas repetitivas que podrían automatizarse? En esta charla descubrirás cómo las herramientas **no code** como **n8n** están revolucionando la form\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/meetup-de-innoit-consulting-en-barcelona/events/311197776/)\\nmeetup_id:311197776	2025-10-22	18:30	\N	79	21	Oficinas InnoIT Consulting		41.3918981	2.1695333	110	99	0.0	f	Artificial Intelligence	https://secure-content.meetupstatic.com/images/classic-events/530502141/highres/
388	Python Meetup October: MCPs & Access Control Systems for AI	For this month's Meetup, we are partnering with **Codurance** to offer two sessions: **Securing AI** and **Python + MCPs**.\n\n\\-\\-\\-\nSchedule:\n\n* 👋 & 🗣️ 18:30: Welcome and Talks\n* 🍕 **&** 🍻 19:45: Networking, food and drinks!\n* 👋 20:30: Bye!\n\n\\-\\-\\-\n\n* ➡️ **What:** Securing AI: a journey through access control systems\n* 📢 **Who**: *Carla Urrea Stabile*\n* ⏱ **Duration**: 30 minutes\n* 👅 **Language**: English\n* 🧐 **Abstract**: Remember when you started working on that application and only admins cou\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/python-barcelona/events/311354313/)\\nmeetup_id:311354313	2025-10-23	18:30	\N	80	21	Location TBD		41.3851	2.1734	70	70	0.0	f	Artificial Intelligence	https://secure-content.meetupstatic.com/images/classic-events/530528895/highres/
389	Barcelona CyberSec Networking Event (Wed 22/10)	We’re back — now as **Barcelona CyberSec**! 🚀\n\nOur community has a new name, new energy, and new ideas, but the same relaxed vibe.\n\nThis meetup is for anyone into (or curious about) cybersecurity in Barcelona: red team, blue team, GRC, engineering, students, or seasoned pros.\n\nWhat to expect:\n\n* Connect with others working or interested in cybersecurity\n* Share tips, tools, and experiences\n* Discuss the latest cyber trends and threats\n* Shape future events (talks, coffee + cyber chats, more netw\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-cybersec/events/311266869/)\\nmeetup_id:311266869	2025-10-22	19:30	\N	81	21	Find a rubber duck on the table		41.3851	2.1734	30	29	0.0	f	Artificial Intelligence	https://secure-content.meetupstatic.com/images/classic-events/530441562/highres/
390	System Design on AWS with Mandeep Singh	🚀 Get ready for our next AWS User Group Barcelona meetup, hosted at **[Altia](https://www.altiacompany.com/)**[!](https://www.altiacompany.com/)\n\nThis time, we're talking with one of the most foremost experts on the AWS cloud.\n\n🎙️ **A Deep Dive into System Design on AWS**\nWe're incredibly excited to welcome **[Mandeep Singh](https://www.linkedin.com/in/msdeep14/)**, co-author of the fantastic O'Reilly book "System Design on AWS"! He'll be sharing his expertise on building scalable, resilient, an\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-amazon-web-services-meetup/events/311524825/)\\nmeetup_id:311524825	2025-10-16	18:30	\N	82	21	La Biblioteca		45.2725028	-123.0161155	0	32	0.0	f	Amazon Web Services	https://secure-content.meetupstatic.com/images/classic-events/530722936/highres/
391	 DevOps Bcn 🤝 Grafana & Friends	Hi everyone 👋\n\nFor October, we are partnering with the [DevOps BCN community](https://www.meetup.com/devops-bcn-group/) for their next meetup at [Allianz Technology Spain](https://tech.allianz.com/en/contact/spain.html).\n\n🚨To attend, don't forget to RSVP at 👉🏼 [https://www.meetup.com/devops-bcn-group/events/311265939](https://www.meetup.com/devops-bcn-group/events/311265939) 🚨\n\n**🎙️ [Niki Manoledaki](https://www.linkedin.com/in/niki-manoledaki-9b505111b/)**, Senior Software Engineer at **[Grafan\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/grafana-and-friends-barcelona/events/311284723/)\\nmeetup_id:311284723	2025-10-30	18:30	\N	83	21	Location TBD		41.3851	2.1734	1	1	0.0	f	Cloud Computing	https://secure-content.meetupstatic.com/images/classic-events/530501111/highres/
392	TechTalks | Data Analytics for Business Growth	We are kicking off TechFems events for this fall with a Data Analytics session at [Dow Jones](https://www.dowjones.com/dj-tech-barcelona/) 📈, open to everyone.\n\n🚨 **To attend, RSVP at** [https://www.eventbrite.com/e/techtalks-data-analytics-for-business-growth-tickets-1778179896939](https://www.eventbrite.com/e/techtalks-data-analytics-for-business-growth-tickets-1778179896939). **This meetup does not accept RSVPs as we track attendance via Eventbrite** this time 🚨\n\n**Agenda**\n6:00 PM - Door ope\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/techfems/events/311410596/)\\nmeetup_id:311410596	2025-10-30	18:00	\N	84	21	Carrer de la Diputació, 409, L'Eixample, 08013 Barcelona		41.3981127	2.1770254	1	1	0.0	f	Data Analytics	https://secure-content.meetupstatic.com/images/classic-events/530621383/highres/
393	Product Design & AI Networking Event	**Join Us for a Product Design Networking Meetup at Barcelona!**\nAre you passionate about product design? Looking to connect with fellow designers, share ideas, and showcase your latest work? Then this is the event for you!\n\nEnjoy a relaxed evening of networking with some minds in the industry while sipping on craft beers from Brewdog. Whether you're an experienced product or design person or just getting started, this is a great opportunity to exchange ideas, find inspiration, and build valuabl\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-product-and-design-tech-networking/events/310894656/)\\nmeetup_id:310894656	2025-10-22	19:00	\N	85	21	Location TBD		41.3851	2.1734	0	13	0.0	f	General	\N
394	How AI impacts Tech Hubs, and how organizations deal with these new tools	👋 Curious about how AI is reshaping technology hubs?\n\nWe’re excited to invite you to the next edition of our **Talented People** event series:\n\n**The Impact of AI on Technology Hubs: How Organizations Adapt and Thrive with Emerging Tools**\n\n🗝️ **What’s this event about?**\nArtificial Intelligence is transforming the way technology hubs operate — from accelerating product development to redefining organizational structures and talent strategies. This panel discussion will explore how companies are\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/talented-by-talent-r-where-great-minds-meet/events/311320659/)\\nmeetup_id:311320659	2025-10-22	18:30	\N	86	21	Location TBD		41.3851	2.1734	100	78	0.0	f	Professional Development	https://secure-content.meetupstatic.com/images/classic-events/530638791/highres/
395	OWASP Barcelona presents: AppSec Core Professional Skills	*AppSec is more than tools and tests.* Success depends on the human skills that earn trust, secure buy-in, and create real change.\nJoin us on **October 23rd at 19:00** at the Geneva Business School in Barcelona for a talk by **Ed Woodfall** on the *core professional skills* AppSec professionals need to thrive.\n\n✅ **What you’ll learn:**\n\n* Why influence and communication matter as much as technical chops\n* How to partner with developers and product teams instead of blocking them\n* Building “paved\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/owasp-barcelona-chapter/events/311268128/)\\nmeetup_id:311268128	2025-10-23	19:00	\N	87	21	Location TBD		41.3851	2.1734	0	37	0.0	f	Application Security	https://secure-content.meetupstatic.com/images/classic-events/530442279/highres/
396	⚓ Wild North 🌊 Cales Verges entre Colera i Llançà  	**(CAST a continuación ⛱️ EN below)**\n\n**Senderisme a la vora del mar – diumenge 19 d’octubre**\n\nUn dels últims trams del **Camí de Ronda**, just abans d’arribar a la frontera francesa. Un sector impressionant i sorprenentment poc conegut: entre **Llançà i Colera**, un reguitzell de cales espectaculars ens espera per relaxar-nos i carregar piles.\n\nUna ruta curta i assequible, de **9 km i només 130 m de desnivell acumulat**, que ens regala uns paisatges diferents de la resta de la Costa Brava. Pe\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/nature-connect/events/311356283/)\\nmeetup_id:311356283	2025-10-19	08:15	\N	88	21	Location TBD		41.3851	2.1734	25	15	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/498095142/highres/
397	Social event networking event 	In this event, you’ll experience the power of networking and shared creativity.\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/she-links/events/311241618/)\\nmeetup_id:311241618	2025-10-27	17:00	\N	89	21	Location TBD		41.3851	2.1734	15	1	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530406466/highres/
398	Tech Networking - Web Summit Edition	**Meet fellow Web Summit attendees over beers before the chaos begins**\nHeading to Web Summit Lisbon this year? Join us for a relaxed pre-conference meetup where you can connect with other attendees who'll be navigating the massive event alongside you.\n\n## Why join us?\n\nWeb Summit can be overwhelming—70,000+ attendees, hundreds of talks, endless exhibitor booths. Before diving into that whirlwind, come grab a beer with a smaller crew of people from across the tech ecosystem. Share which talks yo\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-product-and-design-tech-networking/events/311357463/)\\nmeetup_id:311357463	2025-10-21	19:00	\N	85	21	Location TBD		41.3851	2.1734	0	10	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530528284/highres/
399	🎃 BCN English Speakers – Halloween Meetup at Wild Rover 👻	We are **Barcelona English Speakers**, a friendly community of 2000+ people brought together by a shared language. Every month, we host a free social meet-up so you can connect, chat, and meet new faces.\n\nThis time, we’re turning things spooky! 🎃👻\n\nYou're Invited to Our **Spooktacular Halloween Meetup!** 🕸️🦇\n\nGet your costumes ready and join us for a night of frightful fun, chilling treats, and killer music — the perfect mix of scary and social. 😈\n\n📆 **Friday, October 24th**\n🕘 **From: 9:00 PM ‘t\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelona-english-speakers/events/311477096/)\\nmeetup_id:311477096	2025-10-24	21:00	\N	90	21	Location TBD		41.3851	2.1734	100	32	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/530654018/highres/
400	COMPLET! VISITEM LA CASA DELS ÀNGELS DEL MAG LARI 	*Tothom coneix el Mag Lari, però… t’imagines descobrir el seu món més personal?* Avui et convidem a **una experiència que va més enllà de qualsevol truc:** una visita guiada a **la Casa dels Àngels, una joia del segle XVI a Castellserà, plena de secrets, històries i moltes rialles**.\n\n*Perquè aquesta no és una casa qualsevol, és un lloc on tot és possible!* Recorre els seus racons més amagats, obre portes secretes i atreveix-te a baixar per les seves escales sinistres. **T’esperen objectes sorpr\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/cultura-i-oci-barcelona/events/311402545/)\\nmeetup_id:311402545	2025-11-29	08:30	\N	93	21	Online Event		\N	\N	15	30	0.0	t	Day Trips	https://secure-content.meetupstatic.com/images/classic-events/530587322/highres/
401	🏆🔥  TOURNAMENT Basic Level - Beach Volley ATP - 9:00 AM - (Coach: Breno)	**¡Hola, ATPeople!**\n\n¡Es hora de otro torneo de ATP Beach Volley! 🏐🔥\nUna oportunidad perfecta para poner a prueba nuestras habilidades, disfrutar de una mañana de vóley en la playa y compartir un buen rato con la comunidad ATP. Música, buena vibra y muchos juegos nos esperan.\n\n🔹 **Premios:**\n\n**Serie Oro:**\n🏆 1º Lugar: Medallas + Gafas + Calcetines.\n🥈 2º Lugar: Medallas + Gafas + Calcetines.\n\n**Serie Plata:**\n🏆 1º Lugar: Medallas + Gafas\n🥈 2º Lugar: Medallas + Gafas\n\n🔹 **Formato del Torneo:**\n\n\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelonavolley/events/311500640/)\\nmeetup_id:311500640	2025-10-26	09:30	\N	91	21	Location TBD		41.3851	2.1734	50	34	0.0	f	New In Town	https://secure-content.meetupstatic.com/images/classic-events/530688333/highres/
402	🔥4 plazas 🙋🏻45-65 🚌 BUS URBANO 💦 Molí de Brotons 🌊 Intermedio 11km 💪🏽	⭐️⭐️⭐️⭐️⭐️\n**❤️ Toda la info y para apuntarte [aquí](https://thehikers.es/products/45-65-anos-increible-moli-de-brotons-26-07-25?utm_source=MeetUp&utm_medium=MeetUp&utm_content=45-65-anos-increible-moli-de-brotons-26-07-25) 👈🏾**\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/thehikers_barcelona/events/311409145/)\\nmeetup_id:311409145	2025-10-18	09:00	\N	92	21	Location TBD		41.3851	2.1734	0	37	0.0	f	Nature	https://secure-content.meetupstatic.com/images/classic-events/530593970/highres/
403	‼️Lista de Espera‼️Espectaculares cimas +2000 m en Vallter ⛰️ (Pirineos)	📸 [Instagram](https://www.instagram.com/hikingbcn/)\n\n**¡VIVE LA MAGIA DEL PIRINEO CON UNA ESCAPADA DE ALTURA!** 🌄✨\n\nEl otoño pirenaico 🍂 nos invita a descubrir paisajes de alta montaña cargados de energía, donde la naturaleza muestra su grandeza en cada cima. Te proponemos una aventura inolvidable en la zona de **Vallter 2000**, un rincón privilegiado de los Pirineos.\nDurante dos días recorreremos algunas de las cumbres más emblemáticas de la región: el mítico **Bastiments (2.881 m)** 🏔️, la ele\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/hiking-barcelona/events/310779307/)\\nmeetup_id:310779307	2025-10-25	08:00	\N	94	21	Location TBD		41.3851	2.1734	28	24	0.0	f	Hiking	https://secure-content.meetupstatic.com/images/classic-events/529899022/highres/
404	9º Afterwork en Candy Darling. Vente! 	(Esp)\n\nHey!\n\nPlan sencillo: Nos vemos en el Candy darling para ponernos al día o para ponernos cara si aún no nos conocemos en persona.\n\nDependiendo del interés quizá tengamos algunos juegos de conversación (cómo excusa) para romper el hielo.\n\nEl Candy darling nos va genial por qué:\n\nEstá en plaza Universidad,\n\nel volumen de la música por la tarde permite hablar sin gritar (si, es un argumento de abuelo, haha)\n\ny lo más importante. Todo el mundo es bienvenido.\n\nEs ya nuestro 9º afterwork en un a\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/lgtbiq-friends-in-barcelona/events/311170423/)\\nmeetup_id:311170423	2025-10-24	19:30	\N	95	21	Nos vemos dentro! cerca de la entrada, a la derecha enfrente de la barra		41.3851	2.1734	0	29	0.0	f	Friendships	https://secure-content.meetupstatic.com/images/classic-events/523951500/highres/
405	The Saturday Language Exchange - Pizza Night 	**🇬🇧 The Language Exchange Meetup in Barcelona 🌍**\n\nThis event will be held at Trafalgar, a pizza and cocktail club that makes quality homemade pizzas and cocktails. This unique spot is a cocktail bar, pizza restaurant and club all in one, what more could you ask for! We look forward to meeting you there.\n\nWe are a group of enthusiastic individuals looking to improve our fluency in our second languages while meeting new friends in Barcelona. We exchange all languages at various levels!\n\n🗓️ **Whe\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelonalanguageexchange/events/310903688/)\\nmeetup_id:310903688	2025-10-18	20:00	\N	73	21	A host will welcome you and will give you a sticker. Please, always show the sticker to the bartender in order to get your offer! / Un anfitrión te dará la bienvenida y te entregará una pegatina. Por favor, ¡muestra siempre la pegatina al camarero para obtener tu oferta!		41.3851	2.1734	0	19	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/521210988/highres/
406	🔥🏐 Beach Volley ATP - Basic Level Training 16:30 - (Coach: Martí) - [ES] 	**CONFIRMACIÓN POR WHATSAPP:** [+34 674 335 660](https://api.whatsapp.com/send/?phone=34674335660&text=Hola%21&type=phone_number&app_absent=0)\n\n(ESP) **¡Entrenamiento de Voleibol para Principiantes! 🏐**\n¿Nunca has jugado voleibol o apenas estás empezando? ¡Este es el lugar perfecto para ti! 🎉 Únete a nuestro entrenamiento de nivel básico donde aprenderás los fundamentos del voleibol en un ambiente divertido y relajado. 😊\n\n🕕 **Hora:**\n\n16:30 - 18:00\n\nNo importa si no tienes experiencia, aquí esta\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelonavolley/events/311282405/)\\nmeetup_id:311282405	2025-10-19	16:30	\N	91	21	Location TBD		41.3851	2.1734	10	3	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/523368741/highres/
407	International After work in Gracia	Hello Everyone,\nwe will organise an afterwork event in Gracia en el Bar el Cine. Variety of international and national beers and cocktails!!!\nEconomic prices.\nSpanish Tapas and 70s 80s 90s music\nGet to know new people and have a nice time!!\n#Party #makefriends #Gracia #Tapas.This event is free and a drink is required.\nWe are waiting for you!!!\n\\`\\`\\`\nHola a tod@s\nOrganizaremos un afterwork en Gracia en el Bar el Cine. Variedad de cervezas y cócteles nacionales e internacionales!!!\nPrecios económ\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/www-cosmoitas-com/events/311258679/)\\nmeetup_id:311258679	2025-10-17	19:30	\N	97	21	Entrada pregunta por Masaya, o  Marcelo/Entry asks for Masaya, or a Marcelo		37.7716511	-7.981084500000001	63	7	0.0	f	Communication Skills	https://secure-content.meetupstatic.com/images/classic-events/520808892/highres/
408	🏃‍♂️🍁🌲 RUTA OTOÑAL Y FLUVIAL  "EL TOU"	Bonita ruta semicircular desde Tordera que nos adentrará a los bellos paisajes otoñales con chopos,robles y encinas.Pasaremos por el paseo fluvial del río tordera,fuentes,masías,campos agrarios y construcciones históricas.Acabaremos viendo el casco antiguo del pueblo.\n\nDistancia: 10km aprox.\n\nTiempo: 2h 45m aprox(acabamos sobre las 14h)\n\nDificultad: Fácil (casi toda plana).\n\n🏃‍♂️🌳🍁 PLAN:\n\n⏲ Kedada: 9.45h paseo de gracia n3 (és un portal). ÒSCAR,wsp (mi telf. está en el apartado "cómo encontrarno\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/onbassbcncom/events/311461820/)\\nmeetup_id:311461820	2025-10-19	09:45	\N	96	21	9.45h PASEO DE GRACIA Nº3 (ÉS UN PORTAL). ÒSCAR, 636118101 WSP, GORRA ROJA.		41.3880345	2.170281	40	30	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/530641037/highres/
409	🔥🏐 Beach Volley ATP - Basic Level Training 16:30 - (Coach: Martí) - [ES] 	**CONFIRMACIÓN POR WHATSAPP:** [+34 674 335 660](https://api.whatsapp.com/send/?phone=34674335660&text=Hola%21&type=phone_number&app_absent=0)\n\n(ESP) **¡Entrenamiento de Voleibol para Principiantes! 🏐**\n¿Nunca has jugado voleibol o apenas estás empezando? ¡Este es el lugar perfecto para ti! 🎉 Únete a nuestro entrenamiento de nivel básico donde aprenderás los fundamentos del voleibol en un ambiente divertido y relajado. 😊\n\n🕕 **Hora:**\n\n16:30 - 18:00\n\nNo importa si no tienes experiencia, aquí esta\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/barcelonavolley/events/311265483/)\\nmeetup_id:311265483	2025-10-18	16:30	\N	91	21	Location TBD		41.3851	2.1734	10	3	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/523368741/highres/
410	Adivina el Número de tu Compañero [JUEGO SOCIAL NUMEROLOGíA]	**[Grupo Whatsapp MODO SOCIAL](https://chat.whatsapp.com/JHQ0Yf00Fkh3PtTKC1fKzS)** **¿Qué número eres en realidad?**\nEn un ambiente relajado y divertido, exploraremos la esencia de cada número —desde la fuerza del 1 hasta la sabiduría del 9— y también la potencia especial de los números maestros: la intuición del 11, la visión del 22 y la misión espiritual del 33.\n\nTus compañeros jugarán a representar diferentes vibraciones numéricas y tú tendrás que afinar tu intuición, observar detalles y dedu\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/modo-social/events/311319415/)\\nmeetup_id:311319415	2025-10-25	19:00	\N	98	21	Location TBD		41.3851	2.1734	60	12	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/530499329/highres/
411	El Dado Social [JUEGO]	**[Grupo Whatsapp MODO SOCIAL](https://chat.whatsapp.com/JHQ0Yf00Fkh3PtTKC1fKzS)** 🎲 ¿Te imaginas un dado gigante decidiendo tu destino social?\n🎲 ¿Quieres conectar, reír y dejar que la suerte te sorprenda?\n🎲 ¿Te apetece pasar un buen rato… aunque no siempre te toque la mejor tirada? 😏\n\nEntonces **Dado Social** es tu evento.\n\nEn este evento, el protagonista no es el azar de un casino ni el clásico parchís de la abuela: es un **dado gigante** que marcará dinámicas, retos y momentos de conexión con\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/modo-social/events/311319113/)\\nmeetup_id:311319113	2025-10-18	19:00	\N	98	21	Location TBD		41.3851	2.1734	80	13	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/530499089/highres/
412	🔒 GRUPO COMPLETO 🍂🍄🌋 Castellfollit - La Garrotxa🍄🌋🍂	**👉 Este grupo es para ti si...**\n\n* 💪🏻 Tienes el nivel físico que exige la ruta\n* 😃 Traes buena energía y ganas de pasarlo bien\n\n🌲 **¿ CÓMO RESERVAR PLAZA ? :**\n\n1. Pulsa asistiré en este meetup\n2. Deja tu móvil al inscribirte\n3. Acepta la Normativa de Seguridad [aquí](https://forms.gle/B5DzcPVxBSYNfyAH7)\n4. Haz pago reserva de plaza [aquí](https://www.guaita.info/event-details/castellfollit-la-garrotxa-1)\n\n**🍒 EDAD PREDOMINANTE Excursiones de 1 Día:** Entre 30 y 49 años.\n\n★ **POR QUÉ ELEGIR GU\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/guaita/events/311067103/)\\nmeetup_id:311067103	2025-10-18	07:55	\N	100	21	Location TBD		41.3851	2.1734	20	23	0.0	f	Nature	https://secure-content.meetupstatic.com/images/classic-events/530226140/highres/
413	Auténtica cocina China 	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/bcn-gastronomic-society/events/311318977/)\\nmeetup_id:311318977	2025-10-22	20:00	\N	71	21	Location TBD		41.3851	2.1734	16	16	0.0	f	Cooking	\N
414	48H OPEN HOUSE BCN´25! VISITAS GRATIS! (2ª PARTE)	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/catalunya-friends/events/311427015/)\\nmeetup_id:311427015	2025-10-26	10:00	\N	101	21	Location TBD		41.3851	2.1734	30	12	0.0	f	Art	\N
415	Outdoor Bachata Social in Parc de la Ciutadella	FREE 100% Bachata social Saturday in Barcelona\nEvery week we meet at Parc de la Ciutadella (the stairs of the palace without plants) to enjoy music and movement together\nWe have our amazing DJ TRESOR (follow him on Instagram: @franck_kizz @ciudadella_with_dj_tresor_x_), who is always willing to provide us with the top music!\nOpen, cheerful environment for all levels!\nWe’d love you to bring more friends or family, also you can come alone cuz we have all the friendly people here:) Join us to have \\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/outdoor-bachata-social/events/311550700/)\\nmeetup_id:311550700	2025-10-17	17:00	\N	102	21	We are always on the side WITHOUT trees of the famous and beautiful Cascada Monumental!		41.3901658	2.1865593	0	2	0.0	f	General	https://secure-content.meetupstatic.com/images/classic-events/530749240/highres/
416	🤩❤️🍹ENCUENTRO ONLINE PARA CHATEAR TODOS LOS LUNES, MIÉRCOLES Y VIERNES.	Event from Meetup.com\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/amigos-singles-barcelona/events/311312657/)\\nmeetup_id:311312657	2025-10-20	22:00	\N	103	21	Location TBD		41.3851	2.1734	0	5	0.0	f	General	\N
417	¡La Caza de la Bruja!: El Kaos ha Llegado [JUEGO SOCIAL]	**[Grupo Whatsapp MODO SOCIAL](https://chat.whatsapp.com/JHQ0Yf00Fkh3PtTKC1fKzS)** En este evento, nada será lo que parece… Una misteriosa bruja con poderes especiales **se ha infiltrado** entre vosotros, y su objetivo es sembrar caos y descontrol a su antojo.\n\nMentiras, manipulaciones y travesuras se sucederán mientras ella juega con el grupo… ¿seréis capaces de **descubrir quién es** antes de que sea demasiado tarde?\n\nRisas aseguradas, tensión y emoción a partes iguales: pon a prueba tu ingeni\\n\\n---\\nFrom Meetup.com\\n[View on Meetup](https://www.meetup.com/modo-social/events/311517218/)\\nmeetup_id:311517218	2025-11-01	19:00	\N	98	21	Location TBD		41.3851	2.1734	0	4	0.0	f	Make New Friends	https://secure-content.meetupstatic.com/images/classic-events/530713764/highres/
\.


--
-- Data for Name: friendships; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.friendships (user_id, friend_id, created_at) FROM stdin;
22	21	2025-10-16 14:10:21.623331+00
21	22	2025-10-16 14:10:21.623331+00
\.


--
-- Data for Name: group_members; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.group_members (user_id, group_id) FROM stdin;
22	62
22	63
22	64
\.


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.groups (id, name, description, category, location, members_count, organizer_id, image, founded) FROM stdin;
65	🏳️‍🌈FR¡!NDR✌🏻 | International LGBTQ+ Community	Events from 🏳️‍🌈FR¡!NDR✌🏻 | International LGBTQ+ Community	Locals & New in Town		282	21	https://secure-content.meetupstatic.com/images/classic-events/530731338/highres/	2024-01-01 00:00:00+00
62	Barcelona Chess Meetup	Events from Barcelona Chess Meetup	General		2412	21	https://secure-content.meetupstatic.com/images/classic-events/491620901/highres/	2024-01-01 00:00:00+00
63	Barcelona Fun Activites  Meet people and Make friends	Events from Barcelona Fun Activites  Meet people and Make friends	International Friends		947	21	https://secure-content.meetupstatic.com/images/classic-events/517082540/highres/	2024-01-01 00:00:00+00
64	INTERNATIONAL MEETING MULTILANGUAGE BARCELONA	Events from INTERNATIONAL MEETING MULTILANGUAGE BARCELONA	International Friends		4832	21	https://secure-content.meetupstatic.com/images/classic-events/487154421/highres/	2024-01-01 00:00:00+00
99	Enjoy Catalonia (tours a Barcelona, excursions i viatges)	Events from Enjoy Catalonia (tours a Barcelona, excursions i viatges)	Arts & Culture		27342	21	https://source.unsplash.com/400x400/?group,people,community	2024-01-01 00:00:00+00
66	Friendly Vibes	Events from Friendly Vibes	General		2101	21	https://secure-content.meetupstatic.com/images/classic-events/528077174/highres/	2024-01-01 00:00:00+00
67	Barcelona English Speaking Meetup	Events from Barcelona English Speaking Meetup	General		3442	21	https://secure-content.meetupstatic.com/images/classic-events/514499290/highres/	2024-01-01 00:00:00+00
68	BCN Afterwork Friends & Fun	Events from BCN Afterwork Friends & Fun	General		6824	21	https://secure-content.meetupstatic.com/images/classic-events/526516944/highres/	2024-01-01 00:00:00+00
69	BARCELONA MEET 😃🎉😃	Events from BARCELONA MEET 😃🎉😃	General		0	21	https://secure-content.meetupstatic.com/images/classic-events/513058996/highres/	2024-01-01 00:00:00+00
70	Barcelona Social Media Creators & Influencer Meetups	Events from Barcelona Social Media Creators & Influencer Meetups	Digital Marketing		208	21	https://secure-content.meetupstatic.com/images/classic-events/504861068/highres/	2024-01-01 00:00:00+00
71	BCN Gastronomic Society	Events from BCN Gastronomic Society	Beer		0	21	https://secure-content.meetupstatic.com/images/classic-events/502571818/highres/	2024-01-01 00:00:00+00
72	Eventos Barcelona	Events from Eventos Barcelona	Coffee		0	21	https://secure-content.meetupstatic.com/images/classic-events/524287938/highres/	2024-01-01 00:00:00+00
73	Barcelona Language Exchange	Events from Barcelona Language Exchange	General		48220	21	https://secure-content.meetupstatic.com/images/classic-events/472813328/highres/	2024-01-01 00:00:00+00
74	Meet New Friends Every Week at Brunch Roulette	Events from Meet New Friends Every Week at Brunch Roulette	Coffee and Tea Socials		126	21	https://secure-content.meetupstatic.com/images/classic-events/527227952/highres/	2024-01-01 00:00:00+00
75	Barcelona Night Out Event (Student/Local/Tourista) ALL MIX	Events from Barcelona Night Out Event (Student/Local/Tourista) ALL MIX	Arts & Culture		884	21	https://secure-content.meetupstatic.com/images/classic-events/518385489/highres/	2024-01-01 00:00:00+00
76	NETWORKING BARCELONA con Connecting People	Events from NETWORKING BARCELONA con Connecting People	General		6	21	https://secure-content.meetupstatic.com/images/classic-events/530540516/highres/	2024-01-01 00:00:00+00
77	KCN Club de Networking	Events from KCN Club de Networking	Business & Professional		4823	21	https://secure-content.meetupstatic.com/images/classic-events/488788223/highres/	2024-01-01 00:00:00+00
78	Women’s Coffee Network	Events from Women’s Coffee Network	Coffee and Tea Socials		50	21	https://secure-content.meetupstatic.com/images/classic-events/530241814/highres/	2024-01-01 00:00:00+00
79	Meetup de InnoIT Consulting en Barcelona	Events from Meetup de InnoIT Consulting en Barcelona	Artificial Intelligence		5426	21	https://secure-content.meetupstatic.com/images/classic-events/515030835/highres/	2024-01-01 00:00:00+00
80	Python Barcelona Meetup	Events from Python Barcelona Meetup	Artificial Intelligence		5001	21	https://secure-content.meetupstatic.com/images/classic-events/530713081/highres/	2024-01-01 00:00:00+00
81	Barcelona CyberSec	Events from Barcelona CyberSec	Artificial Intelligence		93	21	https://secure-content.meetupstatic.com/images/classic-events/530439979/highres/	2024-01-01 00:00:00+00
82	Amazon Web Services Barcelona User Group	Events from Amazon Web Services Barcelona User Group	Amazon Web Services		3033	21	https://secure-content.meetupstatic.com/images/classic-events/524682702/highres/	2024-01-01 00:00:00+00
83	Grafana & Friends Barcelona	Events from Grafana & Friends Barcelona	Cloud Computing		566	21	https://secure-content.meetupstatic.com/images/classic-events/515060405/highres/	2024-01-01 00:00:00+00
84	TechFems	Events from TechFems	Data Analytics		904	21	https://secure-content.meetupstatic.com/images/classic-events/522379653/highres/	2024-01-01 00:00:00+00
85	Product & Design Tech Networking	Events from Product & Design Tech Networking	General		2072	21	https://secure-content.meetupstatic.com/images/classic-events/523702178/highres/	2024-01-01 00:00:00+00
86	Talented People by Talent-R "Where Great Minds Meet"	Events from Talented People by Talent-R "Where Great Minds Meet"	Professional Development		496	21	https://secure-content.meetupstatic.com/images/classic-events/527553050/highres/	2024-01-01 00:00:00+00
87	OWASP Barcelona Chapter	Events from OWASP Barcelona Chapter	Application Security		265	21	https://secure-content.meetupstatic.com/images/classic-events/528624236/highres/	2024-01-01 00:00:00+00
88	Nature Connect	Events from Nature Connect	General		14147	21	https://secure-content.meetupstatic.com/images/classic-events/504380410/highres/	2024-01-01 00:00:00+00
89	SHE LINKS	Events from SHE LINKS	General		1	21	https://secure-content.meetupstatic.com/images/classic-events/530401391/highres/	2024-01-01 00:00:00+00
90	Barcelona English Speakers	Events from Barcelona English Speakers	Make New Friends		2196	21	https://secure-content.meetupstatic.com/images/classic-events/523827102/highres/	2024-01-01 00:00:00+00
93	Cultura I Oci Barcelona	Events from Cultura I Oci Barcelona	Day Trips		8601	21	https://secure-content.meetupstatic.com/images/classic-events/526676414/highres/	2024-01-01 00:00:00+00
91	🔥ATP Beach Volley - Entrenos Multi Niveles - (Coach: Breno)	Events from 🔥ATP Beach Volley - Entrenos Multi Niveles - (Coach: Breno)	New In Town		2206	21	https://secure-content.meetupstatic.com/images/classic-events/523369122/highres/	2024-01-01 00:00:00+00
92	The Hikers · Barcelona 👣	Events from The Hikers · Barcelona 👣	Nature		15062	21	https://secure-content.meetupstatic.com/images/classic-events/529899987/highres/	2024-01-01 00:00:00+00
94	HIKING BCN 🥾⛰️	Events from HIKING BCN 🥾⛰️	Hiking		3980	21	https://secure-content.meetupstatic.com/images/classic-events/526129719/highres/	2024-01-01 00:00:00+00
95	LGTBIQ Friends in Barcelona	Events from LGTBIQ Friends in Barcelona	Friendships		890	21	https://secure-content.meetupstatic.com/images/classic-events/521875843/highres/	2024-01-01 00:00:00+00
97	Barcelona cosmopolitan Meetup	Events from Barcelona cosmopolitan Meetup	Communication Skills		11565	21	https://secure-content.meetupstatic.com/images/classic-events/475356840/highres/	2024-01-01 00:00:00+00
96	onbassbcn	Events from onbassbcn	Make New Friends		8482	21	https://secure-content.meetupstatic.com/images/classic-events/526443241/highres/	2024-01-01 00:00:00+00
98	Modo Social	Events from Modo Social	Make New Friends		365	21	https://secure-content.meetupstatic.com/images/classic-events/529207952/highres/	2024-01-01 00:00:00+00
100	GUAITA Nature ＆ Friends • Senderismo Barcelona	Events from GUAITA Nature ＆ Friends • Senderismo Barcelona	Nature		19908	21	https://secure-content.meetupstatic.com/images/classic-events/524124260/highres/	2024-01-01 00:00:00+00
101	CATALUNYA FRIENDS	Events from CATALUNYA FRIENDS	Art		0	21	https://secure-content.meetupstatic.com/images/classic-events/500525246/highres/	2024-01-01 00:00:00+00
103	SINGLES BARCELONA ❤️ DE 30 A 39 AÑOS +1000🕺🏻💃🏽🕺🏻.	Events from SINGLES BARCELONA ❤️ DE 30 A 39 AÑOS +1000🕺🏻💃🏽🕺🏻.	General		0	21	https://secure-content.meetupstatic.com/images/classic-events/524538663/highres/	2024-01-01 00:00:00+00
104	INTERNATIONAL TARDEO 27-44yo NEWCOM & RESID +7600 🕺🏻💃🏽	Events from INTERNATIONAL TARDEO 27-44yo NEWCOM & RESID +7600 🕺🏻💃🏽	General		7521	21	https://secure-content.meetupstatic.com/images/classic-events/528047082/highres/	2024-01-01 00:00:00+00
105	WeMeet 20s - 40s años (Barcelona)	Events from WeMeet 20s - 40s años (Barcelona)	Dining Out		3445	21	https://secure-content.meetupstatic.com/images/classic-events/526349208/highres/	2024-01-01 00:00:00+00
106	Speaking Social Barcelona	Events from Speaking Social Barcelona	Arts & Culture		6787	21	https://secure-content.meetupstatic.com/images/classic-events/519242171/highres/	2024-01-01 00:00:00+00
107	Solteras y solteros Barcelona	Events from Solteras y solteros Barcelona	Coffee		0	21	https://secure-content.meetupstatic.com/images/classic-events/525177912/highres/	2024-01-01 00:00:00+00
102	Outdoor Bachata Social in Parc de la Ciutadella	Events from Outdoor Bachata Social in Parc de la Ciutadella	General		2	21	https://source.unsplash.com/400x400/?group,people,community	2024-01-01 00:00:00+00
108	Data, Cloud and AI in Barcelona	<p>Hola!!</p>\n<p>To see all meetups in this group: <a href="https://www.meetup.com/pro/ibm-community/">https://www.meetup.com/pro/ibm-community/</a></p>This is an IBM sponsored Meetup group geared towards developers, data scientists, data engineers, and ALL Big Data, Cloud and AI enthusiasts. Our meetups provide an opportunity to work hands on with the solutions and tools in our Big Data portfolio and to interact and share knowledge with experts at IBM and in our extended community. \n<br>\n<p>Nue	Artificial Intelligence	Barcelona	3634	23	https://secure-content.meetupstatic.com/images/classic-events/454981147/highres/	2024-01-01 00:00:00+00
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.messages (id, conversation_id, sender_id, content, sent_at, is_read) FROM stdin;
1	1	22	hello	2025-10-16 14:10:25.411664+00	t
2	1	22	bro	2025-10-16 14:10:31.081328+00	t
3	1	21	yo	2025-10-16 16:39:55.952466+00	t
4	1	21	whats good	2025-10-16 16:40:00.649072+00	t
\.


--
-- Data for Name: saved_searches; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.saved_searches (id, user_id, name, keyword, location, category, is_online, price, created_at) FROM stdin;
\.


--
-- Data for Name: search_history; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.search_history (id, user_id, keyword, location, category, is_online, price, searched_at) FROM stdin;
\.


--
-- Data for Name: user_interests; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.user_interests (user_id, category_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: meetup_user
--

COPY public.users (id, email, password_hash, name, bio, location, avatar, member_since, is_active) FROM stdin;
23	aa@mail.ru	$2b$12$KwBPrCGucHmFLK31CwH5x.Z726tMuEGzrQYAgePPuSlHlBm5ukHIy	mi	hello	\N	\N	2025-10-16 16:38:11.421234+00	t
21	admin@meetup.app	$2b$12$e8fdi.kL0YIwXcaMX1eRiukjGITgbDIYwWlGEXSK4xcms9QsJbYCm	Admin	Admin user	Barcelona	\N	2024-01-01 00:00:00+00	t
22	M@mail.ru	$2b$12$yDGi34w/9vmYz42NlwECT.q6xRd2RnvDKFIFU/5f5YkvjU.kZpuTm	M	hello	Barcelona 	https://i.pravatar.cc/300?img=6	2025-10-16 14:01:03.21534+00	t
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.categories_id_seq', 12, true);


--
-- Name: conversations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.conversations_id_seq', 1, true);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.events_id_seq', 442, true);


--
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.groups_id_seq', 108, true);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.messages_id_seq', 4, true);


--
-- Name: saved_searches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.saved_searches_id_seq', 1, false);


--
-- Name: search_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.search_history_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: meetup_user
--

SELECT pg_catalog.setval('public.users_id_seq', 23, true);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (id);


--
-- Name: event_attendees event_attendees_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.event_attendees
    ADD CONSTRAINT event_attendees_pkey PRIMARY KEY (user_id, event_id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: friendships friendships_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_pkey PRIMARY KEY (user_id, friend_id);


--
-- Name: group_members group_members_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_pkey PRIMARY KEY (user_id, group_id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: saved_searches saved_searches_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.saved_searches
    ADD CONSTRAINT saved_searches_pkey PRIMARY KEY (id);


--
-- Name: search_history search_history_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.search_history
    ADD CONSTRAINT search_history_pkey PRIMARY KEY (id);


--
-- Name: user_interests user_interests_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.user_interests
    ADD CONSTRAINT user_interests_pkey PRIMARY KEY (user_id, category_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_categories_name; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE UNIQUE INDEX ix_categories_name ON public.categories USING btree (name);


--
-- Name: ix_categories_slug; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE UNIQUE INDEX ix_categories_slug ON public.categories USING btree (slug);


--
-- Name: ix_conversations_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_conversations_id ON public.conversations USING btree (id);


--
-- Name: ix_events_category; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_events_category ON public.events USING btree (category);


--
-- Name: ix_events_date; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_events_date ON public.events USING btree (date);


--
-- Name: ix_events_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_events_id ON public.events USING btree (id);


--
-- Name: ix_events_is_online; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_events_is_online ON public.events USING btree (is_online);


--
-- Name: ix_events_location_city; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_events_location_city ON public.events USING btree (location_city);


--
-- Name: ix_events_title; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_events_title ON public.events USING btree (title);


--
-- Name: ix_groups_category; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_groups_category ON public.groups USING btree (category);


--
-- Name: ix_groups_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_groups_id ON public.groups USING btree (id);


--
-- Name: ix_groups_name; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_groups_name ON public.groups USING btree (name);


--
-- Name: ix_messages_conversation_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_messages_conversation_id ON public.messages USING btree (conversation_id);


--
-- Name: ix_messages_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_messages_id ON public.messages USING btree (id);


--
-- Name: ix_messages_sent_at; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_messages_sent_at ON public.messages USING btree (sent_at);


--
-- Name: ix_saved_searches_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_saved_searches_id ON public.saved_searches USING btree (id);


--
-- Name: ix_search_history_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_search_history_id ON public.search_history USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: meetup_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: conversations conversations_participant1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_participant1_id_fkey FOREIGN KEY (participant1_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: conversations conversations_participant2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_participant2_id_fkey FOREIGN KEY (participant2_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: event_attendees event_attendees_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.event_attendees
    ADD CONSTRAINT event_attendees_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE;


--
-- Name: event_attendees event_attendees_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.event_attendees
    ADD CONSTRAINT event_attendees_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: events events_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id) ON DELETE CASCADE;


--
-- Name: events events_organizer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_organizer_id_fkey FOREIGN KEY (organizer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: friendships friendships_friend_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_friend_id_fkey FOREIGN KEY (friend_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: friendships friendships_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: group_members group_members_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id) ON DELETE CASCADE;


--
-- Name: group_members group_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: groups groups_organizer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_organizer_id_fkey FOREIGN KEY (organizer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversations(id) ON DELETE CASCADE;


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: saved_searches saved_searches_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.saved_searches
    ADD CONSTRAINT saved_searches_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: search_history search_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.search_history
    ADD CONSTRAINT search_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_interests user_interests_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.user_interests
    ADD CONSTRAINT user_interests_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- Name: user_interests user_interests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: meetup_user
--

ALTER TABLE ONLY public.user_interests
    ADD CONSTRAINT user_interests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict bncuI0YIA3799bibAwCy1zAr9JQKUW4SkhXXh8FoKTyYMj6Dwjczy4UW11u1g1D

