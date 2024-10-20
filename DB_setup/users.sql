CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    alias VARCHAR(100),
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    isActive BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);


CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


-- INSERT INTO public.users VALUES (1, 'admin', '$2b$12$PFZB97rGVqLFh2wcztzG7OBTFwv8UkhPrOrQbm4WmguGJWqqCXegO', 'admin@admin.com', true, '2024-10-14 02:24:18.65506', '2024-10-14 02:24:18.655064');
-- INSERT INTO public.users VALUES (2, 'giu', '$2b$12$U8nEBjUCd0R71txv8ydqnuuLvssx1q..uCF0fs4dohZ4.f4YfbbsO', 'giuliana@gmail.com', true, '2024-10-14 02:24:18.849304', '2024-10-14 02:24:18.849307');
-- INSERT INTO public.users VALUES (3, 'lau', '$2b$12$9Z/lTM3PUPV1//qKxtN9U.eI3WIBVpw0ymRzghyeTmfi1xJkYNKE6', 'lau@gmail.com', true, '2024-10-14 02:24:19.042834', '2024-10-14 02:24:19.042838');

SELECT pg_catalog.setval('public.users_id_seq', 3, true);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
