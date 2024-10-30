DROP TABLE IF EXISTS public.job_proposals;

CREATE TABLE IF NOT EXISTS public.job_proposals
(
    id SERIAL NOT NULL,
    institutional_work_proposal institutional_work_proposals NOT NULL,
    condition conditions NOT NULL,
    headquarters headquarters NOT NULL,
    days days_of_week[] NOT NULL,
    rider_id integer NOT NULL,
    professor_id integer NOT NULL,
    member_horse_rider_id integer NOT NULL,
    horse_id integer NOT NULL,
    assistant_id integer NOT NULL,
    CONSTRAINT job_proposals_pkey PRIMARY KEY (id),
    CONSTRAINT job_proposals_assistant_id_fkey FOREIGN KEY (assistant_id)
        REFERENCES public.members (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT job_proposals_horse_id_fkey FOREIGN KEY (horse_id)
        REFERENCES public.horses (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT job_proposals_member_horse_rider_id_fkey FOREIGN KEY (member_horse_rider_id)
        REFERENCES public.members (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT job_proposals_professor_id_fkey FOREIGN KEY (professor_id)
        REFERENCES public.members (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT job_proposals_rider_id_fkey FOREIGN KEY (rider_id)
        REFERENCES public.riders (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public.job_proposals
    OWNER to grupo04;


INSERT INTO job_proposals (institutional_work_proposal, condition, headquarters, days, rider_id, professor_id, member_horse_rider_id, horse_id, assistant_id)
VALUES ('Hipoterapia', 'Regular', 'CASJ', ARRAY['Lunes', 'Miércoles', 'Viernes'], 1, 1, 1, 1, 1);
