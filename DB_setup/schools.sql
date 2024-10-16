CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    address VARCHAR(128) NOT NULL,
    phone VARCHAR(16) NOT NULL,
    level school_levels NOT NULL,
    year INTEGER NOT NULL,
    observations TEXT NOT NULL,
    rider_id INTEGER NOT NULL REFERENCES riders(id)
);

INSERT INTO schools (name, address, phone, level, year, observations, rider_id)
VALUES ('Escuela_0', 'Calle Falsa 120', '123456780', 'Primario', 5, 'Observaciones de la escuela 0', 1);
