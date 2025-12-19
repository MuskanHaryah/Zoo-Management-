# 🦁 Zoo Management System

A comprehensive Django-based Zoo Management System for managing animals, caretakers, tasks, and visitors efficiently.

---

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Local Development Setup](#-local-development-setup)
- [Deployment on Render](#-deployment-on-render)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)

---

## ✨ Features
- 🔐 User authentication for caretakers and admin
- 🐾 Animal management (CRUD operations)
- 📝 Task assignment and tracking for caretakers
- ⏰ Automated deadline monitoring and task status updates
- 👥 Visitor information pages
- 📊 Admin dashboard for comprehensive management
- ☁️ Cloudinary integration for media files
- 📱 Responsive frontend design

---

## 📁 Project Structure

```
zoo_management/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── runtime.txt                        # Python version for deployment
├── build.sh                          # Build script for Render
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore file
│
├── frontend/                         # Frontend files (organized)
│   ├── static/                       # Static assets
│   │   ├── css/                      # Stylesheets
│   │   │   ├── landing.css
│   │   │   ├── login.css
│   │   │   ├── profile.css
│   │   │   └── visitor.css
│   │   ├── images/                   # Image assets
│   │   ├── landing.js                # Landing page scripts
│   │   ├── profile.js                # Profile page scripts
│   │   └── visitor.js                # Visitor page scripts
│   │
│   └── templates/                    # HTML templates
│       ├── caretaker/                # Caretaker templates
│       │   ├── landing.html
│       │   ├── login.html
│       │   └── profile.html
│       └── visitor/                  # Visitor templates
│           └── visitor.html
│
├── api/                              # Main application
│   ├── models.py                     # Database models
│   ├── views.py                      # View functions
│   ├── urls.py                       # URL routing
│   ├── admin.py                      # Admin configuration
│   ├── signals.py                    # Django signals
│   ├── tests.py                      # Test cases
│   │
│   ├── management/                   # Custom management commands
│   │   └── commands/
│   │       ├── check_expired_tasks.py
│   │       ├── clear_cache.py
│   │       └── ... (other commands)
│   │
│   └── migrations/                   # Database migrations
│
├── zoo_management/                   # Project configuration
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Root URL configuration
│   ├── wsgi.py                       # WSGI configuration
│   └── asgi.py                       # ASGI configuration
│
└── staticfiles/                      # Collected static files (auto-generated)
```

---

## 🔧 Prerequisites

- Python 3.11+
- PostgreSQL 12+
- pip (Python package manager)
- Git

---

## 🚀 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MuskanHaryah/Zoo-Management-.git
cd zoo_management
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory (copy from `.env.example`):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=zoo_management
DB_USER=zoo_admin
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5433

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Set Up PostgreSQL Database
```bash
# Create database
createdb -U postgres zoo_management

# Or using psql
psql -U postgres
CREATE DATABASE zoo_management;
CREATE USER zoo_admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE zoo_management TO zoo_admin;
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files
```bash
python manage.py collectstatic
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit http://localhost:8000 to see the application.

---

## 🌐 Deployment on Render

### Step 1: Prepare Your Repository
1. Ensure all changes are committed to Git
2. Push to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Account
1. Go to [Render.com](https://render.com)
2. Sign up or log in with GitHub

### Step 3: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Fill in details:
   - Name: `zoo-management-db`
   - Region: Choose closest to your users
   - PostgreSQL Version: 16
   - Plan: Free (or paid for production)
3. Click "Create Database"
4. **Save the Internal Database URL** (you'll need this)

### Step 4: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Fill in details:
   - Name: `zoo-management`
   - Region: Same as database
   - Branch: `main`
   - Root Directory: Leave empty if project is in root
   - Runtime: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn zoo_management.wsgi:application`
   - Plan: Free (or paid for production)

### Step 5: Add Environment Variables
In the Render dashboard, go to "Environment" and add:

```
SECRET_KEY=<generate-a-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<paste-internal-database-url-from-step-3>
CLOUDINARY_CLOUD_NAME=<your-cloudinary-name>
CLOUDINARY_API_KEY=<your-cloudinary-key>
CLOUDINARY_API_SECRET=<your-cloudinary-secret>
PYTHON_VERSION=3.11.0
```

### Step 6: Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run `build.sh`
   - Collect static files
   - Run migrations
   - Start the application

### Step 7: Create Admin User (Post-Deployment)
1. Go to Render dashboard → Shell
2. Run:
```bash
python manage.py createsuperuser
```

### Step 8: Access Your Application
- Your app will be live at: `https://zoo-management.onrender.com`
- Admin panel: `https://zoo-management.onrender.com/admin/`

---

## 🔐 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode | No | False |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | Yes | localhost,127.0.0.1 |
| `DATABASE_URL` | PostgreSQL connection URL | Production only | - |
| `DB_NAME` | Database name (local) | Development | zoo_management |
| `DB_USER` | Database user (local) | Development | zoo_admin |
| `DB_PASSWORD` | Database password (local) | Development | admin123 |
| `DB_HOST` | Database host (local) | Development | localhost |
| `DB_PORT` | Database port (local) | Development | 5433 |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes | - |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes | - |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes | - |

---

## 📡 API Endpoints

### Public Routes
- `/` - Landing page
- `/visitor/` - Visitor information page
- `/caretaker/login/` - Caretaker login

### Authenticated Routes (Caretaker)
- `/caretaker/profile/` - Caretaker dashboard
- `/tasks/<id>/` - Task details
- `/tasks/<id>/complete/` - Mark task complete
- `/tasks/rejected/` - View rejected tasks

### Admin Routes
- `/admin/` - Admin dashboard

---

## 🛠️ Management Commands

```bash
# Check for expired tasks
python manage.py check_expired_tasks

# Clear cache
python manage.py clear_cache

# Debug admin tasks
python manage.py debug_admin_tasks
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test api
```

---

## 📝 Notes

- **Static Files**: Managed by WhiteNoise for efficient serving
- **Media Files**: Handled by Cloudinary CDN
- **Database**: PostgreSQL recommended for production
- **Security**: All sensitive data moved to environment variables

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Authors

- **Muskan Haryah** - [GitHub](https://github.com/MuskanHaryah)

---

## 🐛 Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear --no-input
```

### Database connection issues
- Check DATABASE_URL is correct
- Ensure database is running
- Verify credentials

### Deployment fails
- Check build logs in Render
- Verify all environment variables are set
- Ensure `build.sh` has execute permissions

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [Your Email]

---

**Made with ❤️ for Wildlife Conservation**
