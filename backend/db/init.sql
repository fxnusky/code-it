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
    room_code VARCHAR(100) NOT NULL,
    token VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_code VARCHAR(100) NOT NULL,
    template_id INTEGER REFERENCES game_templates(id) ON DELETE CASCADE,
    game_state VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    template_id INTEGER REFERENCES game_templates(id) ON DELETE CASCADE,
    order_key FLOAT NOT NULL,
    time_limit INTEGER NOT NULL,
    code_starter TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_cases (
    case_id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    input TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    is_hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS submissions (
    submission_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    player_id INTEGER NOT NULL,  
    code TEXT NOT NULL,
    earned_points INTEGER NOT NULL DEFAULT 0,
    submission_time TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_case_executions (
    case_execution_id SERIAL PRIMARY KEY,
    submission_id INTEGER NOT NULL REFERENCES submissions(submission_id) ON DELETE CASCADE,
    case_id INTEGER NOT NULL REFERENCES test_cases(case_id) ON DELETE CASCADE,
    obtained_output TEXT NOT NULL,
    correct BOOLEAN NOT NULL
);


INSERT INTO game_templates DEFAULT VALUES;

INSERT INTO questions (description, template_id, order_key, time_limit, code_starter, language)
VALUES 
    ('Write a function called "add" that takes two numbers as arguments and returns their sum.', 
     1, 1, 60, 'def add(a, b):\n    # Your code here', 'python'),
     
    ('Write a function called "is_even" that takes a number and returns True if it''s even, False otherwise.', 
     1, 2, 45, 'def is_even(num):\n    # Your code here', 'python'),
     
    ('Write a function called "reverse_string" that takes a string and returns the reversed version.', 
     1, 3, 75, 'def reverse_string(s):\n    # Your code here', 'python');


INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (1, '2, 3', '5', FALSE),
    (1, '-1, 1', '0', FALSE),
    (1, '0, 0', '0', FALSE),
    (1, '100, 200', '300', TRUE); 

INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (2, '4', 'True', FALSE),
    (2, '7', 'False', FALSE),
    (2, '0', 'True', FALSE),
    (2, '-2', 'True', TRUE);  

INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (3, '"hello"', '"olleh"', FALSE),
    (3, '""', '""', FALSE),
    (3, '"a"', '"a"', FALSE),
    (3, '"racecar"', '"racecar"', TRUE);