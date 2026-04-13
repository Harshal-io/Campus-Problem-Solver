CREATE TABLE IF NOT EXISTS problems (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    image_path TEXT,
    reg_no TEXT,
    email TEXT,
    urgency TEXT,
    category TEXT,
    confidence REAL,
    department TEXT,
    status TEXT DEFAULT 'Submitted',
    resolution_note TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact_email TEXT,
    category TEXT
);
