CREATE TABLE public.schools (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    address character varying(128) NOT NULL,
    phone character varying(16) NOT NULL,
    level public.school_levels NOT NULL,
    year integer NOT NULL,
    observations text NOT NULL,
    rider_id integer NOT NULL
);

CREATE SEQUENCE public.schools_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.schools_id_seq OWNED BY public.schools.id;
ALTER TABLE ONLY public.schools ALTER COLUMN id SET DEFAULT nextval('public.schools_id_seq'::regclass);

INSERT INTO public.schools VALUES (1, 'Escuela_0', 'Calle Falsa 120', '123456780', 'Primario', 5, 'Observaciones de la escuela 0', 3);
INSERT INTO public.schools VALUES (2, 'Escuela_1', 'Calle Falsa 121', '123456781', 'Primario', 5, 'Observaciones de la escuela 1', 5);
INSERT INTO public.schools VALUES (3, 'Escuela_2', 'Calle Falsa 122', '123456782', 'Primario', 5, 'Observaciones de la escuela 2', 7);
INSERT INTO public.schools VALUES (4, 'Escuela_3', 'Calle Falsa 123', '123456783', 'Primario', 5, 'Observaciones de la escuela 3', 9);
INSERT INTO public.schools VALUES (5, 'Escuela_4', 'Calle Falsa 124', '123456784', 'Primario', 5, 'Observaciones de la escuela 4', 11);
INSERT INTO public.schools VALUES (6, 'Escuela_5', 'Calle Falsa 125', '123456785', 'Primario', 5, 'Observaciones de la escuela 5', 13);
INSERT INTO public.schools VALUES (7, 'Escuela_6', 'Calle Falsa 126', '123456786', 'Primario', 5, 'Observaciones de la escuela 6', 15);
INSERT INTO public.schools VALUES (8, 'Escuela_7', 'Calle Falsa 127', '123456787', 'Primario', 5, 'Observaciones de la escuela 7', 17);
INSERT INTO public.schools VALUES (9, 'Escuela_8', 'Calle Falsa 128', '123456788', 'Primario', 5, 'Observaciones de la escuela 8', 19);
INSERT INTO public.schools VALUES (10, 'Escuela_9', 'Calle Falsa 129', '123456789', 'Primario', 5, 'Observaciones de la escuela 9', 21);
INSERT INTO public.schools VALUES (11, 'Escuela_10', 'Calle Falsa 1210', '1234567810', 'Primario', 5, 'Observaciones de la escuela 10', 23);
INSERT INTO public.schools VALUES (12, 'Escuela_11', 'Calle Falsa 1211', '1234567811', 'Primario', 5, 'Observaciones de la escuela 11', 25);
INSERT INTO public.schools VALUES (13, 'Escuela_12', 'Calle Falsa 1212', '1234567812', 'Primario', 5, 'Observaciones de la escuela 12', 27);
INSERT INTO public.schools VALUES (14, 'Escuela_13', 'Calle Falsa 1213', '1234567813', 'Primario', 5, 'Observaciones de la escuela 13', 29);
INSERT INTO public.schools VALUES (15, 'Escuela_14', 'Calle Falsa 1214', '1234567814', 'Primario', 5, 'Observaciones de la escuela 14', 31);
INSERT INTO public.schools VALUES (16, 'Escuela_15', 'Calle Falsa 1215', '1234567815', 'Primario', 5, 'Observaciones de la escuela 15', 33);
INSERT INTO public.schools VALUES (17, 'Escuela_16', 'Calle Falsa 1216', '1234567816', 'Primario', 5, 'Observaciones de la escuela 16', 35);
INSERT INTO public.schools VALUES (18, 'Escuela_17', 'Calle Falsa 1217', '1234567817', 'Primario', 5, 'Observaciones de la escuela 17', 37);
INSERT INTO public.schools VALUES (19, 'Escuela_18', 'Calle Falsa 1218', '1234567818', 'Primario', 5, 'Observaciones de la escuela 18', 39);
INSERT INTO public.schools VALUES (20, 'Escuela_19', 'Calle Falsa 1219', '1234567819', 'Primario', 5, 'Observaciones de la escuela 19', 41);
INSERT INTO public.schools VALUES (21, 'Escuela_20', 'Calle Falsa 1220', '1234567820', 'Primario', 5, 'Observaciones de la escuela 20', 43);
INSERT INTO public.schools VALUES (22, 'Escuela_21', 'Calle Falsa 1221', '1234567821', 'Primario', 5, 'Observaciones de la escuela 21', 45);
INSERT INTO public.schools VALUES (23, 'Escuela_22', 'Calle Falsa 1222', '1234567822', 'Primario', 5, 'Observaciones de la escuela 22', 47);
INSERT INTO public.schools VALUES (24, 'Escuela_23', 'Calle Falsa 1223', '1234567823', 'Primario', 5, 'Observaciones de la escuela 23', 49);
INSERT INTO public.schools VALUES (25, 'Escuela_24', 'Calle Falsa 1224', '1234567824', 'Primario', 5, 'Observaciones de la escuela 24', 51);
INSERT INTO public.schools VALUES (26, 'Escuela_25', 'Calle Falsa 1225', '1234567825', 'Primario', 5, 'Observaciones de la escuela 25', 53);
INSERT INTO public.schools VALUES (27, 'Escuela_26', 'Calle Falsa 1226', '1234567826', 'Primario', 5, 'Observaciones de la escuela 26', 55);
INSERT INTO public.schools VALUES (28, 'Escuela_27', 'Calle Falsa 1227', '1234567827', 'Primario', 5, 'Observaciones de la escuela 27', 57);
INSERT INTO public.schools VALUES (29, 'Escuela_28', 'Calle Falsa 1228', '1234567828', 'Primario', 5, 'Observaciones de la escuela 28', 59);
INSERT INTO public.schools VALUES (30, 'Escuela_29', 'Calle Falsa 1229', '1234567829', 'Primario', 5, 'Observaciones de la escuela 29', 61);

SELECT pg_catalog.setval('public.schools_id_seq', 30, true);

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT schools_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT schools_rider_id_fkey FOREIGN KEY (rider_id) REFERENCES public.riders(id);