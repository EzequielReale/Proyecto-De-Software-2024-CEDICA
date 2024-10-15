-- DROP TABLE IF EXISTS professions;

CREATE TABLE IF NOT EXISTS professions
(
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);


INSERT INTO professions (id, name, description) 
VALUES 
(1, 'Psicólogo/a', 'Especialista en salud mental que evalúa y trata trastornos emocionales para el bienestar del paciente.'),
(2, 'Psicomotricista', 'Promueve el desarrollo motriz y la coordinación a través de actividades físicas y lúdicas.'),
(3, 'Médico/a', 'Profesional de la salud que diagnostica y trata enfermedades, enfocándose en la prevención y el cuidado integral.'),
(4, 'Kinesiólogo/a', 'Utiliza técnicas de movimiento para mejorar la movilidad y función física en rehabilitación.'),
(5, 'Terapista Ocupacional', 'Ayuda a mantener habilidades para la vida diaria, enfocándose en ocupaciones significativas.'),
(6, 'Psicopedagogo/a', 'Educador que aborda dificultades educativas y promueve el desarrollo integral del estudiante.'),
(7, 'Docente', 'Facilita el aprendizaje y desarrollo de habilidades en estudiantes mediante diversas metodologías.'),
(8, 'Profesor', 'Enseña materias específicas, promoviendo conocimientos y habilidades a través de estrategias efectivas.'),
(9, 'Fonoaudiólogo/a', 'Diagnostica y trata trastornos de comunicación y lenguaje, mejorando la deglución y la voz.'),
(10, 'Veterinario/a', 'Cuidado y tratamiento de enfermedades en animales, promoviendo su bienestar y prevención.'),
(11, 'Otro', 'Otras profesiones diversas no mencionadas en diferentes áreas y especialidades.');


-- DROP TABLE IF EXISTS jobs;

CREATE TABLE IF NOT EXISTS jobs
(
    id SERIAL PRIMARY KEY,
    name character varying(64) NOT NULL,
    description character varying(128) NOT NULL
);


INSERT INTO jobs (id, name, description) 
VALUES 
(1, 'Administrativo/a', 'Gestiona tareas administrativas en oficinas, asegurando la eficiencia operativa diaria.'),
(2, 'Terapeuta', 'Facilita procesos de sanación y desarrollo personal mediante técnicas terapéuticas.'),
(3, 'Conductor', 'Monta caballos y se encarga de su manejo durante el transporte y las actividades diarias.'),
(4, 'Auxiliar de pista', 'Asiste en la gestión y cuidado de caballos en pistas de equitación, garantizando seguridad'),
(5, 'Herrero', 'Artesano que forja metales, creando herramientas y piezas personalizadas a medida.'),
(6, 'Veterinario', 'Diagnostica y trata enfermedades en animales, ofreciendo cuidados preventivos y educativos.'),
(7, 'Entrenador de Caballos', 'Forma y entrena caballos para competencias o trabajo, desarrollando habilidades específicas.'),
(8, 'Domador', 'Adiestra caballos para establecer confianza y control entre el animal y el jinete.'),
(9, 'Profesor de Equitación', 'Enseña técnicas de monta y manejo de caballos, promoviendo seguridad en la práctica.'),
(10, 'Docente de Capacitación', 'Forma a adultos en conocimientos y habilidades para mejorar su desempeño laboral.'),
(11, 'Auxiliar de mantenimiento', 'Realiza mantenimiento preventivo y correctivo en instalaciones para asegurar su óptimo funcionamiento.'),
(12, 'Otro', 'Otros trabajos variados no mencionados que abarcan diversas funciones y responsabilidades.');
