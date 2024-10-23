CREATE TABLE medios_de_pago (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO medios_de_pago (tipo) VALUES ('Efectivo');
INSERT INTO medios_de_pago (tipo) VALUES ('Tarjeta de Crédito');
INSERT INTO medios_de_pago (tipo) VALUES ('Tarjeta de Débito');
