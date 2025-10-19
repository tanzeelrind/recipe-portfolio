# Django Recipe Portfolio

A full-stack Django web application to manage recipes. Users can create, update, and delete recipes with images and Google OAuth login.

## Features
- User authentication with Django + Google OAuth
- CRUD operations for recipes
- Image upload for recipes
- Search recipes by name
- Responsive design

## Tech Stack
- Python 3.13
- Django 4.x
- HTML/CSS/Bootstrap
- SQLite (default)

## Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/recipe-portfolio.git
Create virtual environment:

bash
Copy code
python -m venv venv
venv\Scripts\activate
Install requirements:

bash
Copy code
pip install -r requirements.txt
Run migrations:

bash
Copy code
python manage.py migrate
Run server:

bash
Copy code
python manage.py runserver
Note:

Set your Google OAuth credentials in .env.

Media files are not included.
