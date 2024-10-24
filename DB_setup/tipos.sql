CREATE TABLE public.tipos (
    id SERIAL PRIMARY KEY,
    tipo character varying(50) NOT NULL
);

INSERT INTO public.tipos VALUES (1, 'Honorarios');
INSERT INTO public.tipos VALUES (2, 'Proveedor');
INSERT INTO public.tipos VALUES (3, 'Varios');
