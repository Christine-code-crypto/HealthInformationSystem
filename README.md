**Health Information System (HealthIS)**

A basic health information management system API built with Django and Django REST Framework. This system enables doctors and healthcare providers to efficiently manage clients and health programs.

**Features**

- Create and manage health programs (e.g., TB, Malaria, HIV)

- Register new clients with detailed profiles

- Enroll clients in one or more health programs

- Search clients by name

- View client profiles including enrolled programs

- Expose client profiles via RESTful API endpoints

**Token-based authentication for secure API access**

**Tech Stack**
- Python 3.12.6

- Django 4.2.8

- Django REST Framework 3.14.0

- SQLite database

**SETUP & INSTALLATION**

- Clone the repository
git clone https://github.com/Christine-code-crypto/HealthInformationSystem.git
cd HealthInformationSystem
- Create and activate a virtual environment
python -m venv venv
- Activate the virtual environment
venv\Scripts\activate

**INSTALL DEPENDANCIES**

- pip install -r requirements.txt
- Configure the database
Run database migrations
python manage.py migrate

- Create a superuser
python manage.py createsuperuser
- Run the development server
python manage.py runserver

- API Endpoints

/api/healthprograms/	POST	Create a new health program
/api/clients/	POST	Register a new client
/api/clients/{id}/enroll/	POST	Enroll a client in a health program
/api/clients/	GET	Search clients
/api/clients/{id}/profile/	GET	View a client’s profile

- Testing
Run tests using Django’s built-in test framework:

python manage.py test healthIS

- Deployment
This app has be deployed on Render platform

- Collect static files:

python manage.py collectstatic


Develop a frontend UI for easier interaction

- License
This project is open-source and licensed under the MIT License.

Author
Christine Omwansa - Software Engineering Intern
GitHub Profile: https://github.com/Christine-code-crypto/HealthInformationSystem
