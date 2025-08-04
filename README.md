# Aurora Project

Aurora Project is a web application for project and task management built with Django. The system is designed for teams who want to efficiently organize their work, track progress, and manage tasks.

## Key Features

- **Task Management**: Create, assign, and track tasks across your projects
- **Project Management**: Organize work into projects with priority and status settings
- **Calendar View**: Visualize tasks and deadlines in a calendar format
- **Team Collaboration**: Assign tasks to team members and work together
- **Progress Tracking**: Monitor project progress and task completion

## Technologies

- Django 4.x
- Python 3.x
- SQLite (for development)
- HTML/CSS (custom styles without Bootstrap)

## Installation and Setup

1. Clone the repository´
1. `cd aurora´
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`

## Project Structure

- `aurora_store/` - main Django application
  - `models.py` - data models (Project, Task, User)
  - `views.py` - request handling views
  - `urls.py` - URL routing
  - `templates/` - HTML templates
  - `forms.py` - forms for data creation and editing

## License

MIT License

