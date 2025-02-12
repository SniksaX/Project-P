# FastAPI User and Movie Management API

This project implements a RESTful API using FastAPI for managing users and their movies.  It includes features for user registration, authentication, movie creation, and retrieval, along with rate limiting and robust error handling.  It uses PostgreSQL for data persistence.

## Features

*   **User Registration:**  Allows new users to register with a name, email, and password (minimum 8 characters).  Handles duplicate email registration attempts.
*   **User Authentication:** Implements token-based authentication using JWT (JSON Web Tokens).  Users can log in with their email and password to obtain an access token.
*   **Protected Routes:**  Most endpoints require a valid JWT for access, ensuring only authenticated users can perform actions.  Uses `OAuth2PasswordBearer`.
*   **User Management:**
    *   Get all users (requires authentication).
    *   Get a specific user by ID (requires authentication).
    *   Delete a user by ID (requires authentication).
*   **Movie Management:**
    *   Create a movie associated with a specific user (requires authentication, and the user ID in the path must match the authenticated user).
    *   Get a list of all movies associated with a specific user (requires authentication, and user ID validation).
*   **Rate Limiting:**  Uses `slowapi` to limit the number of requests per minute for various endpoints, preventing abuse.
*   **Data Validation:** Uses Pydantic models extensively for data validation, ensuring data integrity.
*   **Database Interaction:**  Uses `psycopg2` to interact with a PostgreSQL database.  Database operations are handled through a `DatabaseManager` class.
*   **Error Handling:**  Uses `HTTPException` to provide informative error responses for various scenarios (e.g., invalid credentials, database errors, validation errors, rate limits).
*   **Password Hashing:**  Uses `passlib` with bcrypt to securely store user passwords.

## Setup and Installation

1.  **Install Dependencies:**

    ```bash
    pip install fastapi uvicorn psycopg2-binary pydantic python-jose[cryptography] passlib python-dotenv slowapi
    ```
2.  **Database Setup:**

    *   Install PostgreSQL.
    *   Create a database `your_data_base_name`.
    *   Create a user `username` with password .  **Change these credentials for your setup.**
    *   Create a schema `your_schema_name`.
    *   Create the `users` and `movies` tables within the `userinfo` schema:

        ```sql
        CREATE SCHEMA userinfo;

        CREATE TABLE userinfo.users (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );

        CREATE TABLE userinfo.movies (
            id UUID PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 100),
            release_date DATE NOT NULL,
            user_id UUID REFERENCES userinfo.users(id),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        ```
3. **Configure Environment Variables (Optional but Recommended):**
    *   Create a `.env` file in the project root.
    *   Add the following line, replacing `"supersecretkey"` with a strong, randomly generated secret key:
       ```
       SECRET_KEY="supersecretkey"
       ```
    *   Uncomment lines referencing `config = config(".env")` in `config.py`
4.  **Run the Application:**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 3000 --reload
    ```
    The `--reload` flag enables automatic reloading of the server when code changes are detected.

## API Endpoints

| Method | Endpoint                     | Description                                     | Authentication | Rate Limit |
| :----- | :--------------------------- | :---------------------------------------------- | :------------- | :--------- |
| POST   | `/users`                     | Create a new user.                               | No             | 3/minute   |
| GET    | `/users`                     | Get all users.                                  | Yes            | 10/minute  |
| GET    | `/users/{user_id}`           | Get a specific user by ID.                      | Yes            | 2/minute   |
| DELETE | `/users/{user_id}`           | Delete a user by ID.                            | Yes            | 2/minute   |
| POST   | `/token`                     | Login and get an access token.                  | No             | -          |
| POST   | `/users/{user_id}/movies`    | Create a movie for a specific user.             | Yes            | 3/minute   |
| GET    | `/users/{user_id}/movies`    | Get all movies for a specific user.              | Yes            | 5/minute   |

**Request and Response Models:**

*   **`UserCreate`:** `name` (str), `email` (str), `password` (str, min length 8)
*   **`User`:** `id` (UUID), `name` (str), `email` (str)
*   **`TokenRequest`:** `email` (str), `password` (str)
*   **`Token`:** `access_token` (str), `token_type` (str, "bearer")
*   **`MovieCreate`:** `title` (str), `description` (str, optional), `rating` (int, 1-100), `release_date` (date)
*   **`Movie`:** `id` (UUID), `user_id` (UUID), `title` (str), `description` (str, optional), `rating` (int), `release_date` (date), `created_at` (datetime)

**Example Usage (using `curl`):**

1.  **Create a User:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com", "password": "securepassword"}' http://localhost:3000/users
    ```

2.  **Get an Access Token:**

    ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"email": "john.doe@example.com", "password": "securepassword"}' http://localhost:3000/token
    ```

    This will return a JSON object like:

    ```json
    {
      "access_token": "YOUR_ACCESS_TOKEN",
      "token_type": "bearer"
    }
    ```

3.  **Create a Movie (replace `YOUR_ACCESS_TOKEN` and `{user_id}`):**

    ```bash
    curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"title": "My Movie", "description": "A great movie", "rating": 85, "release_date": "2023-10-26"}' http://localhost:3000/users/{user_id}/movies
    ```

4.  **Get All Users (replace `YOUR_ACCESS_TOKEN`):**
    ```bash
    curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:3000/users
    ```
5. **Get movies for a user (replace `YOUR_ACCESS_TOKEN` and `{user_id}`):**
   ```bash
   curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:3000/users/{user_id}/movies
