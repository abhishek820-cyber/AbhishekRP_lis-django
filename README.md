# Laboratory Information System (LIS)

A web-based Laboratory Information System built with Django 6, Django REST Framework, and SQLite.

## Features

- **5 Role-based user types**: Admin, Physician, Nurse, Phlebotomist, Lab Technician
- **Patient Registration** with auto-generated MRN (PAT-XXXXXX)
- **Lab Order Entry** with multi-test selection
- **Sample Collection Worklist** for Phlebotomists
- **Result Entry Worklist** for Lab Technicians
- **Clinical Report View** with flag indicators (H/L/CR/N)
- **JWT Authentication** via djangorestframework-simplejwt
- **REST API** with full CRUD on all modules
- **Print-ready Lab Reports**

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Django 6.0, Python 3.13           |
| API        | Django REST Framework 3.x         |
| Auth       | JWT (djangorestframework-simplejwt)|
| Database   | SQLite3                           |
| Frontend   | Bootstrap 5.3, Bootstrap Icons    |

## Project Structure

AbhishekRP_lis-django/
├── accounts/      # User management, JWT auth, role permissions
├── patients/      # Patient registration and search
├── labtests/      # Test menus and assay catalogue
├── orders/        # Order entry, sample collection workflow
├── results/       # Result entry and lab report generation
├── templates/     # HTML templates (Bootstrap 5)
├── lab_project/   # Django settings and root URLs
└── manage.py

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AbhishekRP_lis-django.git
cd AbhishekRP_lis-django
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```

### 6. Create Admin profile
Go to `http://127.0.0.1:8000/admin/` → User masters → Add:
- Auth user: your superuser
- Employee ID: EMP-001
- Role: Admin
- Designation: System Administrator

### 7. Run the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login/` | Get JWT tokens |
| POST | `/api/v1/auth/logout/` | Blacklist token |
| GET/POST | `/api/v1/patients/` | List / Register patients |
| GET/POST | `/api/v1/orders/` | List / Place orders |
| PATCH | `/api/v1/orders/{id}/collect/` | Mark sample collected |
| PATCH | `/api/v1/orders/{id}/receive/` | Mark sample In-Lab |
| POST | `/api/v1/orders/{id}/results/` | Enter results |
| GET | `/api/v1/orders/{id}/report/` | Get lab report |
| GET/POST | `/api/v1/tests/assays/` | List / Add assays |
| GET/POST | `/api/v1/users/` | List / Add staff users |

## User Roles & Access

| Role | Patient Reg | Order Entry | Sample Collection | Result Entry | View Report |
|------|-------------|-------------|-------------------|--------------|-------------|
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |
| Physician | ✅ | ✅ | ❌ | ❌ | ✅ |
| Nurse | ✅ | ✅ | ❌ | ❌ | ✅ |
| Phlebotomist | ❌ | ❌ | ✅ | ❌ | ❌ |
| Lab Technician | ❌ | ❌ | ❌ | ✅ | ❌ |

## Screenshots

See the `/screenshots/` folder.