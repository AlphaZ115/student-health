# Student Health Tracking System
## Project Report

---

## 1. Project Description

### 1.1 Topic / Application
This project is a **web application with SQLite database integration** designed to support school health management. The system helps store and analyze student health data across multiple periodic health checkups.

### 1.2 Objectives
- Manage student information in schools
- Track health checkups over time
- Identify students with abnormal BMI values
- Provide statistics and analysis to support school administration

### 1.3 Main Features
The application includes the following features:

#### **Student Management**
- Add new students
- View student list
- Edit student information
- Delete students

#### **Health Record Management**
- Each student can have multiple health checkups
- Add health records (height, weight, check date)
- Edit existing health records
- Delete health records
- View complete health history for each student

#### **Health Analysis**
- **BMI Analysis**: Calculate BMI and detect abnormal cases
  - Underweight: BMI < 18.5
  - Overweight: BMI > 25
  - Option to show all records or only latest per student
- **Monthly Statistics**: Track number of checkups per month
  - Optional display of checked students (clickable to view their records)
- **Height Comparison**: Compare average height by class (based on latest records)
- **Weight Comparison**: Compare average weight by class (based on latest records)

---

## 2. Database Description

### 2.1 Number of Tables
The database consists of **2 main tables**:

1. `HocSinh` (Students)
2. `SucKhoe` (Health Records)

---

### 2.2 Table: `HocSinh` (Students)

Stores basic student information.

| Column | Data Type | Description |
|--------|-----------|-------------|
| MaHS | INTEGER | Primary key (Student ID, auto-increment) |
| TenHS | TEXT | Student name |
| Lop | TEXT | Class |
| NgaySinh | TEXT | Birth date |

**Constraints:**
- `MaHS`: PRIMARY KEY, AUTOINCREMENT
- `TenHS`, `Lop`, `NgaySinh`: NOT NULL

---

### 2.3 Table: `SucKhoe` (Health Records)

Stores multiple health checkup records for students.

| Column | Data Type | Description |
|--------|-----------|-------------|
| MaSK | INTEGER | Primary key (Record ID, auto-increment) |
| MaHS | INTEGER | Foreign key linking to student |
| ChieuCao | REAL | Height in meters |
| CanNang | REAL | Weight in kilograms |
| NgayKham | TEXT | Checkup date |

**Constraints:**
- `MaSK`: PRIMARY KEY, AUTOINCREMENT
- `MaHS`: FOREIGN KEY → HocSinh(MaHS)
- `ChieuCao`, `CanNang`, `NgayKham`: NOT NULL

---

### 2.4 Table Relationships

The relationship between the tables is **One-to-Many (1:N)**:

```
HocSinh (1) ←──→ (N) SucKhoe
```

- One student can have multiple health checkup records
- Each health record belongs to exactly one student
- Foreign key constraint: `SucKhoe.MaHS` references `HocSinh.MaHS`

**Relationship Diagram:**
```
┌─────────────────┐         ┌──────────────────┐
│    HocSinh      │         │     SucKhoe      │
├─────────────────┤         ├──────────────────┤
│ MaHS (PK)       │←────────│ MaSK (PK)        │
│ TenHS           │    1:N  │ MaHS (FK)        │
│ Lop             │         │ ChieuCao         │
│ NgaySinh        │         │ CanNang          │
└─────────────────┘         │ NgayKham         │
                            └──────────────────┘
```

---

## 3. Tools and Frameworks

### 3.1 Programming Language
- **Python** (version 3.7+)

### 3.2 Frameworks and Libraries

| Tool / Library | Version | Purpose |
|----------------|---------|---------|
| Flask | 2.x+ | Web framework for backend development |
| SQLite3 | Built-in | Embedded database for data storage |
| Bootstrap | 5.3.0 | Frontend CSS framework for responsive UI design |

#### **Flask**
- **Type:** Micro web framework
- **Usage:** 
  - Route handling (`@app.route`)
  - Template rendering with Jinja2
  - Request/response processing
  - Database connection management

#### **SQLite3**
- **Type:** Serverless, file-based SQL database
- **Usage:**
  - Data persistence in `health.db` file
  - SQL queries for CRUD operations
  - Complex queries with JOINs and aggregations

#### **Bootstrap 5**
- **Type:** Frontend framework
- **Usage:**
  - Responsive layout and grid system
  - Pre-styled components (tables, forms, buttons, cards, alerts)
  - Navigation bar and dropdowns
  - Badge styling for status indicators

### 3.3 Python Modules Used

```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
```

**Core modules:**
- `flask`: Web application framework
- `sqlite3`: Database operations
- `render_template`: Template rendering
- `request`: HTTP request handling
- `redirect`, `url_for`: Navigation and URL management

---

## 4. Installation and Usage

### 4.1 Installation

```bash
# Clone or download the project
cd student-health

# Install Flask
pip install flask

# Run the application
python app.py
```

### 4.2 Access the Application

Open a web browser and navigate to:
```
http://127.0.0.1:5000
```

### 4.3 Quick Start Guide

1. **Add Students:** Click "+ Add Student" button
2. **Add Health Records:** Click "Health Records" for a student, then "+ Add Health Record"
3. **View Analysis:** Use the "Analysis" dropdown menu for various reports

**Detailed usage instructions are available in:**
- English: `usage-en.txt`
- Vietnamese: `usage-vi.txt`

