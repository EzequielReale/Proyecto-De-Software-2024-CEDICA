CREATE TABLE public.jobs (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);

CREATE SEQUENCE public.jobs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.jobs_id_seq OWNED BY public.jobs.id;
ALTER TABLE ONLY public.jobs ALTER COLUMN id SET DEFAULT nextval('public.jobs_id_seq'::regclass);


INSERT INTO public.jobs VALUES (1, 'Docente de capacitación', 'Enseñanza para nuevos miembros');
INSERT INTO public.jobs VALUES (2, 'Administrativo/a', 'Gestiona tareas administrativas en oficinas, asegurando la eficiencia operativa diaria.');
INSERT INTO public.jobs VALUES (3, 'Terapeuta', 'Facilita procesos de sanación y desarrollo personal mediante técnicas terapéuticas.');
INSERT INTO public.jobs VALUES (4, 'Conductor', 'Maneja caballos garantizando la seguridad y comodidad de pasajeros.');
INSERT INTO public.jobs VALUES (5, 'Auxiliar de pista', 'Asiste en la gestión y cuidado de caballos en pistas de equitación, garantizando seguridad.');
INSERT INTO public.jobs VALUES (6, 'Herrero', 'Artesano que forja metales, creando herramientas y piezas personalizadas a medida.');
INSERT INTO public.jobs VALUES (7, 'Veterinario', 'Diagnostica y trata enfermedades en animales, ofreciendo cuidados preventivos y educativos.');
INSERT INTO public.jobs VALUES (8, 'Entrenador de Caballos', 'Forma y entrena caballos para competencias o trabajo, desarrollando habilidades específicas.');
INSERT INTO public.jobs VALUES (9, 'Domador', 'Adiestra caballos para establecer confianza y control entre el animal y el jinete.');
INSERT INTO public.jobs VALUES (10, 'Profesor de Equitación', 'Enseña técnicas de monta y manejo de caballos, promoviendo seguridad en la práctica.');
INSERT INTO public.jobs VALUES (11, 'Docente de Capacitación', 'Forma a adultos en conocimientos y habilidades para mejorar su desempeño laboral.');
INSERT INTO public.jobs VALUES (12, 'Auxiliar de mantenimiento', 'Realiza mantenimiento preventivo y correctivo en instalaciones para asegurar su óptimo funcionamiento.');
INSERT INTO public.jobs VALUES (13, 'Otro', 'Otros trabajos variados no mencionados que abarcan diversas funciones y responsabilidades.');

SELECT pg_catalog.setval('public.jobs_id_seq', 13, true);

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);
