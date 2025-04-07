CREATE TABLE IF NOT EXISTS game_templates (
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    google_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    active_room VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(100) NOT NULL,
    room_code VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_code VARCHAR(100) NOT NULL,
    template_id INTEGER REFERENCES game_templates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    template_id INTEGER REFERENCES game_templates(id) ON DELETE CASCADE,
    order_key FLOAT NOT NULL,
    time_limit INTEGER NOT NULL
);

INSERT INTO game_templates DEFAULT VALUES;

INSERT INTO questions (description, template_id, order_key, time_limit)
VALUES 
('Lorem ipsum dolor sit amet...', 1, 1, 30),
('Which planet is known as the Red Planet?', 1, 2, 15);