CREATE TABLE public.tipos (
    id serial PRIMARY KEY,  -- Usamos serial para auto-incrementar
    tipo varchar(50) NOT NULL
);

INSERT INTO public.tipos (tipo) VALUES ('Honorarios'), ('Varios'), ('Proveedor');
