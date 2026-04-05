--
-- PostgreSQL database dump
--

\restrict XBVDHmVGUfTWb0NjrqY2ee9YrYpw5CER3P4Bg8hG4lUYfQhlcXpRgcLII7TeMgq

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

-- Started on 2026-04-05 10:52:13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 228 (class 1259 OID 16448)
-- Name: carrito; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carrito (
    id_carrito integer NOT NULL,
    id_usuario integer NOT NULL,
    id_producto integer NOT NULL,
    cantidad integer DEFAULT 1 NOT NULL,
    CONSTRAINT carrito_cantidad_check CHECK ((cantidad > 0))
);


ALTER TABLE public.carrito OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16447)
-- Name: carrito_id_carrito_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.carrito_id_carrito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.carrito_id_carrito_seq OWNER TO postgres;

--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 227
-- Name: carrito_id_carrito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.carrito_id_carrito_seq OWNED BY public.carrito.id_carrito;


--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: categorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.categorias OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categorias_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categorias_id_categoria_seq OWNER TO postgres;

--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 219
-- Name: categorias_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categorias_id_categoria_seq OWNED BY public.categorias.id_categoria;


--
-- TOC entry 232 (class 1259 OID 16489)
-- Name: detalle_venta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detalle_venta (
    id_detalle integer NOT NULL,
    id_venta integer NOT NULL,
    id_producto integer NOT NULL,
    cantidad integer NOT NULL,
    precio_unitario numeric(12,2) NOT NULL,
    CONSTRAINT detalle_venta_cantidad_check CHECK ((cantidad > 0))
);


ALTER TABLE public.detalle_venta OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16488)
-- Name: detalle_venta_id_detalle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.detalle_venta_id_detalle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detalle_venta_id_detalle_seq OWNER TO postgres;

--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 231
-- Name: detalle_venta_id_detalle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.detalle_venta_id_detalle_seq OWNED BY public.detalle_venta.id_detalle;


--
-- TOC entry 234 (class 1259 OID 16512)
-- Name: pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pago (
    id_pago integer NOT NULL,
    id_venta integer NOT NULL,
    metodo_pago character varying(50),
    estado_pago character varying(50),
    fecha_pago timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.pago OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16511)
-- Name: pago_id_pago_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pago_id_pago_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pago_id_pago_seq OWNER TO postgres;

--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 233
-- Name: pago_id_pago_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pago_id_pago_seq OWNED BY public.pago.id_pago;


--
-- TOC entry 224 (class 1259 OID 16413)
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    id_producto integer NOT NULL,
    nombre character varying(150) NOT NULL,
    descripcion text,
    precio numeric(12,2) NOT NULL,
    stock integer DEFAULT 0 NOT NULL,
    imagen_url text,
    id_categoria integer,
    id_vendedor integer,
    activo boolean DEFAULT true,
    CONSTRAINT productos_precio_check CHECK ((precio >= (0)::numeric))
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16412)
-- Name: productos_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.productos_id_producto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.productos_id_producto_seq OWNER TO postgres;

--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 223
-- Name: productos_id_producto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.productos_id_producto_seq OWNED BY public.productos.id_producto;


--
-- TOC entry 226 (class 1259 OID 16433)
-- Name: sesiones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesiones (
    id_sesion integer NOT NULL,
    id_usuario integer NOT NULL,
    fecha_login timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.sesiones OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16432)
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesiones_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sesiones_id_sesion_seq OWNER TO postgres;

--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 225
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesiones_id_sesion_seq OWNED BY public.sesiones.id_sesion;


--
-- TOC entry 222 (class 1259 OID 16399)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    rol character varying(20) DEFAULT 'cliente'::character varying,
    nombre character varying(100),
    CONSTRAINT usuarios_rol_check CHECK (((rol)::text = ANY ((ARRAY['admin'::character varying, 'cliente'::character varying, 'vendedor'::character varying])::text[])))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16398)
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- TOC entry 230 (class 1259 OID 16471)
-- Name: ventas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ventas (
    id_venta integer NOT NULL,
    id_usuario integer NOT NULL,
    fecha timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    total_pago numeric(12,2) DEFAULT 0 NOT NULL,
    estado_envio character varying(50) DEFAULT 'pendiente'::character varying
);


