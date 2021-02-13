DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS ues;
DROP TABLE IF EXISTS colleges;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS item_per_colleges;
DROP TABLE IF EXISTS lss;


CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE ues (
    ue_id TEXT PRIMARY KEY,
    ue_name TEXT NOT NULL
);

CREATE TABLE colleges (
    college_id TEXT PRIMARY KEY,
    college_name TEXT NOT NULL
);

CREATE TABLE item_per_colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    college_id TEXT NOT NULL,
    FOREIGN KEY(college_id) REFERENCES colleges(college_id),
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);

CREATE TABLE items (
    item_id TEXT PRIMARY KEY,
    ue_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    FOREIGN KEY(ue_id) REFERENCES ues(ue_id)
    
);

CREATE TABLE lss (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date DATE NOT NULL,
    -- ue_id TEXT NOT NULL,
    college_id TEXT NOT NULL,
    item_id TEXT,
    serieux INTEGER,
    rang_a BOOL NOT NULL,
    rang_B BOOL NOT NULL,
    -- FOREIGN KEY(ue_id) REFERENCES ues(id),
    FOREIGN KEY(college_id) REFERENCES colleges(college_id),
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);
