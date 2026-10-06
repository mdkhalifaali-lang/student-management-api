# Student Management API

A backend REST API built with FastAPI for managing student records with JWT authentication, user-based access control, validation, filtering, pagination, sorting, and automated testing.

## Features

* User registration and login
* Secure password hashing with bcrypt
* JWT-based authentication
* Protected student endpoints
* User-based student ownership
* Student CRUD operations
* Get individual student by ID
* Case-insensitive student filtering
* Pagination
* Sorting
* Request validation with Pydantic
* SQLite database with SQLAlchemy
* Environment-based secret configuration
* Automated API tests with Pytest

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* Passlib / bcrypt
* Pytest
* Git & GitHub

## Project Structure

```text
student-management-api/
│
├── main.py
├── database.py
├── models.py
├── auth_models.py
├── schemas.py
├── requirements.txt
├── requirements-dev.txt
|-- render.yaml
├── .gitignore
│
├── routers/
│   ├── auth.py
│   └── students.py
│
└── tests/
    ├── conftest.py
    ├── test_api.py
    └── test_students.py
```

## API Endpoints

### Authentication

| Method | Endpoint         | Description                   |
| ------ | ---------------- | ----------------------------- |
| POST   | `/auth/register` | Register a new user           |
| POST   | `/auth/login`    | Login and receive a JWT token |

### Students

| Method | Endpoint                 | Description                                  |
| ------ | ------------------------ | -------------------------------------------- |
| GET    | `/students/`             | Get students belonging to the logged-in user |
| GET    | `/students/{student_id}` | Get one student                              |
| POST   | `/students/`             | Create a student                             |
| PUT    | `/students/{student_id}` | Update a student's details                   |
| DELETE | `/students/{student_id}` | Delete a student                             |

## Student List Features

The student listing endpoint supports:

### Filtering

```text
GET /students/?name=ava
GET /students/?course=biology
```

Filtering is case-insensitive.

### Pagination

```text
GET /students/?skip=0&limit=10
```

### Sorting

```text
GET /students/?sort_by=name&order=desc
```

Supported sorting fields include:

* `id`
* `name`
* `age`
* `course`

Supported ordering:

* `asc`
* `desc`

## Authentication

Student endpoints require a valid JWT access token.

After logging in through:

```text
POST /auth/login
```

the returned access token can be provided through the Swagger **Authorize** button.

The API also ensures that users can access and modify only their own student records.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=<your-long-random-secret>
```

Use a strong random value for `SECRET_KEY`. The application exits with an error if it is missing. Keep the `.env` file private; it is excluded from Git using `.gitignore`.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/mdkhalifaali-lang/student-management-api.git
cd student-management-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install the runtime dependencies:

```bash
pip install -r requirements.txt
```

To run the test suite, install the development and testing dependencies (including the runtime dependencies):

```bash
pip install -r requirements-dev.txt
```

## Running the API

Start the FastAPI development server:

```powershell
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Live Deployment

The API is deployed on Render:

* Live API: [https://student-management-api-nvdl.onrender.com](https://student-management-api-nvdl.onrender.com)
* Swagger / API documentation: [https://student-management-api-nvdl.onrender.com/docs](https://student-management-api-nvdl.onrender.com/docs)

### Deploying to Render

The repository includes `render.yaml`, which configures the Render web service, installs dependencies from `requirements.txt`, starts the application with Uvicorn, and generates the `SECRET_KEY` environment variable. To deploy, connect this repository to Render and create the service from the existing Blueprint configuration in `render.yaml`. Keep `SECRET_KEY` in Render's environment configuration; never commit its value or store it in the repository.

The current Render free deployment uses SQLite on an ephemeral filesystem. Database data may be lost when the service restarts or is redeployed.

## Running Tests

Run the complete automated test suite:

```powershell
python -m pytest
```

Current test result:

```text
16 passed
```

## Security Notes

* Passwords are stored as bcrypt hashes rather than plain text.
* JWT authentication protects student endpoints.
* The JWT secret is read from the `SECRET_KEY` environment variable (or the local `.env` file) and the application refuses to start if it is missing.
* `.env` and the local SQLite database are excluded from Git.

## Project Status

The project currently includes authentication, authorization, CRUD operations, filtering, pagination, sorting, validation, and automated API testing.

Docker is not required to run the project locally.
