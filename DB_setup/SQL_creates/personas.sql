-- DROP TABLE IF EXISTS persons;

CREATE TABLE IF NOT EXISTS persons
(
    id integer NOT NULL DEFAULT nextval('persons_id_seq'::regclass),
    name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    dni character varying(16) NOT NULL,
    phone character varying(32) NOT NULL,
    emergency_phone character varying(32) NOT NULL,
    street character varying(128) NOT NULL,
    "number" character varying(8) NOT NULL,
    locality_id integer NOT NULL,
    type character varying(16),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT persons_pkey PRIMARY KEY (id),
    CONSTRAINT persons_locality_id_fkey FOREIGN KEY (locality_id)
        REFERENCES public.localities (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- Definir el tipo ENUM para condition
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'condition_types') THEN
        CREATE TYPE condition_types AS ENUM ('Voluntario', 'Personal Rentado');
    END IF;
END $$;

-- DROP TABLE IF EXISTS members;

CREATE TABLE IF NOT EXISTS members
(
    id SERIAL PRIMARY KEY,
    email character varying(64) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    health_insurance character varying(32) NOT NULL,
    health_insurance_number character varying(32) NOT NULL,
    condition condition_types NOT NULL,
    active boolean DEFAULT TRUE,
    profession_id integer,
    job_id integer NOT NULL,
    CONSTRAINT members_id_fkey FOREIGN KEY (id)
        REFERENCES public.persons (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT members_job_id_fkey FOREIGN KEY (job_id)
        REFERENCES public.jobs (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT members_profession_id_fkey FOREIGN KEY (profession_id)
        REFERENCES public.professions (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
