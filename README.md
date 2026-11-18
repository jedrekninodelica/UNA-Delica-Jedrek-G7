# UNA

UNA is a web-based workload tracking and analytics system for college students and instructors.
Instructors post course deadlines, and students rate how approachable each task feels.
UNA ranks the tasks and shows the single task to start now on a "Focus One" screen.

Built with full-stack Django (Django templates) and PostgreSQL hosted on Supabase.
This project started from the CampusConnect class activity and was extended for UNA.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill it in.
   - `SECRET_KEY`: any long random string.
   - `DATABASE_URL`: in Supabase, click **Connect** and copy the **Session pooler** URI. Put in your database password.
4. Create the tables and an admin account:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run the server and open http://127.0.0.1:8000
   ```bash
   python manage.py runserver
   ```

