CREATE TABLE disability_diagnoses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    type_id INTEGER NOT NULL,
    FOREIGN KEY (type_id) REFERENCES disability_types(id)
);

INSERT INTO disability_diagnoses (name, type_id) 
VALUES 
('ECNE, Lesión post-traumática', 2), -- Ejemplo: Motora
('Mielomeningocele', 2),
('Esclerosis Múltiple', 2),
('Escoliosis Leve', 2),
('Secuelas de ACV', 2),
('Discapacidad Intelectual', 1), -- Ejemplo: Mental
('Trastorno del Espectro Autista', 1),
('Trastorno del Aprendizaje', 1),
('Trastorno por Déficit de Atención/Hiperactividad', 1),
('Trastorno de la Comunicación', 1),
('Trastorno de Ansiedad', 1),
('Síndrome de Down', 1),
('Retraso Madurativo', 1),
('Psicosis', 1),
('Trastorno de Conducta', 1),
('Trastornos del ánimo y afectivos', 1),
('Trastorno Alimentario', 1),
('OTRO', 1);
