CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    image TEXT,
    rating INTEGER,
    duration TEXT,
    ingredients TEXT,
    source TEXT
);