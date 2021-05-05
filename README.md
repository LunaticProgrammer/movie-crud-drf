# drf-chunked-upload example

[![Python Version](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.2-brightgreen.svg)](https://djangoproject.com)
[![Django Rest Framework Version](https://img.shields.io/badge/djangorestframework-3.12-brightgreen.svg)](https://www.django-rest-framework.org/)

This is a Django demo project of the drf-chunked-upload module.

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/LunaticProgrammer/movie-crud-drf.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Apply the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a user (superuser):

```bash
python manage.py createsuperuser
```

Finally, run the development server:

```bash
python manage.py runserver
```

To run the tests

```bash
python manage.py test
```

The API endpoints will be available at **127.0.0.1:8000**.
