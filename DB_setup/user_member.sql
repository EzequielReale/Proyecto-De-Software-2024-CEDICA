CREATE TABLE user_member (
    user_id INTEGER NOT NULL REFERENCES users(id),
    member_id INTEGER NOT NULL REFERENCES members(id) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
