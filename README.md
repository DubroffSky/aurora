# 🌅 Aurora - TaskFlow Management System

<div align="center">

![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A modern, intuitive project and task management platform designed to streamline team collaboration and boost productivity.**

</div>

---

## Project Overview

**Aurora** is a comprehensive web-based project management system built with Django that transforms how teams organize, track, and execute their work. This platform combines powerful task management capabilities with intuitive project organization, making it an ideal solution for development teams, marketing agencies, and any organization seeking to improve their workflow efficiency.

## Key Features

### **Advanced Task Management**
- Create, assign, and track tasks with detailed descriptions
- Priority levels (Low, Medium, High, Urgent) for effective prioritization
- Status tracking (To Do, In Progress, Review, Completed)
- Due date management with calendar integration
- Task assignment to team members

### **Project Organization**
- Create and manage multiple projects
- Project priority and status management
- Team member invitation and management
- Project progress tracking and analytics
- Hierarchical organization of tasks within projects

### **Team Collaboration**
- User registration and authentication system
- Role-based access control
- Team member management within projects
- Task assignment and ownership tracking
- Collaborative project workspaces

### **Calendar Integration**
- Visual calendar view of all tasks and deadlines
- Interactive calendar interface
- Deadline tracking and notifications
- Project timeline visualization

### **Security & User Management**
- Secure user authentication and authorization
- User profile management
- Session management and logout functionality
- Protected routes and views

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | Django 4.x |
| **Programming Language** | Python 3.x |
| **Database** | PostgreSQL (Development) |
| **Frontend** | HTML5, CSS3 (Custom styling) |
| **Authentication** | Django's built-in auth system |
| **Template Engine** | Django Templates |
| **Version Control** | Git |

---

## 📁 Project Architecture

```
aurora/
├── aurora_store/          # Main Django application
│   ├── models.py          # Data models (Project, Task, User)
│   ├── views.py           # Business logic and request handling
│   ├── urls.py            # URL routing configuration
│   ├── forms.py           # Form handling and validation
│   ├── templates/         # HTML templates with custom styling
│   └── migrations/        # Database schema migrations
├── aurora/                # Django project settings
│   ├── settings.py        # Application configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI application entry point
└── requirements.txt       # Python dependencies
```

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aurora
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Register a new account or login with your superuser credentials

---

## Database Models

### Core Entities

- **User**: Authentication and user management
- **Project**: Project organization with priority and status
- **Task**: Individual work items with assignment and tracking
- **Order/Product**: E-commerce functionality (in development)

### Key Features
- **Many-to-Many Relationships**: Projects can have multiple members
- **Foreign Key Relationships**: Tasks belong to projects, users can be assigned tasks
- **Audit Trails**: Created/updated timestamps on all models
- **Status Management**: Comprehensive status and priority systems

---

## User Interface

The application features a clean, modern interface with:
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Intuitive Navigation**: Easy-to-use menu system
- **Visual Feedback**: Success/error messages and status indicators
- **Calendar Integration**: Interactive calendar view for task management
- **Custom Styling**: Professional appearance without external CSS frameworks

---

## Development Status

**⚠️ This project is currently in active development**

### ✅ Completed Features
- User authentication and registration
- Project creation and management
- Task creation, assignment, and tracking
- Calendar view for task visualization
- Basic user interface and styling

### 🚧 In Development
- Enhanced calendar functionality
- Real-time notifications
- Advanced reporting and analytics
- API endpoints for mobile integration
- Performance optimizations

### 📋 Planned Features
- Email notifications
- File upload capabilities
- Advanced search and filtering
- Mobile application
- Integration with external tools

---

## Contributing

This project is currently in development and not accepting external contributions at this time. However, feedback and suggestions are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

