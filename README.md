# Complaint Management System 📋

A complete full-stack web application built using **Python Flask**, **SQLite**, **SQLAlchemy ORM**, **HTML5**, **CSS3**, **JavaScript**, and **Bootstrap 5**. Designed specifically for educational institutions, corporate offices, and organization grievance redressal workflows.

---

## 🌟 Key Features

### 1. Authentication & Security
- **User Registration & Login**: Account creation with email verification & password hashing.
- **Admin Portal**: Dedicated administrator access portal.
- **Password Hashing**: Cryptographic password hashing using Werkzeug.
- **Session Management**: Session-based authorization decorators (`@login_required`, `@admin_required`).

### 2. User Portal
- **Dashboard Overview**: Metrics for Total, Pending, In Progress, and Resolved complaints.
- **Submit New Complaint**: Form with Title, Description, Category selection, Priority levels (Low, Medium, High), and auto-generated Ticket IDs (e.g. `CMP-2026-0001`).
- **Track Complaint Status**: Live ticket tracking table with status badges (**Pending**, **In Progress**, **Resolved**, **Rejected**), priority pills, search bar, and admin remarks.
- **Profile Management**: View and edit name, mobile contact details, and password.

### 3. Admin Command Center & Analytics
- **System Metrics**: Total complaints count, pending reviews, active investigations, resolved issues, rejected requests, and total user accounts.
- **Interactive Analytics**: Visual charts powered by **Chart.js** displaying Status Breakdown (Doughnut), Category-wise Complaints (Bar), and Priority Distribution (Pie).
- **Manage Complaints**: Review tickets, search & filter by category/status/priority, update status, append admin resolution notes, and delete invalid complaints.
- **User Management**: Search user directory, view complaint counts per user, and manage user accounts.

---

## 🛠️ Technology Stack

- **Backend Framework**: Python 3 & Flask Framework
- **Database**: SQLite 3 with SQLAlchemy ORM
- **Security**: Werkzeug Security (`generate_password_hash`, `check_password_hash`)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, FontAwesome 6
- **Data Analytics**: Chart.js

---

## 📁 Project Structure

```text
Complaint_Management_System/
│
├── app.py                      # Core Flask controller & application routes
├── config.py                   # App configuration & database connection URI
├── requirements.txt            # Dependencies (Flask, Flask-SQLAlchemy, Werkzeug)
├── seed.py                     # Initial database seeding script
├── README.md                   # Project documentation
│
├── models/
│   ├── __init__.py
│   └── models.py               # Database schemas (User, Admin, Complaint)
│
├── templates/                  # Bootstrap 5 HTML Jinja2 Templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── user_dashboard.html
│   ├── add_complaint.html
│   ├── my_complaints.html
│   ├── profile.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── manage_complaints.html
│   └── manage_users.html
│
└── static/
    ├── css/
    │   └── style.css           # Custom styling & theme variables
    └── js/
        └── script.js           # Chart.js integration & client-side scripts
```

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/keerthanajagadish29-dotcom/complaint-system.git
   cd complaint-system
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access in browser**:
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔑 Demo Credentials

| Role | Username / Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full admin dashboard, status updates, chart analytics |
| **Sample User 1** | `rahul@gmail.com` | `user123` | User portal, lodging & tracking complaints |
| **Sample User 2** | `priya@gmail.com` | `user123` | User portal & profile management |

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
