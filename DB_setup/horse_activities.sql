CREATE TABLE public.horse_activities (
    horse_id SERIAL PRIMARY KEY,
    activity_id integer NOT NULL REFERENCES activities(id) ON DELETE CASCADE
);

-- INSERT INTO public.horse_activities VALUES (1, 1);
-- INSERT INTO public.horse_activities VALUES (1, 3);
-- INSERT INTO public.horse_activities VALUES (1, 2);
-- INSERT INTO public.horse_activities VALUES (2, 3);
-- INSERT INTO public.horse_activities VALUES (2, 2);
