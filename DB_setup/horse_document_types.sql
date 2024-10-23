CREATE TABLE public.horse_document_types (
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL
);

INSERT INTO public.horse_document_types VALUES (1, 'Ficha general');
INSERT INTO public.horse_document_types VALUES (2, 'Planificación de Entrenamiento');
INSERT INTO public.horse_document_types VALUES (3, 'Informe de Evolución');
INSERT INTO public.horse_document_types VALUES (4, 'Imágenes');
INSERT INTO public.horse_document_types VALUES (5, 'Registro veterinario');
