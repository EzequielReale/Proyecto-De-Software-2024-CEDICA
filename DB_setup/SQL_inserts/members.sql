CREATE TABLE public.members (
    id integer NOT NULL,
    email character varying(64) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    condition public.condition_types NOT NULL,
    active boolean,
    profession_id integer,
    job_id integer NOT NULL
);


INSERT INTO public.members VALUES (1, 'giuliana@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (2, 'giuliana_0@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (4, 'giuliana_1@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (6, 'giuliana_2@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (8, 'giuliana_3@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (10, 'giuliana_4@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (12, 'giuliana_5@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (14, 'giuliana_6@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (16, 'giuliana_7@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (18, 'giuliana_8@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (20, 'giuliana_9@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (22, 'giuliana_10@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (24, 'giuliana_11@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (26, 'giuliana_12@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (28, 'giuliana_13@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (30, 'giuliana_14@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (32, 'giuliana_15@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (34, 'giuliana_16@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (36, 'giuliana_17@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (38, 'giuliana_18@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (40, 'giuliana_19@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (42, 'giuliana_20@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (44, 'giuliana_21@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (46, 'giuliana_22@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (48, 'giuliana_23@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (50, 'giuliana_24@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (52, 'giuliana_25@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (54, 'giuliana_26@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (56, 'giuliana_27@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (58, 'giuliana_28@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);
INSERT INTO public.members VALUES (60, 'giuliana_29@gmail.com', '2023-01-01', '2023-12-31', 'Voluntario', true, 1, 1);


ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_id_fkey FOREIGN KEY (id) REFERENCES public.persons(id);

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_profession_id_fkey FOREIGN KEY (profession_id) REFERENCES public.professions(id);
