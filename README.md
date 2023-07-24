# Site resume

To start the backend, follow these steps:

1. Clone this repository and open the terminal.
2. Install all project's requirements by running the following command:
pip install -r requirements.txt

3. Apply database migrations with the following command:
python manage.py migrate

4. Create a superuser by running the command:
python manage.py createsuperuser
Follow the instructions to enter a login and password for your superuser.

5. Finally, start the local server by running the command:
python manage.py runserver

This will start a Django backend server at [http://localhost:8000/](http://localhost:8000/).

To access the API:
- Go to [http://localhost:8000/tech/](http://localhost:8000/tech/) to access the API.
- Go to [http://localhost:8000/tech_relation/1/](http://localhost:8000/tech_relation/1/) to access the API communication between objects.

To access the Django admin page:
- Go to [http://localhost:8000/admin/](http://localhost:8000/admin/).