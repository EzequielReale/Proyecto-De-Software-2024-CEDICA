CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    dni VARCHAR(16) NOT NULL,
    phone VARCHAR(32) NOT NULL,
    emergency_phone VARCHAR(32) NOT NULL,
    street VARCHAR(128) NOT NULL,
    number VARCHAR(8) NOT NULL,
    floor VARCHAR(4),
    apartment VARCHAR(8),
    health_insurance VARCHAR(32) NOT NULL,
    health_insurance_number VARCHAR(32) NOT NULL,
    locality_id INTEGER NOT NULL REFERENCES localities(id),
    type VARCHAR(16),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);