ALTER TABLE public.ventas OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16470)
-- Name: ventas_id_venta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ventas_id_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ventas_id_venta_seq OWNER TO postgres;

--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 229
-- Name: ventas_id_venta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ventas_id_venta_seq OWNED BY public.ventas.id_venta;


--
-- TOC entry 4852 (class 2604 OID 16451)
-- Name: carrito id_carrito; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carrito ALTER COLUMN id_carrito SET DEFAULT nextval('public.carrito_id_carrito_seq'::regclass);


--
-- TOC entry 4844 (class 2604 OID 16393)
-- Name: categorias id_categoria; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias ALTER COLUMN id_categoria SET DEFAULT nextval('public.categorias_id_categoria_seq'::regclass);


--
-- TOC entry 4858 (class 2604 OID 16492)
-- Name: detalle_venta id_detalle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_venta ALTER COLUMN id_detalle SET DEFAULT nextval('public.detalle_venta_id_detalle_seq'::regclass);


--
-- TOC entry 4859 (class 2604 OID 16515)
-- Name: pago id_pago; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago ALTER COLUMN id_pago SET DEFAULT nextval('public.pago_id_pago_seq'::regclass);


--
-- TOC entry 4847 (class 2604 OID 16416)
-- Name: productos id_producto; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos ALTER COLUMN id_producto SET DEFAULT nextval('public.productos_id_producto_seq'::regclass);


--
-- TOC entry 4850 (class 2604 OID 16436)
-- Name: sesiones id_sesion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones ALTER COLUMN id_sesion SET DEFAULT nextval('public.sesiones_id_sesion_seq'::regclass);


--
-- TOC entry 4845 (class 2604 OID 16402)
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- TOC entry 4854 (class 2604 OID 16474)
-- Name: ventas id_venta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas ALTER COLUMN id_venta SET DEFAULT nextval('public.ventas_id_venta_seq'::regclass);


--
-- TOC entry 5050 (class 0 OID 16448)
-- Dependencies: 228
-- Data for Name: carrito; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carrito (id_carrito, id_usuario, id_producto, cantidad) FROM stdin;
9	4	2	1
\.


--
-- TOC entry 5042 (class 0 OID 16390)
-- Dependencies: 220
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categorias (id_categoria, nombre) FROM stdin;
1	Laptops
2	Bolsos
3	Mujer
4	Hombre
5	Accesorios
\.


--
-- TOC entry 5054 (class 0 OID 16489)
-- Dependencies: 232
-- Data for Name: detalle_venta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detalle_venta (id_detalle, id_venta, id_producto, cantidad, precio_unitario) FROM stdin;
1	1	3	3	850.00
2	1	2	1	750.00
3	2	3	13	850.00
4	3	2	1	750.00
5	3	3	2	850.00
6	4	2	1	750.00
7	4	3	4	850.00
8	5	3	1	850.00
9	6	3	1	850.00
10	7	3	1	850.00
11	8	3	2	850.00
12	9	3	1	850.00
13	10	4	1	300.00
14	11	5	1	550.00
15	12	6	1	700.00
16	13	6	1	700.00
17	13	5	1	550.00
18	14	2	1	750.00
19	15	8	1	700.00
20	16	11	1	700.00
21	17	2	2	750.00
22	17	3	3	850.00
23	17	12	1	7000.00
24	18	12	1	7000.00
25	19	12	27	7000.00
26	20	12	2	7000.00
27	21	12	1	7000.00
28	22	12	1	7000.00
\.


--
-- TOC entry 5056 (class 0 OID 16512)
-- Dependencies: 234
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pago (id_pago, id_venta, metodo_pago, estado_pago, fecha_pago) FROM stdin;
\.


