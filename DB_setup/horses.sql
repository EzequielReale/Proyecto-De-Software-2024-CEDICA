CREATE TABLE public.horses (
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL,
    birth_date date NOT NULL,
    gender character varying(16) NOT NULL,
    race character varying(32) NOT NULL,
    coat character varying(32) NOT NULL,
    donation boolean NOT NULL,
    entry_date date NOT NULL,
    assigned_location character varying(64) NOT NULL
);

-- INSERT INTO public.horses VALUES (1, 'Canelo', '2001-05-04', 'Macho', 'Criollo', 'Marrón', false, '2023-01-01', 'Sede principal');
-- INSERT INTO public.horses VALUES (2, 'Summer', '2012-06-10', 'Macho', 'Norteño', 'Gris plateado', true, '2024-03-12', 'Sede Winterfell');
