CREATE TABLE rider_member (
    rider_id INTEGER NOT NULL REFERENCES riders(id) ON DELETE CASCADE,
    member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    PRIMARY KEY (rider_id, member_id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

--INSERT INTO rider_member (2, 1);