--
-- TOC entry 5046 (class 0 OID 16413)
-- Dependencies: 224
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (id_producto, nombre, descripcion, precio, stock, imagen_url, id_categoria, id_vendedor, activo) FROM stdin;
5	Tennis Nike Premier	sdasadsa	550.00	1	https://m.media-amazon.com/images/I/71oG884tDJL._AC_SX575_.jpg	1	5	f
6	Tennis Pirma 	sdsadasdasdddddddddddddddd	700.00	1	https://m.media-amazon.com/images/I/61Vhw88vVGL._AC_SX575_.jpg	1	5	f
4	gorra	None	400.00	6	https://m.media-amazon.com/images/I/51DZ5PAO7pL._AC_SX679_.jpg	1	5	f
7	Tennis Nike	Tennis para correr	700.00	1		1	7	f
3	Laptop Lenovo IdeaPad 1	Laptop con procesador Intel Core i7, 8GB RAM y 512GB SSD	850.00	15	https://mi-tienda.com/imagenes/lenovo-ideapad3.jpg	1	\N	f
2	Laptop Lenovo IdeaPad 3	Laptop con procesador Intel Core i5, 8GB RAM y 512GB SSD	750.00	15	https://unsplash.com/es/fotos/dos-hombres-con-traje-paseando-juntos-al-aire-libre-aBm0Zvp1S2c	1	\N	f
10	Tennis Nike Premier	dasdasda	700.00	1	https://m.media-amazon.com/images/I/711EGIS6SZL._AC_SX575_.jpg	4	7	f
8	Tennis Nike	tennis futbol	700.00	1	https://m.media-amazon.com/images/I/61aVQ6oYU-L._AC_SY575_.jpg	1	7	f
9	Tennis Nike Premier	tennnis para hombre numero 7 	700.00	1	https://m.media-amazon.com/images/I/711EGIS6SZL._AC_SX575_.jpg	1	7	f
11	Tennis Nike Premier	jnjjjjj	700.00	1	https://m.media-amazon.com/images/I/711EGIS6SZL._AC_SX575_.jpg	4	7	f
12	Teenis	Tennis nike originales\r\n	7000.00	1	https://m.media-amazon.com/images/I/71jAr2M6RwL._AC_SY575_.jpg	3	2	t
13	Teenis	dsdfsfsfs	700.00	1	https://m.media-amazon.com/images/I/71jAr2M6RwL._AC_SY575_.jpg	4	9	f
14	Teenis	safsdfs	5.00	1		3	9	f
15	tenis negros nike	tenis	500.00	1	https://m.media-amazon.com/images/I/71jAr2M6RwL._AC_SY575_.jpg	2	13	t
16	bolso	jjhjkhjkhjkh	500.00	1	https://m.media-amazon.com/images/I/71jAr2M6RwL._AC_SY575_.jpg	2	13	f
\.


--
-- TOC entry 5048 (class 0 OID 16433)
-- Dependencies: 226
-- Data for Name: sesiones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sesiones (id_sesion, id_usuario, fecha_login) FROM stdin;
\.


