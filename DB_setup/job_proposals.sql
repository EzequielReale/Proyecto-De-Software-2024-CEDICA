CREATE TABLE job_proposals (
    id SERIAL PRIMARY KEY,
    institutional_work_proposal institutional_work_proposals NOT NULL,
    condition conditions NOT NULL,
    headquarters headquarters NOT NULL,
    days VARCHAR[] NOT NULL,
    rider_id INTEGER NOT NULL REFERENCES riders(id),
    professor_id INTEGER NOT NULL REFERENCES members(id),
    member_horse_rider_id INTEGER NOT NULL REFERENCES members(id),
    horse_id INTEGER NOT NULL REFERENCES horses(id),
    assistant_id INTEGER NOT NULL REFERENCES members(id)
);

INSERT INTO job_proposals (institutional_work_proposal, condition, headquarters, days, rider_id, professor_id, member_horse_rider_id, horse_id, assistant_id)
VALUES ('Hipoterapia', 'Regular', 'CASJ', ARRAY['Lunes', 'Miércoles', 'Viernes'], 1, 1, 1, 1, 1);
