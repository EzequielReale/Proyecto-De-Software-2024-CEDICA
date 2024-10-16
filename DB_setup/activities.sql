CREATE TABLE public.activities (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;
ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);

INSERT INTO public.activities VALUES (1, 'Hipoterapia');
INSERT INTO public.activities VALUES (2, 'Monta Terapéutica');
INSERT INTO public.activities VALUES (3, 'Deporte Ecuestre Adaptado');
INSERT INTO public.activities VALUES (4, 'Actividades Recreativas');
INSERT INTO public.activities VALUES (5, 'Equitación');


SELECT pg_catalog.setval('public.activities_id_seq', 5, true);

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);