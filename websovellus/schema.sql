-- All databases in use:


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE plant (
    id SERIAL PRIMARY KEY,
    name TEXT, 
    latinname TEXT,
    light TEXT,
    water TEXT, 
    other TEXT,
    user_id int references users(id),
    visibility TEXT
);


CREATE TABLE directions (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    direction TEXT 
);


CREATE TABLE note1 (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    user_id int references users(id),
    name TEXT
);

CREATE TABLE emojis (
    id SERIAL PRIMARY KEY,
    number INTEGER
);


