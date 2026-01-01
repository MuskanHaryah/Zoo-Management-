<div align="center">

# 🦁 Zoo Management System

### A Modern, Full-Stack Zoo Management Solution

[![Live Demo](https://img.shields.io/badge/Live%20Demo-zoo--management.up.railway.app-brightgreen?style=for-the-badge&logo=railway)](https://zoo-management.up.railway.app)
[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![REST API](https://img.shields.io/badge/REST-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://www.django-rest-framework.org/)

[Live Demo](https://zoo-management.up.railway.app) • [Report Bug](https://github.com/MuskanHaryah/Zoo-Management-/issues) • [Request Feature](https://github.com/MuskanHaryah/Zoo-Management-/issues)

</div>

---

## 📖 Overview

A comprehensive, production-ready web application designed for modern zoo management. Built with Django and Django REST Framework, this system streamlines animal care, staff coordination, visitor experiences, and operational workflows through an intuitive interface and robust API.

**🌐 Live Application:** [zoo-management.up.railway.app](https://zoo-management.up.railway.app)

### 🎯 Key Highlights

- 🏗️ **Enterprise Architecture**: Built on Django's MVT pattern with RESTful API endpoints
- 🔐 **Authentication & Authorization**: Secure role-based access control using Django-Allauth
- ☁️ **Cloud-Native**: Cloudinary integration for media management
- 📱 **Responsive Design**: Mobile-first frontend with modern CSS and JavaScript
- 🚀 **Production-Ready**: Deployed on Railway with PostgreSQL, WhiteNoise, and Gunicorn
- 🔄 **Real-Time Task Management**: Automated deadline tracking and notifications
- 📊 **Analytics Dashboard**: Comprehensive reporting and insights

---

## ✨ Features

### 🐾 Animal Management
- Complete CRUD operations for animal records
- Image uploads with Cloudinary integration
- Species categorization and health tracking
- Care schedule management

### 👥 Staff & Caretaker Portal
- Role-based dashboards (Admin, Caretaker, Visitor)
- Task assignment and tracking system
- Automated deadline monitoring with custom management commands
- Performance analytics and reporting

### 🎟️ Visitor Experience
- Public-facing visitor portal
- Event browsing and engagement
- Interactive content display
- Responsive design for all devices

### 🛡️ Security & Administration
- Django Admin Panel with custom configurations
- User authentication via Django-Allauth
- CORS-enabled REST API
- Secure file handling and validation

### ⚙️ Advanced Features
- Custom management commands for automation
- Database indexing for optimized queries
- Signal-based event handling
- Comprehensive error pages (403, 404, 500)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.2.7
- **API:** Django REST Framework 3.15.2
- **Database:** PostgreSQL (psycopg2-binary)
- **Authentication:** Django-Allauth 65.3.0
- **Task Queue:** Custom management commands

### Frontend
- **Templates:** Django Template Engine
- **Styling:** Custom CSS with modern design patterns
- **JavaScript:** Vanilla JS for interactivity
- **Media:** Cloudinary integration

### DevOps & Deployment
- **Hosting:** Railway
- **WSGI Server:** Gunicorn 23.0.0
- **Static Files:** WhiteNoise 6.8.2
- **Database:** PostgreSQL (Production)
- **Media Storage:** Cloudinary
- **Environment:** Python-Decouple for config management

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- **Python** 3.8 or higher
- **pip** (Python package manager)
- **PostgreSQL** 12+ (for production setup)
- **Git**
- **virtualenv** (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/MuskanHaryah/Zoo-Management-.git
cd Zoo-Management-
```

2. **Set up virtual environment**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment configuration**

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/zoo_db
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. **Database setup**

```bash
python manage.py migrate
```

6. **Create superuser**

```bash
python manage.py createsuperuser
```

7. **Collect static files** (for production)

```bash
python manage.py collectstatic
```

8. **Run development server**

```bash
python manage.py runserver
```

9. **Access the application**

- **Main Site:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **API Endpoints:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## 📁 Project Structure

```
zoo_management/
├── api/                      # REST API application
│   ├── models.py            # Database models
│   ├── views.py             # API views and viewsets
│   ├── urls.py              # API routing
│   ├── signals.py           # Django signals
│   └── management/          # Custom commands
│       └── commands/        # CLI commands
├── frontend/                # Frontend application
│   ├── templates/           # HTML templates
│   │   ├── caretaker/      # Staff portal
│   │   └── visitor/        # Public portal
│   └── static/             # CSS, JS, Images
├── zoo_management/          # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL routing
│   └── views.py            # Core views
├── staticfiles/            # Collected static files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Procfile               # Railway deployment config
├── runtime.txt            # Python version
└── build.sh               # Build script
```

---

## 🔧 Custom Management Commands

The system includes several custom Django commands for automation:

```bash
# Check and update expired tasks
python manage.py check_expired_tasks

# Clear application cache
python manage.py clear_cache

# Create caretaker user
python manage.py create_caretaker_user

# Debug admin tasks
python manage.py debug_admin_tasks

# Reset expired tasks
python manage.py reset_expired_tasks
```

---

## 🌐 API Documentation

The project includes a RESTful API built with Django REST Framework:

- **Base URL (Production):** `https://zoo-management.up.railway.app/api/`
- **Base URL (Local):** `http://127.0.0.1:8000/api/`

### Available Endpoints

- `/api/animals/` - Animal management
- `/api/tasks/` - Task operations
- `/api/events/` - Event management
- `/api/content/` - Content delivery

---

## 🚢 Deployment

This project is configured for deployment on Railway:

1. **Railway Setup**
   - Connect your GitHub repository
   - Add PostgreSQL database
   - Configure environment variables

2. **Environment Variables**
   ```
   SECRET_KEY=<your-secret-key>
   DEBUG=False
   DATABASE_URL=<provided-by-railway>
   CLOUDINARY_CLOUD_NAME=<your-cloudinary-name>
   CLOUDINARY_API_KEY=<your-api-key>
   CLOUDINARY_API_SECRET=<your-api-secret>
   ```

3. **Build Command** (from `build.sh`)
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

4. **Start Command** (from `Procfile`)
   ```
   gunicorn zoo_management.wsgi:application
   ```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available for educational and commercial use.

---

## 👤 Author

**Muskan Haryah**

- GitHub: [@MuskanHaryah](https://github.com/MuskanHaryah)

---

## 🙏 Acknowledgments

- Django Framework and community
- Django REST Framework
- Railway for hosting
- Cloudinary for media management
- All contributors and supporters

---

<div align="center">

**[⬆ Back to Top](#-zoo-management-system)**

Made with ❤️ using Django

</div>

