# 🎟️ EVENT PLANET

### Event Management REST API

<p align="center">
  A structured, API-first event management platform built with Django REST Framework and PostgreSQL.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/DRF-REST%20API-red?style=for-the-badge" alt="Django REST Framework"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
</p>

---

## 📌 Overview

**EVENT PLANET** is an API-first event management platform designed to organize events, manage participants, coordinate multi-stage schedules, collect feedback, and publish event results.

The backend is built with Django REST Framework and PostgreSQL, with token-based authentication, role-based access control, and Docker-based development.

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Authentication | User registration and token-based login |
| 👥 Role Management | Separate permissions for participants and organizers |
| 📅 Event Management | Create events and manage their lifecycle |
| 🔄 Event Lifecycle | Draft → Published → Closed → Finished |
| 🧩 Multi-stage Events | Organize event stages and assign roles |
| ⚙️ Dynamic Attributes | Typed event attributes without using JSON fields |
| 🎟️ Registration | Capacity validation and duplicate-registration prevention |
| ⭐ Feedback | Collect feedback for eligible completed events |
| 🏆 Results | Publish and publicly display event results |
| 🐳 Docker Support | Run the application with Docker Compose |

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Backend:** Django 5.2, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** DRF Token Authentication
- **Containerization:** Docker, Docker Compose
- **Version Control:** Git and GitHub

## 🏗️ Project Structure

```text
event_planet/
├── accounts/       # Users, registration and authentication
├── events/         # Events, stages and dynamic attributes
├── registrations/  # Event registration management
├── feedback/       # Participant feedback
├── results/        # Event results and publication
├── config/         # Django project configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Make sure you have installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/zahra-solhjoo/event-planet.git
cd event-planet
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=replace_with_a_long_random_secret_key
POSTGRES_DB=event_planet
POSTGRES_USER=event_planet_user
POSTGRES_PASSWORD=replace_with_a_strong_password
```

Use your own secret key and a strong database password. Never commit your real `.env` file to GitHub.

### 3. Start the application

```bash
docker compose up --build -d
```

The web container applies database migrations when it starts.

The API will be available at:

```text
http://localhost:8000/
```

### 4. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Run the test suite

```bash
docker compose exec web python manage.py test
```

### Useful Commands

```bash
# Check the Django configuration
docker compose exec web python manage.py check

# Inspect migrations
docker compose exec web python manage.py showmigrations

# View application logs
docker compose logs -f web

# Stop the containers
docker compose down
```

## 🔌 API Overview

All API endpoints use the `/api/` prefix.

### 🔐 Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts/register/` | Register a user |
| POST | `/api/accounts/login/` | Obtain an authentication token |
| GET | `/api/accounts/profile/` | Retrieve the authenticated user's profile |

### 📅 Events

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | List published events |
| GET | `/api/events/<id>/` | Retrieve a published event |
| GET / POST | `/api/organizer/events/` | List or create organizer-owned events |
| PATCH | `/api/organizer/events/<id>/status/` | Update an event's lifecycle status |

### 🧩 Stages and Dynamic Attributes

| Endpoint | Purpose |
|---|---|
| `/api/organizer/events/<event_id>/stages/` | Manage event stages |
| `/api/organizer/events/<event_id>/stages/<stage_id>/` | Retrieve or manage a stage |
| `/api/organizer/events/<event_id>/attributes/` | Manage dynamic attribute definitions |
| `/api/organizer/events/<event_id>/attribute-values/` | Manage event attribute values |

### 🎟️ Registrations

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/registrations/events/<event_id>/register/` | Register for an event |
| GET | `/api/registrations/my-registrations/` | View personal registrations |
| GET | `/api/registrations/organizer/events/<event_id>/registrations/` | View event participants |

### ⭐ Feedback

| Endpoint | Purpose |
|---|---|
| `/api/feedback/` | Create feedback and list the current participant's feedback |
| `/api/feedback/organizer/events/<event_id>/` | View feedback for an organizer-owned event |

### 🏆 Results

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/organizer/events/<event_id>/results/` | Publish results for a finished event |
| GET | `/api/results/` | List published results |
| GET | `/api/results/<id>/` | Retrieve published result details |

> **Note:** Protected endpoints require authentication and appropriate permissions. Requests with a body should use JSON where applicable. Consult the corresponding views and serializers for exact request and response schemas.

## 🔄 Event Lifecycle

Events follow a defined lifecycle:

```text
DRAFT
  ↓
PUBLISHED
  ↓
CLOSED
  ↓
FINISHED
```

- **Draft:** The event is being prepared and is not publicly listed.
- **Published:** The event is available to participants for registration.
- **Closed:** New registrations are no longer accepted.
- **Finished:** The event has ended and can have feedback and published results.

## 🧩 Dynamic Event Attributes

EVENT PLANET supports typed event attributes, allowing organizers to attach additional information to events.

Supported data types include:

- Text
- Integer
- Decimal
- Boolean

The data type is validated against the selected attribute, helping maintain consistent data.

## 🧪 Testing

The project includes automated tests for core application behavior, including:

- Event registration and capacity limits
- Duplicate-registration prevention
- User roles and access permissions
- Event status validation
- Feedback restrictions
- Event result publication
- Dynamic attribute validation and ownership checks

Run the test suite with:

```bash
docker compose exec web python manage.py test
```

## 🔒 Security Notes

- Keep secret keys and database credentials in environment variables.
- Do not commit `.env`, local databases, virtual environments, or generated build files.
- Use role-based permissions to protect organizer-only operations.
- Validate input through serializers and application-level rules.

## 🖥️ Optional Frontend

The backend is designed to be consumed through an API. If you use the optional React/Vite frontend included in the repository, follow its setup instructions and configure its development proxy to forward API requests to `http://localhost:8000`.

## 👩‍💻 Author

**Zahra Solhjoo**

- GitHub: [@zahra-solhjoo](https://github.com/zahra-solhjoo)
- LinkedIn: [Zahra Solhjoo](https://www.linkedin.com/in/zahra-solhjoo-527965257/)

---

<p align="center">
  Built with Python, Django REST Framework, and PostgreSQL.
</p>