--
-- TOC entry 5044 (class 0 OID 16399)
-- Dependencies: 222
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id_usuario, email, password, rol, nombre) FROM stdin;
1	marcuzfinixloapez@gmail.com	pbkdf2:sha256:1000000$BCT4yMrh1OWg6Owt$c42e044c02a5e3d583caf5b4ef582f29f67603087471eaeaab4fd87bcfecb5d5	cliente	marco
3	marcuzfinixlopez@gmail.coms	pbkdf2:sha256:1000000$6KrZd6TQHAysRGVa$abf53a644faba54914129bc4894240e7073ad9b2c4384914230edbc7e98b0fba	cliente	Beatriz Arely
4	lola_marvelo@hotmail.com	pbkdf2:sha256:1000000$fasjC6740pi2uZkf$4dbeb317a3ce16dbdef2eb90def70f83a1885ee5794d94ea97285713b6eccc6a	cliente	marco
5	gabo123@gmail.com	pbkdf2:sha256:1000000$xRRgsOHkfIqdZSbp$502b02c95fd68bddcced3d6ffbad6e1508d8fa2e0d8cac222059e310f698e676	vendedor	gabriel najera esparza 
6	marco123@gmail.com	pbkdf2:sha256:1000000$aUslsWtyOqTZqmLS$333badb8ec54040111319a0bd8345c64a80f6f77db742af6de33ba6b0ad7bf40	cliente	marco
7	marcuzfinixlopes@gmail.com	pbkdf2:sha256:1000000$aReumX21fHLhS2IO$0216aa6f29cf879e9c3afa3d89e908478a4f5012303508b1cc099de5fb054c53	vendedor	marco
8	marcuzfinixlopess@gmail.com	pbkdf2:sha256:1000000$MaPkDxEav4byTl4A$50df47676c4206a311026953254563713bbc554d7138e5ebb44eacb9186f76fc	cliente	MARCOss
2	marcuzfinixlopez@gmail.com	pbkdf2:sha256:1000000$DJlSZxCtAdMp9h1H$c26fabc7f84270d68da7b648c474d77d1ac37fb90a1051ae1267ab3155cd2477	vendedor	Beatriz Arely
9	ricardo@gmail.com	pbkdf2:sha256:1000000$m8dIWsDD77CmhXpS$0fe15feb25d88d89b15771f39dd8fd78facb97ec213dc52a684787f7c20cfe88	vendedor	Ricardo
10	juan.atleta@fffactory.com	pbkdf2:sha256:1000000$GgOoMe4GJK0bWwdw$70597a1201e336ca91cd8f226381998835ac0c871fbcb502dc786505c54c60ca	cliente	Juan Perez
11	juan.atleta@ffactory.com	pbkdf2:sha256:1000000$ZvBQOXQMbxASNM3u$35dfcbbb0ddbec61fc467415d15fe0f3b8fd35ae8d893e6394bb072ea1eab8a0	cliente	Juan Perez
12	ricardocom@dasdas.com	pbkdf2:sha256:1000000$ngQFm6yGolHxjGRO$6db6b82b6e71612b3b72fef39715ec4b9d59f2416872ea248ea20623f1bf00e3	cliente	marco
13	ricardo2@gmail.com	pbkdf2:sha256:1000000$k4sv9KDU4vZpMT8s$ffb0126510a673e5c2edc0d048a450d8eb953007f9b5b96bfec442774b371ba2	vendedor	ricardo2
\.


--
-- TOC entry 5052 (class 0 OID 16471)
-- Dependencies: 230
-- Data for Name: ventas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ventas (id_venta, id_usuario, fecha, total_pago, estado_envio) FROM stdin;
1	4	2026-02-16 00:54:59.19955-06	3300.00	pendiente
2	5	2026-02-17 15:39:36.062254-06	11050.00	pendiente
3	5	2026-02-17 15:55:34.827325-06	2450.00	pendiente
4	5	2026-02-17 16:01:56.090432-06	4150.00	pendiente
5	5	2026-02-17 16:03:45.449793-06	850.00	pendiente
6	5	2026-02-19 11:47:55.411055-06	850.00	pendiente
7	2	2026-02-21 12:49:32.818574-06	850.00	pendiente
8	2	2026-02-21 13:36:58.042994-06	1700.00	pendiente
9	5	2026-02-21 14:23:06.562513-06	850.00	pendiente
10	5	2026-02-21 14:53:21.73591-06	300.00	pendiente
11	6	2026-02-21 15:17:47.956497-06	550.00	pendiente
12	5	2026-02-21 15:29:39.13237-06	700.00	pendiente
13	5	2026-02-24 17:14:26.457159-06	1250.00	pendiente
14	7	2026-03-03 15:11:50.305297-06	750.00	pendiente
15	7	2026-03-03 15:16:12.110912-06	700.00	pendiente
16	7	2026-03-06 08:35:53.286965-06	700.00	pendiente
17	2	2026-03-06 14:28:31.145756-06	11050.00	pendiente
18	2	2026-03-09 17:24:51.01902-06	7000.00	pendiente
19	9	2026-03-09 17:28:18.794766-06	189000.00	pendiente
20	9	2026-03-09 18:36:16.827579-06	14000.00	pendiente
21	13	2026-03-26 19:06:22.081818-06	7000.00	pendiente
22	13	2026-03-29 00:34:45.476724-06	7000.00	pendiente
\.


--
-- TOC entry 5070 (class 0 OID 0)
-- Dependencies: 227
-- Name: carrito_id_carrito_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.carrito_id_carrito_seq', 36, true);


