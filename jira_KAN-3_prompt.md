# Implementation Task

## Objective
Create a calculator application featuring a JavaScript-based user interface and a secure authentication page to restrict access.

## Context
The application requires a full-stack implementation including a frontend for the UI, a backend for authentication and session management, and a data store for user credentials.

## Requirements
- **Authentication System**: A login page that validates user credentials.
- **Session Management**: Mechanism to ensure the calculator is only accessible to authenticated users.
- **Calculator Engine**: Logic to perform basic mathematical operations.
- **User Interface**: 
    - A login form.
    - A calculator interface with a display and buttons for digits and operators.
- **Data Storage**: Storage for user credentials (usernames and hashed passwords).

## Implementation
1. **Backend (Python/Flask)**:
    - Implement a Flask server to handle routing and authentication.
    - Create an `/auth` endpoint to verify credentials and issue a session token/cookie.
    - Implement a middleware or decorator to protect the calculator route.
    - Use a secure hashing library (e.g., `werkzeug.security`) for password storage.
2. **Database**:
    - Implement a simple SQLite database to store user accounts.
3. **Frontend (HTML/CSS/JS)**:
    - Create `login.html` with a form for username and password.
    - Create `calculator.html` with a grid layout for the calculator.
    - Implement `calculator.js` to handle the mathematical logic and UI updates.
    - Implement `auth.js` to handle the login request and session redirection.

## Acceptance Criteria
- [ ] User is presented with an authentication page upon accessing the application.
- [ ] User cannot access the calculator without successful authentication.
- [ ] User can successfully log in with valid credentials.
- [ ] The calculator interface is rendered after login.
- [ ] The calculator performs basic mathematical operations correctly.

## Validation
1. **Auth Test**: Attempt to access the calculator URL directly without logging in; verify redirection to the login page.
2. **Login Test**: Enter invalid credentials; verify that access is denied.
3. **Access Test**: Enter valid credentials; verify redirection to the calculator interface.
4. **Functional Test**: Perform a series of calculations (addition, subtraction, multiplication, division) and verify the results are correct.

## Final Report
The final delivery must include:
- The backend server code.
- The database schema/initialization script.
- The frontend HTML, CSS, and JavaScript files.
- A brief summary of the changes made and the files created.