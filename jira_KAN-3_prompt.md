# Implementation Task

## Objective
Create a calculator application featuring a JavaScript-based user interface and a secure authentication page to restrict access.

## Context
The application requires a full-stack implementation including a frontend for the UI, a backend for authentication and session management, and a database to store user credentials.

## Requirements
- **Authentication System**: A login page that validates user credentials against a database.
- **Session Management**: Implementation of a mechanism (e.g., JWT or sessions) to ensure the calculator is only accessible to authenticated users.
- **Calculator Logic**: A functional engine capable of performing basic mathematical operations.
- **User Interface**: 
    - A login form for authentication.
    - A calculator interface with a display screen and buttons for digits and operators.
- **Database**: A user table to store usernames and hashed passwords.

## Implementation
1. **Backend Setup**:
    - Use Python (Flask or FastAPI) to create the server.
    - Implement a database schema for users (username, hashed_password).
    - Create an authentication endpoint (`/login`) that verifies credentials and returns a session token.
    - Create a protected route/middleware to verify the token before serving the calculator logic or page.
2. **Frontend Setup**:
    - Create an HTML/CSS/JS login page.
    - Create an HTML/CSS/JS calculator page.
    - Implement JavaScript logic to handle the calculator's arithmetic operations and UI updates.
    - Implement client-side routing/redirection to ensure unauthenticated users are sent to the login page.
3. **Integration**:
    - Connect the frontend login form to the backend authentication endpoint.
    - Store the session token securely (e.g., HttpOnly cookie or LocalStorage).

## Acceptance Criteria
- [ ] User is redirected to an authentication page upon accessing the application.
- [ ] User cannot access the calculator without valid credentials.
- [ ] User can successfully log in with valid credentials.
- [ ] Calculator interface is displayed after successful authentication.
- [ ] Calculator performs basic mathematical operations correctly.

## Validation
- **Authentication Test**: Attempt to access the calculator URL directly without logging in; verify redirection to login.
- **Login Test**: Enter invalid credentials and verify access is denied; enter valid credentials and verify access is granted.
- **Functional Test**: Perform a series of calculations (addition, subtraction, multiplication, division) and verify the results are correct.
- **Security Test**: Verify that passwords are stored as hashes in the database and not in plain text.

## Final Report
The final report must include:
- A list of all created/modified files.
- Confirmation that all acceptance criteria are met.
- Instructions on how to initialize the database and run the application.