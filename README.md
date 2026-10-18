# 🎟️ EVENT PLANET

### Full-Stack Event Management Platform

A RESTful, API-first event management platform built with **Django REST Framework**, **PostgreSQL**, and a **React + Vite** frontend.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/DRF-REST%20API-red?style=for-the-badge" alt="Django REST Framework"/>
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/Vite-Frontend-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
</p>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies](#-technologies)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Backend Setup](#-backend-setup)
- [Environment Variables](#-environment-variables)
- [Create a Superuser](#-create-a-superuser)
- [Frontend Setup](#-frontend-setup)
- [API Endpoints](#-api-endpoints)
- [Event Lifecycle](#-event-lifecycle)
- [Event Stages and Registration](#-event-stages-and-registration)
- [Dynamic Attributes](#-dynamic-attributes)
- [Testing](#-testing)
- [Useful Commands](#-useful-commands)
- [Git and Security](#-git-and-security)

---

## 🌍 Overview

**EVENT PLANET** is a full-stack event management application that allows organizers to manage events while participants can discover events, register, and submit feedback after completion.

The application follows an API-first architecture. The Django REST Framework backend manages business logic, authentication, permissions, validation, and persistence, while the React frontend communicates with the API.

The project uses PostgreSQL as its database and Docker Compose to simplify local development.

## ✨ Features

- 🔐 User registration and token-based authentication
- 👥 Participant and Organizer roles
- 📅 Event creation and management
- 🔄 Event lifecycle management: Draft, Published, Closed, and Finished
- 🧩 Multi-stage events with independent schedules and ordering
- ⚙️ Typed Entity-Attribute-Value (EAV) model for dynamic event attributes
- 🎟️ Event registration with capacity and duplicate-registration checks
- ⭐ Feedback for eligible participants after event completion
- 🏆 Event results publication
- 🖥️ React frontend built with Vite
- 🐘 PostgreSQL database
- 🐳 Docker and Docker Compose support
- 🧪 Automated backend tests

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming language |
| Django 5.2 | Web framework |
| Django REST Framework | REST API and serialization |
| React | Frontend user interface |
| Vite | Frontend development server and build tool |
| JavaScript | Frontend programming language |
| CSS | Frontend styling |
| PostgreSQL | Relational database |
| Docker | Application containerization |
| Docker Compose | Local multi-container environment |
| Git and GitHub | Version control and source hosting |

## 🏗️ Project Structure

```text
event-planet/
├── accounts/          # User accounts and authentication
├── events/            # Events, stages and dynamic attributes
├── registrations/     # Event registration management
├── feedback/          # Participant feedback
├── results/           # Event results and publication
├── config/            # Django project configuration
├── frontend/          # React + Vite application
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

## 📋 Requirements

Before starting, make sure you have installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Docker Compose
- [Node.js and npm](https://nodejs.org/) for the frontend
- [Git](https://git-scm.com/) to clone the repository

## 🚀 Backend Setup

### 1. Clone the repository

```bash
git clone https://github.com/zahra-solhjoo/event-planet.git
cd event-planet
```

### 2. Configure environment variables

Create a `.env` file in the project root. See the [Environment Variables](#-environment-variables) section below.

### 3. Build and start the backend

```bash
docker compose up --build -d
```

Docker Compose starts PostgreSQL and the Django application. Database migrations are applied automatically when the web container starts.

The backend will be available at:

**http://127.0.0.1:8000/**

### 4. Check the backend

```bash
docker compose exec web python manage.py check
```

## 🔑 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=replace_with_a_long_random_secret_key
POSTGRES_DB=event_planet
POSTGRES_USER=event_planet_user
POSTGRES_PASSWORD=replace_with_a_strong_password
```

The application also supports `POSTGRES_HOST` and `POSTGRES_PORT`. Docker Compose configures these for the web service.

Use a strong secret key and database password. Never commit your real `.env` file or credentials to version control.

## 👤 Create a Superuser

Create a Django administrator account:

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to complete account creation.

## 🖥️ Frontend Setup

The project includes a React frontend powered by Vite.

### 1. Navigate to the frontend directory

Open a new terminal in the project root:

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

Open the frontend in your browser:

**http://localhost:5173/**

### Frontend Technologies

- React
- Vite
- JavaScript
- CSS

### Frontend Features

- Public event listing and event details
- User registration and token-based login
- Participant and Organizer roles
- Organizer dashboard
- Event creation through the Django API
- Event status transitions through the organizer API

The Vite development server proxies `/api` requests to the Django backend at `http://localhost:8000`. Keep the backend running while using the frontend.

## 🔌 API Endpoints

All endpoints use the `/api/` prefix. Use the appropriate HTTP method and authentication for each operation.

### 🔐 Accounts

| Endpoint | Description |
|---|---|
| `POST /api/accounts/register/` | Register a new user |
| `POST /api/accounts/login/` | Obtain an authentication token |
| `GET /api/accounts/profile/` | Retrieve the authenticated user's profile |

### 📅 Events

| Endpoint | Description |
|---|---|
| `GET /api/events/` | List published events |
| `GET /api/events/<id>/` | Retrieve published event details |
| `GET /api/organizer/events/` | List the organizer's events |
| `POST /api/organizer/events/` | Create an event |
| `PATCH /api/organizer/events/<id>/status/` | Update an event's status |

### 🧩 Stages and Dynamic Attributes

| Endpoint | Description |
|---|---|
| `/api/organizer/events/<event_id>/stages/` | Manage event stages |
| `/api/organizer/events/<event_id>/stages/<stage_id>/` | Retrieve, update, or delete a stage |
| `/api/organizer/events/<event_id>/attributes/` | Manage attribute definitions |
| `/api/organizer/events/<event_id>/attribute-values/` | Manage event attribute values |

### 🎟️ Registrations

| Endpoint | Description |
|---|---|
| `POST /api/registrations/events/<event_id>/register/` | Register for a published event |
| `GET /api/registrations/my-registrations/` | List the authenticated participant's registrations |
| `GET /api/registrations/organizer/events/<event_id>/registrations/` | List participants registered for the organizer's event |

### ⭐ Feedback

| Endpoint | Description |
|---|---|
| `/api/feedback/` | Submit or list the authenticated participant's feedback |
| `/api/feedback/organizer/events/<event_id>/feedback/` | List feedback for an organizer's event |

### 🏆 Results

| Endpoint | Description |
|---|---|
| `POST /api/organizer/events/<event_id>/results/` | Publish results for an eligible event |
| `GET /api/results/` | List published results |
| `GET /api/results/<id>/` | Retrieve published result details |

> **Note:** Protected endpoints require authentication and the appropriate role. Refer to the corresponding views and serializers for exact request and response schemas.

## 🔄 Event Lifecycle

Events follow a defined lifecycle:

```text
DRAFT → PUBLISHED → CLOSED → FINISHED
```

- **Draft:** The event is being prepared and is not publicly listed.
- **Published:** The event is publicly available and accepts registrations.
- **Closed:** New registrations are no longer accepted.
- **Finished:** The event has ended and can receive eligible feedback and published results.

## 🧩 Event Stages and Registration

Events can contain multiple stages. Each stage belongs to one event and has its own title, description, ordering, and schedule.

Registration is **event-based, not stage-based**. Participants register for the event as a whole rather than registering separately for each stage. The event's capacity applies to the total number of active registrations.

## ⚙️ Dynamic Attributes

EVENT PLANET uses a typed Entity-Attribute-Value (EAV) model to support flexible event attributes without adding a database column for every new attribute.

Supported data types include:

- Text
- Integer
- Decimal
- Boolean

Attribute definitions are stored separately from their values, and values are validated according to their configured types.

## 🧪 Testing

The project currently includes **38 automated tests** covering core application behavior.

Run the tests with:

```bash
docker compose exec web python manage.py test
```

Check the Django configuration:

```bash
docker compose exec web python manage.py check
```

## 🧰 Useful Commands

| Task | Command |
|---|---|
| Start services | `docker compose up -d` |
| Rebuild and start | `docker compose up --build -d` |
| View application logs | `docker compose logs -f web` |
| Run tests | `docker compose exec web python manage.py test` |
| Check Django | `docker compose exec web python manage.py check` |
| Show migrations | `docker compose exec web python manage.py showmigrations` |
| Create superuser | `docker compose exec web python manage.py createsuperuser` |
| Stop containers | `docker compose down` |

## 🔒 Git and Security

Make sure the following are excluded from version control:

- `.env` and other files containing secrets
- Python virtual environments
- `node_modules/`
- Frontend build output
- Local database files
- Python cache files

Never commit real credentials, secret keys, or authentication tokens.

---

<p align="center">
  <strong>EVENT PLANET</strong><br/>
  Built with Python, Django REST Framework, React, and PostgreSQL.
</p>

<p align="center">
  <a href="https://github.com/zahra-solhjoo">GitHub</a>
  ·
  <a href="https://www.linkedin.com/in/zahra-solhjoo-527965257/">LinkedIn</a>
</p>
