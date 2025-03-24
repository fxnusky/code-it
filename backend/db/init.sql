CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    google_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO users (google_id, name, email) VALUES
('google-id-123', 'John Doe', 'john@example.com'),
('google-id-456', 'Jane Smith', 'jane@example.com');