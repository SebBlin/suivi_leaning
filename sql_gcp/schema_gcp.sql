DROP TABLE IF EXISTS lss;
DROP TABLE IF EXISTS item_per_colleges;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS colleges;
DROP TABLE IF EXISTS ues;
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE ues (
    ue_id VARCHAR(200) PRIMARY KEY,
    UNIQUE INDEX ue_id_UNIQUE (ue_id ASC),
    ue_name TEXT NOT NULL
);

CREATE TABLE colleges (
    college_id VARCHAR(200) PRIMARY KEY,
    UNIQUE INDEX college_id_UNIQUE (college_id ASC),
    college_name TEXT NOT NULL
);

CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    ue_id VARCHAR(200) NOT NULL,
    item_name TEXT NOT NULL,
    UNIQUE INDEX item_id_UNIQUE (item_id ASC),
    FOREIGN KEY(ue_id) REFERENCES ues(ue_id)
    
);

CREATE TABLE item_per_colleges (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    item_id INTEGER NOT NULL,
    college_id VARCHAR(200) NOT NULL,
    FOREIGN KEY(college_id) REFERENCES colleges(college_id),
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);

CREATE TABLE lss (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date DATE NOT NULL,
    -- ue_id TEXT NOT NULL,
    college_id VARCHAR(200) NOT NULL,
    item_id INTEGER,
    serieux INTEGER,
    rang_a BOOL NOT NULL,
    rang_b BOOL NOT NULL,
    -- FOREIGN KEY(ue_id) REFERENCES ues(id),
    FOREIGN KEY(college_id) REFERENCES colleges(college_id),
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);
