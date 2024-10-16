CREATE TABLE public.professions (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);

CREATE SEQUENCE public.professions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.professions_id_seq OWNED BY public.professions.id;

ALTER TABLE ONLY public.professions ALTER COLUMN id SET DEFAULT nextval('public.professions_id_seq'::regclass);


INSERT INTO public.professions VALUES (1, 'Docente', 'Enseñanza');
INSERT INTO public.professions VALUES (2, 'Psicólogo/a', 'Especialista en salud mental que evalúa y trata trastornos emocionales para el bienestar del paciente.');
INSERT INTO public.professions VALUES (3, 'Psicomotricista', 'Promueve el desarrollo motriz y la coordinación a través de actividades físicas y lúdicas.');
INSERT INTO public.professions VALUES (4, 'Médico/a', 'Profesional de la salud que diagnostica y trata enfermedades, enfocándose en la prevención y el cuidado integral.');
INSERT INTO public.professions VALUES (5, 'Kinesiólogo/a', 'Utiliza técnicas de movimiento para mejorar la movilidad y función física en rehabilitación.');
INSERT INTO public.professions VALUES (6, 'Terapista Ocupacional', 'Ayuda a mantener habilidades para la vida diaria, enfocándose en ocupaciones significativas.');
INSERT INTO public.professions VALUES (7, 'Psicopedagogo/a', 'Educador que aborda dificultades educativas y promueve el desarrollo integral del estudiante.');
INSERT INTO public.professions VALUES (8, 'Docente', 'Facilita el aprendizaje y desarrollo de habilidades en estudiantes mediante diversas metodologías.');
INSERT INTO public.professions VALUES (9, 'Profesor', 'Enseña materias específicas, promoviendo conocimientos y habilidades a través de estrategias efectivas.');
INSERT INTO public.professions VALUES (10, 'Fonoaudiólogo/a', 'Diagnostica y trata trastornos de comunicación y lenguaje, mejorando la deglución y la voz.');
INSERT INTO public.professions VALUES (11, 'Veterinario/a', 'Cuidado y tratamiento de enfermedades en animales, promoviendo su bienestar y prevención.');
INSERT INTO public.professions VALUES (12, 'Otro', 'Otras profesiones diversas no mencionadas en diferentes áreas y especialidades.');


SELECT pg_catalog.setval('public.professions_id_seq', 12, true);

ALTER TABLE ONLY public.professions
    ADD CONSTRAINT professions_pkey PRIMARY KEY (id);
