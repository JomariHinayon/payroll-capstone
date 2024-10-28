# Payroll Management System

## Getting Started

### Development Installation

Installation requires an active version of Python 3.

1. Clone this repository.
2. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install all dependencies.

   ```
   pip3 install -r requirements.txt
   ```

4. Create an .env file in the root project folder with the following items:

   ```
   DEBUG=True
   ```

5. Create a database and start serving the dev server with the following commands:

   ```
   python3 manage.py migrate
   python3 manage.py runserver
   ```

5.1. To have access to site and admin page, create a superuser like so:

```
python3 manage.py createsuperuser
```

6. Access the development site at [http://localhost:8000/](http://localhost:8000/).
