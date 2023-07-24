Site resume
Start a backend
1. After cloning this repo, open the terminal and install all project's requirements with help of this command:
pip install -r requirements.txt
2. Run the next command to apply db migrations:
python manage.py migrate
3. Create a superuser using next command:
python manage.py createsuperuser
Follow the instructions and enter login and password for your superuser.
4. Finally, to start a local server, run the next command:
python manage.py runserver
- This will start a Django backend server at http://localhost:8000/
- To access API, go to http://localhost:8000/tech/
- To access API communication between objects http://localhost:8000/tech_relation/1/
- To access Django admin page, go to http://localhost:8000/admin/
