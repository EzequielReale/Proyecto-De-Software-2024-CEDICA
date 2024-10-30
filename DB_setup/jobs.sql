CREATE TABLE public.jobs (
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);

INSERT INTO public.jobs VALUES (1, 'Administrativo/a', 'Gestiona tareas administrativas en oficinas, asegurando la eficiencia operativa diaria.');
INSERT INTO public.jobs VALUES (2, 'Terapeuta', 'Facilita procesos de sanación y desarrollo personal mediante técnicas terapéuticas.');
INSERT INTO public.jobs VALUES (3, 'Conductor', 'Maneja caballos garantizando la seguridad y comodidad de pasajeros.');
INSERT INTO public.jobs VALUES (4, 'Auxiliar de pista', 'Asiste en la gestión y cuidado de caballos en pistas de equitación, garantizando seguridad.');
INSERT INTO public.jobs VALUES (5, 'Herrero', 'Artesano que forja metales, creando herramientas y piezas personalizadas a medida.');
INSERT INTO public.jobs VALUES (6, 'Veterinario', 'Diagnostica y trata enfermedades en animales, ofreciendo cuidados preventivos y educativos.');
INSERT INTO public.jobs VALUES (7, 'Entrenador de Caballos', 'Forma y entrena caballos para competencias o trabajo, desarrollando habilidades específicas.');
INSERT INTO public.jobs VALUES (8, 'Domador', 'Adiestra caballos para establecer confianza y control entre el animal y el jinete.');
INSERT INTO public.jobs VALUES (9, 'Profesor de Equitación', 'Enseña técnicas de monta y manejo de caballos, promoviendo seguridad en la práctica.');
INSERT INTO public.jobs VALUES (10, 'Docente de Capacitación', 'Forma a adultos en conocimientos y habilidades para mejorar su desempeño laboral.');
INSERT INTO public.jobs VALUES (11, 'Auxiliar de mantenimiento', 'Realiza mantenimiento preventivo y correctivo en instalaciones para asegurar su óptimo funcionamiento.');
INSERT INTO public.jobs VALUES (12, 'Otro', 'Otros trabajos variados no mencionados que abarcan diversas funciones y responsabilidades.');
