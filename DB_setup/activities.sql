CREATE TABLE public.activities (
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL
);

INSERT INTO public.activities VALUES (1, 'Hipoterapia');
INSERT INTO public.activities VALUES (2, 'Monta Terapéutica');
INSERT INTO public.activities VALUES (3, 'Deporte Ecuestre Adaptado');
INSERT INTO public.activities VALUES (4, 'Actividades Recreativas');
INSERT INTO public.activities VALUES (5, 'Equitación');
