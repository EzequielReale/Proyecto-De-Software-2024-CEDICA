CREATE TABLE public.roles (
    id SERIAL PRIMARY KEY,
    name character varying(100),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

INSERT INTO public.roles VALUES (1, 'Tecnica', '2024-10-14 02:24:18.438456', '2024-10-14 02:24:18.438458');
INSERT INTO public.roles VALUES (2, 'Encuestre', '2024-10-14 02:24:18.444587', '2024-10-14 02:24:18.444589');
INSERT INTO public.roles VALUES (3, 'Voluntariado', '2024-10-14 02:24:18.449356', '2024-10-14 02:24:18.449358');
INSERT INTO public.roles VALUES (4, 'Administracion', '2024-10-14 02:24:18.451751', '2024-10-14 02:24:18.451753');
INSERT INTO public.roles VALUES (5, 'SystemAdmin', '2024-10-14 02:24:18.458878', '2024-10-14 02:24:18.45888');
