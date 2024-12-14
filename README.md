# Library Management APIs

## Overview
The **Library Management API** is a RESTful web service designed to manage library operations, including borrowing and returning books. It allows library staff and members to track loans, manage available copies, calculate overdue fines, and maintain a seamless workflow for library transactions.

---

## Features

- **Member Management**: Add, update, and manage library members.
- **Book Management**: Manage book inventory, including tracking available copies.
- **Loan Management**: Record loans when members borrow books.
- **Return Handling**: Process book returns, calculate overdue fines, and update book availability.
- **Overdue Fine Calculation**: Automatically calculate fines based on the due date and return date.
- **Authentication**: Secure access using JWT authentication.

---

## Tech Stack

- **Backend Framework**: Django 5.1.4
- **API Framework**: Django REST Framework (DRF) 3.15.2
- **Authentication**: Simple JWT
- **Database**: PostgreSQL (using `psycopg2-binary`)
- **Environment Management**: Python Dotenv

---

## Installation and Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- PostgreSQL

### Clone the Repository
```bash
$ git clone https://github.com/your-username/library-management-api.git
$ cd library-management-api
```

### Create and Activate a Virtual Environment
- **For Windows**:
```bash
$ python -m venv venv
$ .\venv\Scripts\activate
```

- **For macOS/Linux**:
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

### Install Dependencies
```bash
$ pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file in the root directory and configure the following variables:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Apply Migrations
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Run the Development Server
```bash
$ python manage.py runserver
```

---

## Endpoints

### Authentication
| Endpoint                | Method | Description               |
|-------------------------|--------|---------------------------|
| `/api/token/`           | POST   | Obtain JWT token          |
| `/api/token/refresh/`   | POST   | Refresh JWT token         |

### Member Management
| Endpoint                | Method | Description               |
|-------------------------|--------|---------------------------|
| `/api/members/`         | GET    | List all members          |
| `/api/members/`         | POST   | Add a new member          |
| `/api/members/<id>/`    | PATCH  | Update member details     |
| `/api/members/<id>/`    | DELETE | Remove a member           |

### Book Management
| Endpoint                | Method | Description               |
|-------------------------|--------|---------------------------|
| `/api/books/`           | GET    | List all books            |
| `/api/books/`           | POST   | Add a new book            |
| `/api/books/<id>/`      | PATCH  | Update book details       |
| `/api/books/<id>/`      | DELETE | Remove a book             |

### Loan Management
| Endpoint                | Method | Description               |
|-------------------------|--------|---------------------------|
| `/api/loans/`           | GET    | List all loans            |
| `/api/loans/`           | POST   | Create a loan (borrow a book) |
| `/api/loans/<id>/`      | PATCH  | Update loan details       |
| `/api/loans/return/`    | POST   | Return a book and calculate overdue fines |


---

## Acknowledgments
- Django and Django REST Framework communities for their powerful tools and excellent documentation.
- The requirement document for guiding the project structure and functionality.

