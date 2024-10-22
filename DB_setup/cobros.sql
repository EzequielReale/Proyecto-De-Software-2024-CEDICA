CREATE TABLE pagos_jinetes_amazonas (
    id SERIAL PRIMARY KEY,
    fecha_pago timestamp without time zone NOT NULL,
    monto INTEGER NOT NULL,
    en_deuda BOOLEAN DEFAULT FALSE,
    observaciones VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    jinete_amazona_id INTEGER NOT NULL REFERENCES riders(id) ON DELETE CASCADE,
    medio_de_pago_id INTEGER NOT NULL REFERENCES medios_de_pago(id) ON DELETE CASCADE,
    receptor_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE
);
