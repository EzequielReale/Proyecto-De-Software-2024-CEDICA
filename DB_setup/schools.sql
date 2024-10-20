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
    rider_id integer NOT NULL,
    CONSTRAINT schools_pkey PRIMARY KEY (id),
    CONSTRAINT schools_rider_id_fkey FOREIGN KEY (rider_id)
        REFERENCES public.riders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE IF EXISTS public.schools
    OWNER to grupo04;CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    address VARCHAR(128) NOT NULL,
    phone VARCHAR(16) NOT NULL,
    level school_levels NOT NULL,
    year INTEGER NOT NULL,
    observations TEXT NOT NULL,
    rider_id INTEGER NOT NULL REFERENCES riders(id)
);

-- INSERT INTO schools (name, address, phone, level, year, observations, rider_id)
-- VALUES ('Escuela_0', 'Calle Falsa 120', '123456780', 'Primario', 5, 'Observaciones de la escuela 0', 1);
