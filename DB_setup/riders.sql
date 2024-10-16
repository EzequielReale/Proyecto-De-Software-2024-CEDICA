CREATE TABLE riders (
    id INTEGER PRIMARY KEY REFERENCES persons(id),
    birth_date DATE NOT NULL,
    grant_percentage FLOAT DEFAULT 0.0,
    family_allowance family_allowances,
    pension_benefit pension_benefits,
    has_guardianship BOOLEAN DEFAULT FALSE,
    disability_id INTEGER REFERENCES disability_diagnoses(id),
    city_of_birth_id INTEGER NOT NULL REFERENCES localities(id),
    tutor_1_id INTEGER REFERENCES tutors(id),
    tutor_2_id INTEGER REFERENCES tutors(id)
);

INSERT INTO riders (id, birth_date, grant_percentage, family_allowance, pension_benefit, has_guardianship, disability_id, city_of_birth_id, tutor_1_id, tutor_2_id)
VALUES (1, '2002-01-01', 20.0, 'Asignación universal por hijo', 'Nacional', TRUE, 1, 1, 1, 2);
