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
   git clone https://github.com/tanzeelrind/recipe-portfolio.git

**Create virtual environment:**
python -m venv venv
venv\Scripts\activate

**Install requirements:**
pip install -r requirements.txt

**Run migrations:**
python manage.py migrate

**Run server:**
python manage.py runserver


**Note:**
Set your Google OAuth credentials in .env.
Media files are not included.
