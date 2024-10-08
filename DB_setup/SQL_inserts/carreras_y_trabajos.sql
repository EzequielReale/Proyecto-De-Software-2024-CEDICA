-- DROP TABLE IF EXISTS professions;

CREATE TABLE IF NOT EXISTS professions
(
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);


INSERT INTO professions (name, description) 
VALUES 
('Psicólogo/a', 'Especialista en salud mental que evalúa y trata trastornos emocionales para el bienestar del paciente.'),
('Psicomotricista', 'Promueve el desarrollo motriz y la coordinación a través de actividades físicas y lúdicas.'),
('Médico/a', 'Profesional de la salud que diagnostica y trata enfermedades, enfocándose en la prevención y el cuidado integral.'),
('Kinesiólogo/a', 'Utiliza técnicas de movimiento para mejorar la movilidad y función física en rehabilitación.'),
('Terapista Ocupacional', 'Ayuda a mantener habilidades para la vida diaria, enfocándose en ocupaciones significativas.'),
('Psicopedagogo/a', 'Educador que aborda dificultades educativas y promueve el desarrollo integral del estudiante.'),
('Docente', 'Facilita el aprendizaje y desarrollo de habilidades en estudiantes mediante diversas metodologías.'),
('Profesor', 'Enseña materias específicas, promoviendo conocimientos y habilidades a través de estrategias efectivas.'),
('Fonoaudiólogo/a', 'Diagnostica y trata trastornos de comunicación y lenguaje, mejorando la deglución y la voz.'),
('Veterinario/a', 'Cuidado y tratamiento de enfermedades en animales, promoviendo su bienestar y prevención.'),
('Otro', 'Otras profesiones diversas no mencionadas en diferentes áreas y especialidades.');


-- DROP TABLE IF EXISTS jobs;

CREATE TABLE IF NOT EXISTS jobs
(
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);


INSERT INTO jobs (name, description) 
VALUES 
('Administrativo/a', 'Gestiona tareas administrativas en oficinas, asegurando la eficiencia operativa diaria.'),
('Terapeuta', 'Facilita procesos de sanación y desarrollo personal mediante técnicas terapéuticas.'),
('Conductor', 'Maneja vehículos garantizando la seguridad y comodidad de pasajeros o entrega de mercancías.'),
('Auxiliar de pista', 'Asiste en la gestión y cuidado de caballos en pistas de equitación, garantizando seguridad.'),
('Herrero', 'Artesano que forja metales, creando herramientas y piezas personalizadas a medida.'),
('Veterinario', 'Diagnostica y trata enfermedades en animales, ofreciendo cuidados preventivos y educativos.'),
('Entrenador de Caballos', 'Forma y entrena caballos para competencias o trabajo, desarrollando habilidades específicas.'),
('Domador', 'Adiestra caballos para establecer confianza y control entre el animal y el jinete.'),
('Profesor de Equitación', 'Enseña técnicas de monta y manejo de caballos, promoviendo seguridad en la práctica.'),
('Docente de Capacitación', 'Forma a adultos en conocimientos y habilidades para mejorar su desempeño laboral.'),
('Auxiliar de mantenimiento', 'Realiza mantenimiento preventivo y correctivo en instalaciones para asegurar su óptimo funcionamiento.'),
('Otro', 'Otros trabajos variados no mencionados que abarcan diversas funciones y responsabilidades.');

