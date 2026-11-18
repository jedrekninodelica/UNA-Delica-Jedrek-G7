# UNA

UNA is a web-based workload tracking and analytics system for college students and instructors.
Instructors post course deadlines, and students rate how approachable each task feels.
UNA ranks the tasks and shows the single task to start now on a "Focus One" screen.

Built with full-stack Django (Django templates) and PostgreSQL hosted on Supabase.
This project started from the CampusConnect class activity and was extended for UNA.

## Project Development 1: Account Feature

- **Sign up** with required fields, a valid and unique email, a unique username, and a matching password confirmation. Passwords are hashed by Django.
- **Log in and log out.** Wrong credentials show an error. Logging out ends the session.
- **Protected pages** use `LoginRequiredMixin`. Logged-out users are sent to the login page.
- **Two roles: Student and Instructor.** After login, each user goes to their own dashboard. Opening the other role's dashboard shows an "Access denied" page (403).
- **Profile.** Users view and edit their own name, email, course/program, contact number, and profile photo, and can change their password. The profile URLs have no user ID, so users can only reach their own profile.

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

## Tests

```bash
python manage.py test
```

## Main URLs

| URL | Page |
|---|---|
| `/accounts/signup/` | Sign up |
| `/accounts/login/` | Log in |
| `/` | Sends you to your role's dashboard |
| `/student/` | Student dashboard (students only) |
| `/instructor/` | Instructor dashboard (instructors only) |
| `/accounts/profile/` | View your profile |
| `/accounts/profile/edit/` | Edit your profile |
| `/accounts/password/change/` | Change your password |
| `/admin/` | Django admin (superusers only) |
