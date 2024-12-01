CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    alias VARCHAR(100),
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    isActive BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.users VALUES (1, 'admin', '$2b$12$PFZB97rGVqLFh2wcztzG7OBTFwv8UkhPrOrQbm4WmguGJWqqCXegO', 'admin@admin.com', true, '2024-10-14 02:24:18.65506', '2024-10-14 02:24:18.655064');
