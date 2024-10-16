CREATE TABLE disability_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

INSERT INTO disability_types (name) 
VALUES 
('Mental'),
('Motora'),
('Sensorial'),
('Visceral');
