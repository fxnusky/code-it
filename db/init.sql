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
    code_starter TEXT NOT NULL,
    main_function TEXT NOT NULL,
    language VARCHAR(20) NOT NULL DEFAULT 'python'
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


INSERT INTO game_templates (id) 
VALUES
    (1),
    (2),
    (3);

INSERT INTO questions (description, id, template_id, order_key, time_limit, code_starter, main_function)
VALUES 
    ('Write a function called "add" that takes two numbers as arguments and returns their sum.', 
     1, 1, 1, 600, 'def add(a, b):\n    # Your code here\n\nprint(add(1, 2)) #EXAMPLE: SHOULD RETURN 3', 'add'),
     
    ('Write a function called "is_even" that takes a number and returns True if it''s even, False otherwise.', 
     2, 1, 2, 450, 'def is_even(num):\n    # Your code here\n\nprint(is_even(2)) #EXAMPLE: SHOULD RETURN True', 'is_even'),
     
    ('Write a function called "reverse_digits" that takes a positive integer and returns the reversed version.', 
     3, 1, 3, 750, 'def reverse_digits(d):\n    # Your code here\n\nprint(reverse_digits(12345)) #EXAMPLE: SHOULD RETURN 54321', 'reverse_digits');


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
    (3, '12345', '54321', FALSE),
    (3, '0', '0', FALSE),
    (3, '98642', '24689', FALSE),
    (3, '78', '87', TRUE);

INSERT INTO questions (description, id, template_id, order_key, time_limit, code_starter, main_function)
VALUES 
    ('Write a function called "is_prime" that takes a number and returns True if it''s prime, False otherwise.', 
     4, 2, 1, 1200, 'def is_prime(n):\n    # Your code here\n\nprint(is_prime(7)) #EXAMPLE: SHOULD RETURN True', 'is_prime');

INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (4, '2', 'True', FALSE),
    (4, '3', 'True', FALSE),
    (4, '4', 'False', FALSE),
    (4, '17', 'True', FALSE),
    (4, '1', 'False', FALSE),
    (4, '0', 'False', TRUE),
    (4, '-5', 'False', TRUE),
    (4, '19', 'True', TRUE),
    (4, '20', 'False', TRUE),
    (4, '23', 'True', TRUE),
    (4, '29', 'True', TRUE),
    (4, '31', 'True', TRUE),
    (4, '37', 'True', TRUE),
    (4, '41', 'True', TRUE),
    (4, '43', 'True', TRUE),
    (4, '47', 'True', TRUE),
    (4, '49', 'False', TRUE),
    (4, '53', 'True', TRUE),
    (4, '59', 'True', TRUE),
    (4, '61', 'True', TRUE);

INSERT INTO questions (description, id, template_id, order_key, time_limit, code_starter, main_function, language)
VALUES 
    ('Write a function called "add" that takes two integers and returns their sum.', 
     5, 3, 1, 600, '#include <stdio.h>\n\nint add(int a, int b) {\n    // Your code here\n}\n\nint main() {\n    printf("%d", add(1, 2)); //EXAMPLE: SHOULD RETURN 3\n    return 0;\n}', 'add', 'c'),
     
    ('Write a function called "is_even" that takes an integer and returns 1 if it''s even, 0 otherwise.', 
     6, 3, 2, 450, '#include <stdio.h>\n\nint is_even(int num) {\n    // Your code here\n}\n\nint main() {\n    printf("%d", is_even(2)); //EXAMPLE: SHOULD RETURN 1\n    return 0;\n}', 'is_even', 'c'),
     
    ('Write a function called "reverse_digits" that takes a positive integer and returns the reversed version.', 
     7, 3, 3, 750, '#include <stdio.h>\n\nint reverse_digits(int d) {\n    // Your code here\n}\n\nint main() {\n    printf("%d", reverse_digits(12345)); //EXAMPLE: SHOULD RETURN 54321\n    return 0;\n}', 'reverse_digits', 'c');

INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (5, '2, 3', '5', FALSE),
    (5, '-1, 1', '0', FALSE),
    (5, '0, 0', '0', FALSE),
    (5, '100, 200', '300', TRUE),
    (5, '2147483647, 1', '-2147483648', TRUE); 

INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (6, '4', '1', FALSE),
    (6, '7', '0', FALSE),
    (6, '0', '1', FALSE),
    (6, '-2', '1', TRUE),
    (6, '-3', '0', TRUE);

INSERT INTO test_cases (question_id, input, expected_output, is_hidden)
VALUES
    (7, '"hello"', '"olleh"', FALSE),
    (7, '""', '""', FALSE),
    (7, '"a"', '"a"', FALSE),
    (7, '"racecar"', '"racecar"', TRUE),
    (7, '"12345"', '"54321"', TRUE);