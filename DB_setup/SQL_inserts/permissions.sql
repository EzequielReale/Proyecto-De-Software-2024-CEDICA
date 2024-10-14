CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying(100),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;
ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);

INSERT INTO public.permissions VALUES (1, 'user_index', '2024-10-14 02:24:15.463457', '2024-10-14 02:24:15.463461') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (2, 'user_new', '2024-10-14 02:24:15.466376', '2024-10-14 02:24:15.466378') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (3, 'user_destroy', '2024-10-14 02:24:15.470599', '2024-10-14 02:24:15.470601') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (4, 'user_update', '2024-10-14 02:24:15.472658', '2024-10-14 02:24:15.47266') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (5, 'user_show', '2024-10-14 02:24:15.474608', '2024-10-14 02:24:15.47461') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (6, 'team_index', '2024-10-14 02:24:18.407633', '2024-10-14 02:24:18.407634') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (7, 'team_new', '2024-10-14 02:24:18.409552', '2024-10-14 02:24:18.409554') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (8, 'team_destroy', '2024-10-14 02:24:18.411463', '2024-10-14 02:24:18.411464') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (9, 'team_update', '2024-10-14 02:24:18.413641', '2024-10-14 02:24:18.413643') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (10, 'team_show', '2024-10-14 02:24:18.415508', '2024-10-14 02:24:18.415509') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (11, 'reg_pagos_index', '2024-10-14 02:24:18.417587', '2024-10-14 02:24:18.417589') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (12, 'reg_pagos_new', '2024-10-14 02:24:18.419478', '2024-10-14 02:24:18.41948') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (13, 'reg_pagos_destroy', '2024-10-14 02:24:18.421468', '2024-10-14 02:24:18.42147') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (14, 'reg_pagos_update', '2024-10-14 02:24:18.423558', '2024-10-14 02:24:18.423567') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (15, 'reg_pagos_show', '2024-10-14 02:24:18.425694', '2024-10-14 02:24:18.425695') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (16, 'encuestre_index', '2024-10-14 02:24:18.427699', '2024-10-14 02:24:18.427701') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (17, 'encuestre_new', '2024-10-14 02:24:18.429712', '2024-10-14 02:24:18.429713') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (18, 'encuestre_destroy', '2024-10-14 02:24:18.431619', '2024-10-14 02:24:18.43162') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (19, 'encuestre_update', '2024-10-14 02:24:18.433693', '2024-10-14 02:24:18.433694') ON CONFLICT DO NOTHING;
INSERT INTO public.permissions VALUES (20, 'encuestre_show', '2024-10-14 02:24:18.435593', '2024-10-14 02:24:18.435594') ON CONFLICT DO NOTHING;

SELECT pg_catalog.setval('public.permissions_id_seq', 20, true);

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_name_key UNIQUE (name);

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);
