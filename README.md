#Online Food Delivery Platform
This is a Django REST Framework  project

## Features
- Admin can view ongoing orders
- Admin can view completed orders

## Technologies Used
- Python
- Django
- Django REST Framework

## How to Run
1. Create virtual environment
2. Install requirements
3. Run server

## Project setup(commands to run
- python -m venv env
- env\Scripts\activate
- pip install django djangorestframework
- django-admin startproject ecommerce_project cd ecommerce_project
- python manage.py startapp orders
- python manage.py makemigrations 
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

## other urls to check output and postman urls
- http://127.0.0.1:8000/admin/
- GET http://127.0.0.1:8000/api/admin/orders/
- GET http://127.0.0.1:8000/api/admin/orders/?status=ONGOING
- GET http://127.0.0.1:8000/api/admin/orders/?status=COMPLETED



## Features
- Admin-only access
- Filter orders by status
- Django REST Framework based API
- Tested using Postman

## Author 
Jahnavi K