--
-- TOC entry 5071 (class 0 OID 0)
-- Dependencies: 219
-- Name: categorias_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categorias_id_categoria_seq', 5, true);


--
-- TOC entry 5072 (class 0 OID 0)
-- Dependencies: 231
-- Name: detalle_venta_id_detalle_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.detalle_venta_id_detalle_seq', 28, true);


--
-- TOC entry 5073 (class 0 OID 0)
-- Dependencies: 233
-- Name: pago_id_pago_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pago_id_pago_seq', 1, false);


--
-- TOC entry 5074 (class 0 OID 0)
-- Dependencies: 223
-- Name: productos_id_producto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_id_producto_seq', 16, true);


--
-- TOC entry 5075 (class 0 OID 0)
-- Dependencies: 225
-- Name: sesiones_id_sesion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesiones_id_sesion_seq', 1, false);


--
-- TOC entry 5076 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 13, true);


--
-- TOC entry 5077 (class 0 OID 0)
-- Dependencies: 229
-- Name: ventas_id_venta_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ventas_id_venta_seq', 22, true);


--
-- TOC entry 4876 (class 2606 OID 16459)
-- Name: carrito carrito_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_pkey PRIMARY KEY (id_carrito);


--
-- TOC entry 4866 (class 2606 OID 16397)
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);


--
-- TOC entry 4880 (class 2606 OID 16500)
-- Name: detalle_venta detalle_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_pkey PRIMARY KEY (id_detalle);


--
-- TOC entry 4882 (class 2606 OID 16522)
-- Name: pago pago_id_venta_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_id_venta_key UNIQUE (id_venta);


--
-- TOC entry 4884 (class 2606 OID 16520)
-- Name: pago pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id_pago);


--
-- TOC entry 4872 (class 2606 OID 16426)
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id_producto);


--
-- TOC entry 4874 (class 2606 OID 16441)
-- Name: sesiones sesiones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones
    ADD CONSTRAINT sesiones_pkey PRIMARY KEY (id_sesion);


--
-- TOC entry 4868 (class 2606 OID 16411)
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- TOC entry 4870 (class 2606 OID 16409)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4878 (class 2606 OID 16482)
-- Name: ventas ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (id_venta);


--
-- TOC entry 4885 (class 2606 OID 16427)
-- Name: productos fk_categoria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT fk_categoria FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria) ON DELETE SET NULL;


--
-- TOC entry 4888 (class 2606 OID 16465)
-- Name: carrito fk_producto_carrito; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT fk_producto_carrito FOREIGN KEY (id_producto) REFERENCES public.productos(id_producto) ON DELETE CASCADE;


--
-- TOC entry 4891 (class 2606 OID 16506)
-- Name: detalle_venta fk_producto_detalle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT fk_producto_detalle FOREIGN KEY (id_producto) REFERENCES public.productos(id_producto);


--
-- TOC entry 4889 (class 2606 OID 16460)
-- Name: carrito fk_usuario_carrito; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT fk_usuario_carrito FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- TOC entry 4887 (class 2606 OID 16442)
-- Name: sesiones fk_usuario_sesion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesiones
    ADD CONSTRAINT fk_usuario_sesion FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- TOC entry 4890 (class 2606 OID 16483)
-- Name: ventas fk_usuario_venta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT fk_usuario_venta FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- TOC entry 4886 (class 2606 OID 16528)
-- Name: productos fk_vendedor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT fk_vendedor FOREIGN KEY (id_vendedor) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- TOC entry 4892 (class 2606 OID 16501)
-- Name: detalle_venta fk_venta_detalle; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT fk_venta_detalle FOREIGN KEY (id_venta) REFERENCES public.ventas(id_venta) ON DELETE CASCADE;


--
-- TOC entry 4893 (class 2606 OID 16523)
-- Name: pago fk_venta_pago; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT fk_venta_pago FOREIGN KEY (id_venta) REFERENCES public.ventas(id_venta) ON DELETE CASCADE;


-- Completed on 2026-04-05 10:52:13

--
-- PostgreSQL database dump complete
--

\unrestrict XBVDHmVGUfTWb0NjrqY2ee9YrYpw5CER3P4Bg8hG4lUYfQhlcXpRgcLII7TeMgq

