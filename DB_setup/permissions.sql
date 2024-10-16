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

INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_index', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_new', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_destroy', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_update', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_show', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_block', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('user_update_password', NOW(), NOW()) ON CONFLICT DO NOTHING;

INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('team_index', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('team_new', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('team_destroy', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('team_update', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('team_show', NOW(), NOW()) ON CONFLICT DO NOTHING;

INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_pagos_index', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_pagos_new', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_pagos_destroy', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_pagos_update', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_pagos_show', NOW(), NOW()) ON CONFLICT DO NOTHING;

INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('encuestre_index', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('encuestre_new', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('encuestre_destroy', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('encuestre_update', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('encuestre_show', NOW(), NOW()) ON CONFLICT DO NOTHING;

INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('jya_index', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('jya_new', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('jya_destroy', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('jya_update', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('jya_show', NOW(), NOW()) ON CONFLICT DO NOTHING;

INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_cobros_index', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_cobros_new', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_cobros_destroy', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_cobros_update', NOW(), NOW()) ON CONFLICT DO NOTHING;
INSERT INTO public.permissions (name, created_at, updated_at) VALUES ('reg_cobros_show', NOW(), NOW()) ON CONFLICT DO NOTHING;

SELECT pg_catalog.setval('public.permissions_id_seq', 20, true);

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_name_key UNIQUE (name);

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);