---

## 5. Project Structure

```
student-health/
│
├── app.py                          # Main Flask application
├── schema.sql                      # Database schema
├── health.db                       # SQLite database (auto-generated)
├── README.md                       # This file
├── usage-en.txt                    # English user guide
├── usage-vi.txt                    # Vietnamese user guide
├── .gitignore                      # Git ignore file
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template with navigation
│   ├── students.html               # Student list
│   ├── add_student.html            # Add student form
│   ├── edit_student.html           # Edit student form
│   ├── health_records.html         # Student health records
│   ├── add_health_record.html      # Add health record form
│   ├── edit_health_record.html     # Edit health record form
│   ├── bmi_analysis.html           # BMI analysis page
│   ├── monthly_stats.html          # Monthly statistics
│   ├── height_comparison.html      # Height comparison by class
│   └── weight_comparison.html      # Weight comparison by class
│
└── static/                         # Static files (currently empty)
```

---

## 6. Key Features Implementation

### 6.1 Routes Overview

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home (redirects to students) |
| `/students` | GET | List all students |
| `/students/add` | GET, POST | Add new student |
| `/students/edit/<id>` | GET, POST | Edit student information |
| `/students/delete/<id>` | GET | Delete student |
| `/health/<student_id>` | GET | View student health records |
| `/health/add/<student_id>` | GET, POST | Add health record |
| `/health/edit/<record_id>/<student_id>` | GET, POST | Edit health record |
| `/health/delete/<record_id>/<student_id>` | GET | Delete health record |
| `/analysis/bmi` | GET | BMI analysis page |
| `/analysis/monthly` | GET | Monthly statistics |
| `/analysis/height` | GET | Height comparison by class |
| `/analysis/weight` | GET | Weight comparison by class |

### 6.2 Database Queries

#### Example 1: Find Students with Abnormal BMI (Latest Record Only)
```sql
WITH LatestRecords AS (
    SELECT MaHS, MAX(NgayKham) AS LatestDate
    FROM SucKhoe
    GROUP BY MaHS
)
SELECT HocSinh.MaHS, HocSinh.TenHS, HocSinh.Lop,
       SucKhoe.ChieuCao, SucKhoe.CanNang, SucKhoe.NgayKham,
       (SucKhoe.CanNang / (SucKhoe.ChieuCao * SucKhoe.ChieuCao)) AS BMI
FROM SucKhoe
JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
JOIN LatestRecords ON SucKhoe.MaHS = LatestRecords.MaHS 
                  AND SucKhoe.NgayKham = LatestRecords.LatestDate
WHERE (SucKhoe.CanNang / (SucKhoe.ChieuCao * SucKhoe.ChieuCao)) < 18.5 
   OR (SucKhoe.CanNang / (SucKhoe.ChieuCao * SucKhoe.ChieuCao)) > 25
ORDER BY BMI
```

#### Example 2: Monthly Checkup Statistics with Student Names
```sql
SELECT Thang, SoLan, GROUP_CONCAT(TenHS, ', ') AS Students
FROM (
    SELECT strftime('%Y-%m', SucKhoe.NgayKham) AS Thang,
           COUNT(*) OVER (PARTITION BY strftime('%Y-%m', SucKhoe.NgayKham)) AS SoLan,
           HocSinh.TenHS
    FROM SucKhoe
    JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
    GROUP BY strftime('%Y-%m', SucKhoe.NgayKham), HocSinh.MaHS
)
GROUP BY Thang
ORDER BY Thang DESC
```

#### Example 3: Average Height Comparison by Class
```sql
WITH LatestRecords AS (
    SELECT MaHS, MAX(NgayKham) AS LatestDate
    FROM SucKhoe
    GROUP BY MaHS
)
SELECT Lop,
       AVG(SucKhoe.ChieuCao) AS CaoTB,
       COUNT(DISTINCT HocSinh.MaHS) AS SoHocSinh
FROM SucKhoe
JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
JOIN LatestRecords ON SucKhoe.MaHS = LatestRecords.MaHS 
                  AND SucKhoe.NgayKham = LatestRecords.LatestDate
GROUP BY Lop
ORDER BY Lop
```

---

## 7. Conclusion

The **Student Health Tracking System** provides an effective solution for schools to manage health checkup data, enabling early detection of abnormal cases through BMI analysis and comprehensive statistics.

### 7.1 Achieved Goals
✅ Complete student information management (CRUD operations)  
✅ Health record tracking with multiple entries per student  
✅ BMI calculation and abnormal case detection  
✅ Statistical analysis (monthly, height, weight comparisons)  
✅ User-friendly interface with Bootstrap  
✅ Efficient database design with proper relationships  

### 7.2 Potential Enhancements
- Export reports to PDF/Excel format
- User authentication and role-based access control (teachers, health staff)
- Advanced dashboard with charts and visualizations
- Email notifications for abnormal BMI cases
- Multi-language support
- Data backup and restore functionality

---

## 8. Project Deliverables

📁 **Submission includes:**
- Source code (Flask application)
- SQLite database schema (`schema.sql`)
- Documentation (`README.md`, `usage-en.txt`, `usage-vi.txt`)
- `.gitignore` file for version control

---

**Developed by:** AlphaZ115  
**Repository:** student-health  
**Date:** January 2026
