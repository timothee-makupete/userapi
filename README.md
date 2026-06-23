# User Management API - Django REST Framework

[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-MariaDB-orange)](https://mariadb.org/)

##  Project Overview

A RESTful API for managing users with external data integration, filtering, and secure authentication.


##  Tech Stack

| Technology | Version |
|------------|---------|
| Django | 5.0.3 |
| Django REST Framework | 3.14.0 |
| MySQL/MariaDB | 10.4+ |
| django-filter | 24.2 |
| requests | 2.31.0 |
| python-dotenv | 1.0.1 |
|drf-spectacular |0.29.0 |

##  Installation

### Prerequisites
- Python 3.10 or higher
- XAMPP (MySQL/MariaDB) or any MySQL server
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/timothee-makupete/userapi.git
cd userapi
```

### Step 2: Create Virtual Environment
If `venv` is not available, install `virtualenv` first:
```bash
pip install virtualenv
```

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
py -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
Start MySQL (XAMPP):
- Open XAMPP Control Panel
- Click "Start" next to MySQL

Create database:
```sql
CREATE DATABASE user_db;
```

### Step 5: Environment Variables
Copy the example file to `.env` and update values as needed:
```bash
cp .env.example .env
```
For Windows PowerShell:
```powershell
Copy-Item .env.example .env
```

Create or edit `.env` in the project root:
```env
DB_NAME=user_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

API_USER=admin
API_PASSWORD=SecurePass123!

EXTERNAL_API_URL=https://jsonplaceholder.typicode.com/users
SECRET_KEY=django-insecure-your-secret-key-here
```

### Step 6: Run Migrations
```bash
py manage.py makemigrations users
py manage.py migrate
```

### Step 7: Create Superuser
```bash
py manage.py createsuperuser
# Username: admin
# Password: SecurePass123!
```

### Step 8: Run Server
```bash
py manage.py runserver
```
Server running at: http://127.0.0.1:8000/

##  API Endpoints

All endpoints require HTTP Basic Authentication.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/import/ | Import users from external API |
| GET | /api/users/ | List all users (supports filters) |
| GET | /api/users/{id}/ | Get single user by ID |
| DELETE | /api/users/{id}/delete/ | Delete user by ID |

### Filter Parameters (GET /api/users/)

| Parameter | Example | Description |
|-----------|---------|-------------|
| city | ?city=Gwenborough | Filter by city (case-insensitive) |
| company | ?company=Romaguera | Filter by company name (case-insensitive) |
| name | ?name=Leanne | Filter by user name (case-insensitive) |

Combine filters: `/api/users/?city=Gwenborough&company=Romaguera`

##  Swagger UI

The API documentation is available at: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

![Swagger UI - API Summary](swagger_screenshoots/Screenshot%20(62).png)

![Swagger UI - Authorization Dialog](swagger_screenshoots/Screenshot%20(63).png)

##  Testing the API

### Using cURL
```bash
# Set variables
USERNAME="admin"
PASSWORD="SecurePass123!"
BASE_URL="http://127.0.0.1:8000/api"

# 1. Import users
curl -X POST $BASE_URL/import/ -u $USERNAME:$PASSWORD

# 2. Get all users
curl -u $USERNAME:$PASSWORD $BASE_URL/users/

# 3. Filter by city
curl -u $USERNAME:$PASSWORD "$BASE_URL/users/?city=Gwenborough"

# 4. Filter by company
curl -u $USERNAME:$PASSWORD "$BASE_URL/users/?company=Romaguera"

# 5. Filter by name
curl -u $USERNAME:$PASSWORD "$BASE_URL/users/?name=Leanne"

# 6. Get single user
curl -u $USERNAME:$PASSWORD $BASE_URL/users/1/

# 7. Delete user
curl -X DELETE -u $USERNAME:$PASSWORD $BASE_URL/users/1/delete/
```

### Using Python
```python
import requests
from base64 import b64encode

BASE_URL = "http://127.0.0.1:8000/api"
credentials = b64encode(b"admin:SecurePass123!").decode()
headers = {"Authorization": f"Basic {credentials}"}

# Import users
response = requests.post(f"{BASE_URL}/import/", headers=headers)
print(response.json())

# Get users with filter
response = requests.get(f"{BASE_URL}/users/?city=Gwenborough", headers=headers)
print(response.json())
```

##  AI Usage

Per test requirements, AI was used for:
- API endpoints - DRF view generation
- Filtering implementation - django-filter integration
- Documentation - README and code comments

Adapted from AI output:
- Manual filtering backup logic
- Enhanced error handling messages

No AI used for:
- Initial project structure - Django configuration setup
- Security implementation (manual configuration)
- Database design - Normalized schema suggestion
- Data transformation logic (custom mapping)
- Environment-based credential management
- Testing approach
