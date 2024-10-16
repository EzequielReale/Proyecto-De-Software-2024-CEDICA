CREATE TABLE public.horse_members (
    horse_id integer NOT NULL,
    member_id integer NOT NULL
);

INSERT INTO public.horse_members VALUES (1, 1);
INSERT INTO public.horse_members VALUES (2, 1);

ALTER TABLE ONLY public.horse_members
    ADD CONSTRAINT horse_members_pkey PRIMARY KEY (horse_id, member_id);

ALTER TABLE ONLY public.horse_members
    ADD CONSTRAINT horse_members_horse_id_fkey FOREIGN KEY (horse_id) REFERENCES public.horses(id);

ALTER TABLE ONLY public.horse_members
    ADD CONSTRAINT horse_members_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id);