# EVENT PLANET

A RESTful, API-first event management platform built with Django REST Framework and PostgreSQL.

## Features

- User registration and token authentication
- Participant and Organizer roles
- Event creation and management
- Event status management: Draft, Published, Closed, and Finished
- Multi-stage events with independent schedules and ordering
- Dynamic event attributes using a typed Entity-Attribute-Value (EAV) model
- Event registration with capacity and duplicate-registration checks
- Feedback for eligible participants after event completion
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
3. Configure the required PostgreSQL environment variables.
4. Build and start the containers:

```bash
docker compose up --build -d
```

The application will be available at:

http://127.0.0.1:8000/

Django migrations are applied automatically when the web container starts.

## Environment Variables

Configure the following variables in `.env`:

```env
SECRET_KEY='replace_with_a_long_random_secret_key'
POSTGRES_DB=event_planet
POSTGRES_USER=event_planet_user
POSTGRES_PASSWORD=replace_with_a_strong_password
```

The application also supports `POSTGRES_HOST` and `POSTGRES_PORT`. Docker Compose sets these for the web service.

Do not commit `.env` or real credentials to version control.

## Create a Superuser

Run:

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

## Useful Commands

Run automated tests:

```bash
docker compose exec web python manage.py test
```

Check the Django configuration:

```bash
docker compose exec web python manage.py check
```

Show migration status:

```bash
docker compose exec web python manage.py showmigrations
```

Stop the containers:

```bash
docker compose down
```

## API Endpoints

### Accounts

- `/api/accounts/register/` — User registration
- `/api/accounts/login/` — Token login
- `/api/accounts/profile/` — User profile

### Events

- `/api/events/` — Public event list
- `/api/events/<id>/` — Public event details
- `/api/organizer/events/` — Organizer event management
- `/api/organizer/events/<id>/status/` — Event status management
- `/api/organizer/events/<event_id>/stages/` — Manage event stages
- `/api/organizer/events/<event_id>/stages/<stage_id>/` — Retrieve, update, or delete a stage
- `/api/organizer/events/<event_id>/attributes/` — Manage event attribute definitions
- `/api/organizer/events/<event_id>/attribute-values/` — Manage event attribute values

### Registrations

- `/api/events/<event_id>/register/` — Register for a published event
- `/api/registrations/my-registrations/` — List the authenticated participant's registrations
- `/api/registrations/organizer/events/<event_id>/registrations/` — List participants registered for the organizer's own event

### Feedback

- `/api/feedback/` — Submit and list the authenticated participant's feedback
- `/api/feedback/organizer/events/<event_id>/feedback/` — List feedback for an organizer's own event

### Results

- `/api/organizer/events/<event_id>/results/` — Publish results for an eligible event
- `/api/results/` — Public list of published results
- `/api/results/<id>/` — Public result details

All endpoints should be used with the appropriate HTTP method and authentication where required.

## Event Stages and Registration Decision

Events may contain multiple stages. Each stage belongs to one event and has its own title, description, order, and time range.

Registration is **event-based**, not stage-based: a participant registers for the event as a whole, rather than registering separately for each stage. The event's capacity applies to the event registration count.

## Dynamic Attributes

Event attributes are defined separately from their values. The EAV model allows attributes to be reused without adding a database column for each new attribute. Attribute values are stored separately and validated according to their defined types.

## Testing

The project currently has 36 automated tests. Run them using:

```bash
docker compose exec web python manage.py test
```


## Frontend

The project includes a React frontend built with Vite.

### Technologies

- React
- Vite
- JavaScript
- CSS

### Requirements

- Node.js
- npm
- The Django backend running through Docker Compose

### Run the Frontend

Open a new terminal in the project root and run:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend in your browser:

http://localhost:5173/

The Vite development server proxies `/api` requests to the Django backend at `http://localhost:8000`.

Keep the Django backend running while using the frontend.

### Frontend Features

- Public event listing and event details
- User registration and token-based login
- Participant and organizer roles
- Organizer dashboard
- Event creation through the Django API
- Event status transitions through the organizer API

## Running the Full Application

1. Start the backend using the Docker Compose setup described above.
2. Ensure the backend is available at `http://localhost:8000/`.
3. Start the React frontend using the commands in the Frontend section.
4. Open `http://localhost:5173/`.

## Git

Make sure `.env`, virtual environments, `node_modules`, build output, and local database files are excluded from version control. Never commit real credentials or tokens.
