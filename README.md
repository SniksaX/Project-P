# Project Setup Guide

This project is a FastAPI application that manages users and movies. It includes functionalities such as email verification, JWT authentication, and integration with the TMDB API for movie details.

## Prerequisites

- Python 3.x installed (preferably Python 3.9+)
- pip package manager
- PostgreSQL (database must be installed and running)
- A Gmail account for sending verification emails
- Internet access for API calls (TMDB, email sending, etc.)

## Steps to Set Up the Project

### 1. Clone the Repository

Clone the repository to your local machine using:

```bash
git clone <repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd pyhtonstuff
```

### 3. Create and Activate a Virtual Environment (Optional but Recommended)

Create the virtual environment:

```bash
python -m venv venv
```

Activate the environment:

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

If a `requirements.txt` file exists, install the dependencies using:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages manually.

### 5. Set Up the Database

Ensure PostgreSQL is installed and running. Create a new database and a user with the necessary privileges. Update your database configuration in the environment variables (see next step) with your details:

- DATABASE_HOST
- DATABASE_PORT
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD

### 6. Configure Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```env
# Application Settings
SECRET_KEY=your_supersecret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=3333
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password

# Email Configuration
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Verification Token Settings
VERIFICATION_TOKEN_EXPIRE_MINUTES=1440

# TMDB API Credentials
TMDB_API_KEY=your_tmdb_api_key
TMDB_API_KEY_V4=your_tmdb_api_v4_key
```

#### Acquiring TMDB API Keys:

1. Visit [The Movie Database (TMDB)](https://www.themoviedb.org) and create an account if you don't already have one.
2. Navigate to your account settings and go to the [API section](https://www.themoviedb.org/settings/api).
3. Request an API key. You will typically receive an API key (v3) and an API v4 token.
4. Insert these keys into your `.env` file as `TMDB_API_KEY` and `TMDB_API_KEY_V4`.

#### Setting Up Gmail for Sending Emails:

1. Use a Gmail account to send verification emails.
2. It is recommended to use an App Password instead of your regular Gmail password for security reasons.
3. Enable 2-Step Verification on your Google account.
4. Go to [Google App Passwords](https://myaccount.google.com/apppasswords) and generate an App Password for "Mail".
5. Use the generated App Password as the value for `EMAIL_PASSWORD` in your `.env` file, and set `EMAIL_FROM` to your Gmail address.

### 7. Running the Project

Launch the FastAPI application using one of the following commands:

Using Uvicorn:

```bash
uvicorn main:app --reload
```

Or run directly using Python:

```bash
python main.py
```

The application will be accessible at [http://localhost:3000](http://localhost:3000).

## Troubleshooting & Additional Information

- Ensure all placeholders in the `.env` file are replaced with your actual credentials.
- Verify that your PostgreSQL database is properly set up and running.
- Check your Gmail account settings if you experience issues with sending emails; ensure that the App Password is correctly configured.
- Consult the [FastAPI documentation](https://fastapi.tiangolo.com/) and [PostgreSQL guides](https://www.postgresql.org/docs/) for more details on configuration and troubleshooting.

Enjoy building and running your application!
