# Tracking-Games-Django

## Technologies

- Django 5.2.11
- Python 3.11
- PostgreSQL
- HTML
- CSS
- JavaScript
- WhiteNoise
- Gunicorn
- `python-dotenv`
- `dj-database-url`

## Features

- User sign up and login
- Add, edit, and delete games
- Game status tracking: backlog, playing, completed, and dropped
- Wishlist management
- Game progress entries with hours played and notes
- Reviews with ratings and comments
- Dashboard view for tracking owned and wishlisted games
- AJAX support for adding, editing, and deleting progress and reviews
- User-specific game access and authentication protection

## 

## 

## The process and how to install

### Local setup

1. Clone the repository:

```bash
git clone https://github.com/K2222810/Tracking-Games-Django.git
cd Tracking-Games-Django
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

If you are using Pipenv:

```bash
pipenv install
pipenv shell
```

4. Set up environment variables in a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

5. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

### Deployment notes

- Use `gunicorn` as the production server.
- Set `ON_HEROKU=1` in production if deploying with Heroku.
- Make sure `DATABASE_URL` is configured in production.
- Run `python manage.py collectstatic` before deploying static files.
