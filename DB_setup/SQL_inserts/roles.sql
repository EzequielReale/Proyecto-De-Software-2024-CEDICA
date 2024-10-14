CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(100),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;
ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);

INSERT INTO public.roles VALUES (1, 'Tecnica', '2024-10-14 02:24:18.438456', '2024-10-14 02:24:18.438458');
INSERT INTO public.roles VALUES (2, 'Encuestre', '2024-10-14 02:24:18.444587', '2024-10-14 02:24:18.444589');
INSERT INTO public.roles VALUES (3, 'Voluntariado', '2024-10-14 02:24:18.449356', '2024-10-14 02:24:18.449358');
INSERT INTO public.roles VALUES (4, 'Administracion', '2024-10-14 02:24:18.451751', '2024-10-14 02:24:18.451753');
INSERT INTO public.roles VALUES (5, 'SystemAdmin', '2024-10-14 02:24:18.458878', '2024-10-14 02:24:18.45888');


SELECT pg_catalog.setval('public.roles_id_seq', 5, true);

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
