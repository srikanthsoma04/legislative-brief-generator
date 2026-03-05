CREATE TABLE IF NOT EXISTS bills (
    id VARCHAR PRIMARY KEY,
    state VARCHAR(2) NOT NULL,
    session VARCHAR(50),
    title TEXT,
    description TEXT,
    status VARCHAR(100),
    introduced_date DATE,
    updated_date TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sponsors (
    id SERIAL PRIMARY KEY,
    bill_id VARCHAR REFERENCES bills(id),
    name VARCHAR(200),
    party VARCHAR(50),
    role VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS votes (
    id VARCHAR PRIMARY KEY,
    bill_id VARCHAR REFERENCES bills(id),
    vote_date DATE,
    yes_count INT,
    no_count INT,
    passed BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_bills_state ON bills(state);
CREATE INDEX IF NOT EXISTS idx_bills_status ON bills(status);
CREATE INDEX IF NOT EXISTS idx_sponsors_bill_id ON sponsors(bill_id);