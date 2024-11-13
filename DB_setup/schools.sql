DROP TABLE IF EXISTS public.schools;

CREATE TABLE IF NOT EXISTS public.schools
(
    id SERIAL NOT NULL,
    name character varying(64) COLLATE pg_catalog."default" NOT NULL,
    address character varying(128) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(16) COLLATE pg_catalog."default" NOT NULL,
    level school_levels NOT NULL,
    year integer NOT NULL,
    observations text COLLATE pg_catalog."default" NOT NULL,
    rider_id integer NOT NULL REFERENCES riders(id) ON DELETE CASCADE,
);

-- INSERT INTO schools (name, address, phone, level, year, observations, rider_id)
-- VALUES ('Escuela_0', 'Calle Falsa 120', '123456780', 'Primario', 5, 'Observaciones de la escuela 0', 1);
