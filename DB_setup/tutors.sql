CREATE TABLE tutors (
    id SERIAL PRIMARY KEY,
    relationship relationships NOT NULL,
    name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    dni VARCHAR(9) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    education_level education_levels NOT NULL,
    job VARCHAR(64) NOT NULL
);

CREATE TYPE relationships AS ENUM ('Padre', 'Madre', 'Tutor');
CREATE TYPE education_levels AS ENUM ('Primario', 'Secundario', 'Terciario', 'Universitario');


INSERT INTO tutors (relationship, name, last_name, dni, address, phone, email, education_level, job)
VALUES
('Padre', 'Juan', 'Perez', '12345678', 'Calle Falsa 123', '123456789', 'juanperez@gmail.com', 'Primario', 'Docente'),
('Madre', 'Maria', 'Gomez', '22345678', 'Calle Verdadera 456', '223456789', 'mariagomez@gmail.com', 'Secundario', 'Enfermera');
