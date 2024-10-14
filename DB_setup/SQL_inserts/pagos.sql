CREATE TABLE public.pagos (
    id integer NOT NULL,
    beneficiario_id integer,
    monto integer NOT NULL,
    fecha_pago timestamp without time zone NOT NULL,
    tipo_pago_id integer NOT NULL,
    descripcion character varying(255) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE SEQUENCE public.pagos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.pagos_id_seq OWNED BY public.pagos.id;
ALTER TABLE ONLY public.pagos ALTER COLUMN id SET DEFAULT nextval('public.pagos_id_seq'::regclass);

INSERT INTO public.pagos VALUES (1, 2, 2000, '2024-10-14 02:24:19.052364', 1, 'h', '2024-10-14 02:24:19.055548', '2024-10-14 02:24:19.05555');

SELECT pg_catalog.setval('public.pagos_id_seq', 1, true);

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_beneficiario_id_fkey FOREIGN KEY (beneficiario_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_tipo_pago_id_fkey FOREIGN KEY (tipo_pago_id) REFERENCES public.tipos(id);