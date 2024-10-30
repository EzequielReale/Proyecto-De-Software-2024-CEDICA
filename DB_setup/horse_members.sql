CREATE TABLE public.horse_members (
    horse_id integer NOT NULL,
    member_id integer NOT NULL,
    PRIMARY KEY (horse_id, member_id),
    FOREIGN KEY (horse_id) REFERENCES public.horses(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES public.members(id) ON DELETE CASCADE
);

-- INSERT INTO public.horse_members VALUES (1, 1);
-- INSERT INTO public.horse_members VALUES (2, 1);
