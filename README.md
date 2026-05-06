# Tracking-Games-Django

A Django web app for tracking your game collection, wishlist, play status, progress, and reviews.

## ✨ Technologies

- **Django 5.2.11**
- **Python 3.11**
- **PostgreSQL**
- **HTML / CSS / JavaScript** (Django templates + static files)
- **WhiteNoise** (static files in production)
- **Gunicorn** (production WSGI server)
- **python-dotenv** (load environment variables from `.env`)
- **dj-database-url** (database config from `DATABASE_URL`)

## 🚀 Features

- **Authentication**: sign up, login, logout
- **Game CRUD**: add, edit, view, and delete games
- **Status tracking**: *backlog*, *playing*, *completed*, *dropped*
- **Wishlist**: keep games you want to play later and move them into *playing*
- **Progress tracking**: add progress notes and track hours played over time
- **Reviews**: rate games (1–5) and leave comments
- **Dashboard**: quick view of owned games + wishlist
- **AJAX support** for progress + review actions (add/edit/delete) without full page refresh
- **User isolation**: you can only view/edit your own games

## 🛠️ The Process

This project was built as a simple “personal game tracker” to practice full-stack Django development.

The core workflow is:

1. **Users create an account and log in**.
2. They **add games** and assign a **status** (backlog/playing/completed/dropped).
3. A game can have multiple **progress entries** (notes + hours played) that get stored and displayed in reverse chronological order.
4. Users can also leave **reviews** with a rating and comment.
5. Some actions (progress + reviews) support **AJAX requests** so the UI can update smoothly.

## ▶️ Running the Project

### 1) Clone the repository

```bash
git clone https://github.com/K2222810/Tracking-Games-Django.git
cd Tracking-Games-Django
```

### 2) Create + activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3) Install dependencies

This repo uses **Pipenv** (there’s a `Pipfile`), so the recommended install is:

```bash
pip install pipenv
pipenv install
pipenv shell
```

### 4) Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

Notes:
- Locally, `DEBUG` defaults to `True` unless `ON_HEROKU` is set.
- In production, you should set `ON_HEROKU=1` (or replace this with your own env flag).

### 5) Configure the database

**Local (current settings):** the project is configured to use **PostgreSQL** with the DB name `TrackingGameDataBase`.

Make sure PostgreSQL is installed and you have a database created:

```bash
createdb TrackingGameDataBase
```

(If your local Postgres setup requires a username/password/host, you’ll want to update `trackingGame/settings.py` to include those fields.)

### 6) Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7) Create an admin user (optional)

```bash
python manage.py createsuperuser
```

### 8) Start the dev server

```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## 📌 Notes (Deployment)

- Production server: `gunicorn` (`Procfile` uses `web: gunicorn trackingGame.wsgi`)
- For Heroku-style deployment:
  - set `ON_HEROKU=1`
  - set `DATABASE_URL` (used by `dj-database-url`)
  - run `python manage.py collectstatic`

