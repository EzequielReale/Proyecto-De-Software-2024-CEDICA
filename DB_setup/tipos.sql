CREATE TABLE public.tipos (
    id integer NOT NULL,
    tipo character varying(50) NOT NULL
);


CREATE SEQUENCE public.tipos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_id_seq OWNED BY public.tipos.id;
ALTER TABLE ONLY public.tipos ALTER COLUMN id SET DEFAULT nextval('public.tipos_id_seq'::regclass);


INSERT INTO public.tipos VALUES (1, 'Honorarios');
INSERT INTO public.tipos VALUES (2, 'Proveedor');
INSERT INTO public.tipos VALUES (3, 'Varios');


SELECT pg_catalog.setval('public.tipos_id_seq', 3, true);

ALTER TABLE ONLY public.tipos
    ADD CONSTRAINT tipos_pkey PRIMARY KEY (id);