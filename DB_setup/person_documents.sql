CREATE TABLE person_documents (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    document_path VARCHAR(255) NOT NULL,
    document_type document_type_enum,
    its_a_link BOOLEAN DEFAULT FALSE,
    person_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id)
);

CREATE TYPE document_type_enum AS ENUM (
    'Entrevista',
    'Evaluación',
    'Planificaciones',
    'Evolución',
    'Crónicas',
    'Documental'
);
