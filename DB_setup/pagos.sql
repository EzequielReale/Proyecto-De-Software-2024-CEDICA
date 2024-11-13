CREATE TABLE public.pagos (
    id SERIAL PRIMARY KEY,
    beneficiario_id integer NOT NULL REFERENCES public.members(id) ON DELETE CASCADE,
    monto integer NOT NULL,
    fecha_pago timestamp without time zone NOT NULL,
    tipo_pago_id integer NOT NULL REFERENCES public.tipos(id) ON DELETE CASCADE,
    descripcion character varying(255) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- INSERT INTO public.pagos VALUES (1, 2, 2000, '2024-10-14 02:24:19.052364', 1, 'h', '2024-10-14 02:24:19.055548', '2024-10-14 02:24:19.05555');
