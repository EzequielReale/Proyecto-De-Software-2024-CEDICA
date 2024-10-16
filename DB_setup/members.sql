CREATE TABLE members (
    id INTEGER PRIMARY KEY REFERENCES persons(id),
    email VARCHAR(64) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    condition condition_types NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    profession_id INTEGER REFERENCES professions(id),
    job_id INTEGER NOT NULL REFERENCES jobs(id)
);

INSERT INTO members (id, email, start_date, end_date, condition, active, profession_id, job_id)
VALUES (1, 'giuliana_0@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', TRUE, 1, 1);