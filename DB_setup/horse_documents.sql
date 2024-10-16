CREATE TABLE horse_documents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    horse_id INTEGER NOT NULL,
    document_type_id INTEGER NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    url VARCHAR(256),
    file_path VARCHAR(256),
    FOREIGN KEY (horse_id) REFERENCES horses(id),
    FOREIGN KEY (document_type_id) REFERENCES horse_document_types(id)
);
