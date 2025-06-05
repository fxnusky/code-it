# Prototype of a Real-Time Gamified Coding Competition Web Application

## Project Description
This repository contains six folders:

- **/backend**: Contains the code to run the Game Service
- **/db**: Contains an initialization file to start the database for local execution
- **/frontend**: Contains the UI of the application
- **/isolate-base**: Used to initialize the Isolate environment, installing all dependencies (used in development to avoid re-installing them every time the application starts)
- **/isolate-service**: Contains the code to run the Code Execution Service
- **/k6**: Contains load tests

## Project Execution
1. Install Docker Desktop: https://docs.docker.com/desktop/
2. Clone this repository
3. Add to the root directory an `.env` file with the following environment variables:
- DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydatabase
- ISOLATE_SERVICE_URL=http://isolate-service:8001
- FRONTEND_URL=http://localhost:3000
4. From the root repository, execute:
```
docker-compose up
```
5. Access the following sites to see the services:
- Frontend: http://localhost:3000
- Game Service: http://localhost:8000
- Code Execution Service: http://localhost:8001

## Load Test Execution
To run any of the tests against the local code, the project must be running, and k6 must be installed: https://grafana.com/docs/k6/latest/set-up/install-k6/

Run the tests using these commands:
```
// Code Execution Service Load Tests
k6 run code-execution.js

// Code Submission Load Tests
k6 run code-submission.js

// Game Service WebSocket Load Test (change SEED for each run)
SEED=1 k6 run ws.js
```

Parameters inside the tests can be changed as needed to regulate the work load or other characteristics.

## Deployed application
The deployed version of the application can be seen at:
- Frontend: https://www.code-it-game.xyz
- Game Service: http://34.51.190.45:8000
- Code Execution Service: http://34.51.176.219:8001

These links will be available until 11/07/2025.