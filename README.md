# Trekking Management System

A role-based web application developed using **Flask**, **SQLite**, **SQLAlchemy**, **Jinja2**, and **Bootstrap** to manage trekking activities efficiently.

The system provides separate dashboards for **Admin**, **Staff**, and **Trekkers**, allowing complete management of trekking events, bookings, staff assignments, participant records, and user profiles through a secure authentication system.

---

# Project Overview

The Trekking Management System simplifies the process of organizing and managing trekking events. It enables administrators to manage treks and staff members, staff to supervise assigned treks and participants, and trekkers to browse, book, and track their trekking history.

The application follows a modular Flask architecture using Blueprints and role-based access control.

---

#  Features

##  Admin

- Secure Admin Login
- Dashboard with project statistics
- Approve or deactivate staff members
- Manage registered trekkers
- Blacklist / Unblacklist trekkers
- Create new treks
- Edit trek details
- Delete treks (when no bookings exist)
- Assign staff to treks
- Prevent overlapping staff assignments
- Manage trek slots
- Search staff, trekkers, and treks
- View all booking records

---

##  Staff

- Secure Login
- Personal Dashboard
- View assigned treks
- View trek details
- View all trek participants
- Update trek status
- Update available slots
- Manage personal profile
- Edit profile information

---

## Trekker

- Register and Login
- Browse available treks
- Search treks by name
- Filter treks by difficulty
- Filter treks by location
- View detailed trek information
- Book available treks
- Prevent duplicate bookings
- Cancel bookings
- View complete booking history
- Manage personal profile
- Edit profile

---

# Additional Features

- Role-Based Authentication
- Password Hashing using Werkzeug
- Session Management
- Staff Approval Workflow
- Trek Slot Management
- Booking History
- Trek Status Tracking
- Booking Status Tracking
- Trek Detail View
- Responsive Bootstrap UI
- Search and Filtering
- Staff Date Conflict Validation
- Prevention of Overbooking

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Flask | Backend web framework |
| SQLAlchemy | ORM for SQLite database |
| SQLite | Database |
| Jinja2 | Dynamic HTML rendering |
| Bootstrap 5 | Responsive frontend |
| HTML5 | Page structure |
| CSS3 | Styling |
| Werkzeug | Password hashing |
| Flask Blueprints | Modular routing |
| Git & GitHub | Version control |

---

# Project Structure

```
Trekking-Management-System
│
├── app.py
├── models.py
├── create_db.py
├── requirements.txt
├── README.md
│
├── routes
│   ├── auth.py
│   ├── admin.py
│   ├── staff.py
│   └── user.py
│
├── templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── staff_dashboard.html
│   ├── user_dashboard.html
│   ├── manage_staff.html
│   ├── manage_treks.html
│   ├── manage_trekkers.html
│   ├── browse_treks.html
│   ├── my_bookings.html
│   ├── trek_details.html
│   ├── profile.html
│   └── ...
│
├── static
│
├── instance
│   └── trekking.db
│
└── venv
```

---

# Database Schema

The project consists of five database tables.

## Admin

Stores administrator credentials.

**Fields**

- admin_id
- email
- hash_password

---

## Staff

Stores trekking staff information.

**Fields**

- staff_id
- name
- email
- phone
- hash_password
- status

Status values

- Pending
- Approved
- Deactivated

---

## Trekker

Stores registered trekkers.

**Fields**

- trekker_id
- name
- email
- phone
- hash_password
- is_blacklisted

---

## Trek

Stores trekking event information.

**Fields**

- trek_id
- name
- location
- difficulty
- duration
- available_slots
- status
- start_date
- end_date
- staff_id

Status values

- Open
- Ongoing
- Completed

---

## Booking

Stores trekking booking records.

**Fields**

- booking_id
- trekker_id
- trek_id
- booking_date
- status

Booking Status

- Booked
- Cancelled
- Completed

---

# Database Relationships

- One Staff → Many Treks
- One Trek → Many Bookings
- One Trekker → Many Bookings

---

# How to Run the Project

## 1. Clone Repository

```bash
git clone https://github.com/24f1002360/mad1-trekking-management-app.git
cd mad1-trekking-management-app
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Database

```bash
python create_db.py
```

---

## 5. Run the Application

```bash
python app.py
```

The application will be available at

```
http://127.0.0.1:5000
```
---

# Application Workflow

```
Staff Registers
        │
        ▼
Admin Approves Staff
        │
        ▼
Admin Creates Trek
        │
        ▼
Admin Assigns Staff
        │
        ▼
Trekker Registers
        │
        ▼
Trekker Browses Treks
        │
        ▼
Trekker Books Trek
        │
        ▼
Staff Manages Assigned Trek
        │
        ▼
Trekker Views Booking History
```

---
