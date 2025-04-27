Health Information System (HealthIS)
A basic health information management system API built with Django and Django REST Framework.
This system enables doctors and healthcare providers to efficiently manage clients and health programs.

Features
Create and manage health programs (e.g., TB, Malaria, HIV)

Register new clients with detailed profiles

Enroll clients in one or more health programs

Search clients by name

View client profiles including enrolled programs

Expose client profiles via RESTful API endpoints

Token-based authentication for secure API access

Tech Stack
Python 3.x

Django 4.x

Django REST Framework

PostgreSQL (production-ready database)

SQLite (default for development/testing)

Token Authentication

Setup & Installation
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/HealthIS.git
cd HealthIS
Create and activate a virtual environment

python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
Install dependencies


pip install -r requirements.txt
Configure the database

Default: SQLite (no configuration needed)

For production, update settings.py with your PostgreSQL database credentials.

Run database migrations

bash
Copy
Edit
python manage.py migrate
Create a superuser

bash
Copy
Edit
python manage.py createsuperuser
Run the development server

bash
Copy
Edit
python manage.py runserver
API Endpoints

Endpoint Method Description
/api/healthprograms/ POST Create a new health program
/api/clients/ POST Register a new client
/api/clients/{id}/enroll/ POST Enroll a client in a health program
/api/clients/ GET Search clients
/api/clients/{id}/profile/ GET View a client’s profile
Testing
Run tests using Django’s built-in test framework:

bash
Copy
Edit
python manage.py test
Deployment
This app can be deployed on platforms like Render, Heroku, or AWS. When deploying, ensure you:

Use PostgreSQL as the production database.

Set environment variables for sensitive data such as SECRET_KEY and database credentials.

Collect static files with:


python manage.py collectstatic
Future Improvements
Implement JWT Authentication for enhanced security

Add role-based access control for better permission management

Improve client search with pagination and filters

Develop a frontend UI for easier interaction

License
This project is open-source and licensed under the MIT License.

Author
Christine Omwansa - Software Engineering Intern
GitHub Profile URL - https://github.com/Christine-code-crypto/HealthInformationSystem.git
