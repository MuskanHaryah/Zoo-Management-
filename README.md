# 🦁 Zoo Management System (Django Web App)

A full-stack **Django-based web application** for managing animals, staff, and visitors in a zoo.  
This project demonstrates Django’s **Model-View-Template (MVT)** architecture, database handling, static file management, and makes use of the **Django Admin Panel** for backend administration.

---

## ✨ Features
- 🐅 **Animal Management**: Add, update, and delete animal records  
- 👩‍💼 **Staff Management**: Manage staff profiles, roles, and responsibilities  
- 🎟️ **Visitor Management**: Track visitors, ticket bookings, and activities  
- 📊 **Reports**: Generate insights about animals, staff, and visitors  
- 🎨 **Frontend**: Styled pages using HTML, CSS, and JavaScript  
- 🔑 **Admin Panel**: Fully functional Django **built-in admin dashboard** for easy database management  

---

## 🚀 Getting Started

### ✅ Prerequisites
Make sure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)
- PostgreSQL 

---

### 🔧 Installation & Setup

1. **Clone the repository**  
   `git clone https://github.com/MuskanHaryah/Zoo-Management-.git`  
   `cd Zoo-Management-`

2. **Create & activate virtual environment**  
   - Windows:  
     `python -m venv venv`  
     `venv\Scripts\activate`  
   - Linux/Mac:  
     `python -m venv venv`  
     `source venv/bin/activate`

3. **Install dependencies**  
   `pip install -r requirements.txt`

4. **Apply migrations**  
   `python manage.py migrate`

5. **Create superuser (for Django Admin access)**  
   `python manage.py createsuperuser`

6. **Run development server**  
   `python manage.py runserver`

7. **Open in browser**  
   - Main site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) 
   
