CREATE TABLE public.permissions (
    id SERIAL PRIMARY KEY,
    name character varying(100),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

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
