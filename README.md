
# EVENT PLANET

A RESTful event management platform built with Django REST Framework and PostgreSQL.

## Features

- User registration and token authentication
- Participant and Organizer roles
- Event creation and management
- Event status management
- Dynamic event attributes with type validation
- Event registration with capacity and duplicate-registration checks
- Feedback submission for eligible participants
- Event results publication
- PostgreSQL database
- Docker and Docker Compose support

## Technologies

- Python 3.11
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose

## Requirements

- Docker Desktop
- Docker Compose

## Setup

1. Clone or download the project.
2. Create a `.env` file in the project root.
3. Configure the PostgreSQL environment variables.
4. Build and start the containers:

```bash
docker compose up --build
```

The application will be available at:

http://127.0.0.1:8000/

## Useful Commands

Run automated tests:

```bash
docker compose exec web python manage.py test
```

Check the Django configuration:

```bash
docker compose exec web python manage.py check
```

Stop the containers:

```bash
docker compose down
```

## API Endpoints

- `/api/accounts/register/` — User registration
- `/api/accounts/login/` — Token login
- `/api/accounts/profile/` — User profile
- `/api/` — Event API routes
- `/api/registrations/` — Registration API
- `/api/feedback/` — Feedback API
- `/api/results/` — Public results API

## Testing

The project includes 13 automated tests covering accounts, events, registrations, feedback, and results.

Run the tests using:

```bash
docker compose exec web python manage.py test
```

## Environment Variables

Configure the following variables in `.env`:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

The application also supports `POSTGRES_HOST` and `POSTGRES_PORT`.

Do not commit `.env` or real credentials to version control.
