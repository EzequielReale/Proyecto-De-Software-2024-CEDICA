CREATE TABLE public.horse_document_types (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);

CREATE SEQUENCE public.horse_document_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horse_document_types_id_seq OWNED BY public.horse_document_types.id;
ALTER TABLE ONLY public.horse_document_types ALTER COLUMN id SET DEFAULT nextval('public.horse_document_types_id_seq'::regclass);

INSERT INTO public.horse_document_types VALUES (1, 'Ficha general');
INSERT INTO public.horse_document_types VALUES (2, 'Planificación de Entrenamiento');
INSERT INTO public.horse_document_types VALUES (3, 'Informe de Evolución');
INSERT INTO public.horse_document_types VALUES (4, 'Imágenes');
INSERT INTO public.horse_document_types VALUES (5, 'Registro veterinario');

SELECT pg_catalog.setval('public.horse_document_types_id_seq', 5, true);

ALTER TABLE ONLY public.horse_document_types
    ADD CONSTRAINT horse_document_types_name_key UNIQUE (name);

ALTER TABLE ONLY public.horse_document_types
    ADD CONSTRAINT horse_document_types_pkey PRIMARY KEY (id);