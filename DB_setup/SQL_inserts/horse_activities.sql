CREATE TABLE public.horse_activities (
    horse_id integer NOT NULL,
    activity_id integer NOT NULL
);

INSERT INTO public.horse_activities VALUES (1, 1);
INSERT INTO public.horse_activities VALUES (1, 3);
INSERT INTO public.horse_activities VALUES (1, 2);
INSERT INTO public.horse_activities VALUES (2, 3);
INSERT INTO public.horse_activities VALUES (2, 2);

ALTER TABLE ONLY public.horse_activities
    ADD CONSTRAINT horse_activities_pkey PRIMARY KEY (horse_id, activity_id);

ALTER TABLE ONLY public.horse_activities
    ADD CONSTRAINT horse_activities_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id);

ALTER TABLE ONLY public.horse_activities
    ADD CONSTRAINT horse_activities_horse_id_fkey FOREIGN KEY (horse_id) REFERENCES public.horses(id);
