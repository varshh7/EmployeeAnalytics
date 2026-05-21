# 🗄️ Employee Analytics System — Phase 2

> An interactive Python CLI application for real-time employee analytics using Oracle 21c XE database.

---

## 🎯 Analytics Tasks (4 Operations)

| # | Task | Description |
|---|------|-------------|
| 1 | **Fetch All Employees** | Retrieves all employee records ordered by ID |
| 2 | **Filter by Salary** | Filters employees above a minimum salary threshold |
| 3 | **Department Summary** | Headcount + average salary per department (JOIN) |
| 4 | **Recent Hires** | Employees hired within a user-defined number of days |

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/varshh7/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

### 2. Install Dependencies
```bash
pip install oracledb python-dotenv
```

### 3. Create `.env` File
```env
DB_USER=SYSTEM
DB_PASSWORD=your_oracle_password
DB_DSN=localhost:1521/xe
```

### 4. Set Up Oracle Database
Run this in **SQL Developer** or **SQLcl**:
```sql
DROP TABLE employees CASCADE CONSTRAINTS;
DROP TABLE departments CASCADE CONSTRAINTS;

CREATE TABLE departments (
    department_id   NUMBER PRIMARY KEY,
    department_name VARCHAR2(50) NOT NULL
);

CREATE TABLE employees (
    employee_id   NUMBER PRIMARY KEY,
    first_name    VARCHAR2(50),
    last_name     VARCHAR2(50) NOT NULL,
    salary        NUMBER(8,2),
    hire_date     DATE,
    department_id NUMBER,
    CONSTRAINT fk_dept FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

INSERT INTO departments VALUES (10, 'Engineering');
INSERT INTO departments VALUES (20, 'Sales');
INSERT INTO departments VALUES (30, 'HR');

INSERT INTO employees VALUES (101, 'John',  'Doe',     6000, SYSDATE - 100, 10);
INSERT INTO employees VALUES (102, 'Jane',  'Smith',   8000, SYSDATE - 400, 10);
INSERT INTO employees VALUES (103, 'Alice', 'Johnson', 4500, SYSDATE - 50,  20);
INSERT INTO employees VALUES (104, 'Bob',   'Brown',   5500, SYSDATE - 800, 30);

COMMIT;
```

### 5. Run the App
```bash
python app.py
```

---

## 💻 Sample Output

```
Welcome to the Employee Analytics System

Select an option:
1. Fetch All Employees
2. Filter Employees by Salary
3. View Department Summary Report
4. View Recent Hires Report
5. Exit

Enter your choice (1-5):
```

```
--- ALL EMPLOYEES ---
--------------------------------------------------
EMPLOYEE_ID | FIRST_NAME | LAST_NAME | SALARY
--------------------------------------------------
101         | John       | Doe       | 6000
102         | Jane       | Smith     | 8000
103         | Alice      | Johnson   | 4500
104         | Bob        | Brown     | 5500
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Oracle](https://img.shields.io/badge/Oracle-21c%20XE-red?logo=oracle)
![oracledb](https://img.shields.io/badge/oracledb-Thin%20Mode-orange)

| Technology | Purpose |
|---|---|
| Python 3.11 | Core language |
| oracledb (Thin Mode) | Oracle DB driver — no Instant Client needed |
| python-dotenv | Secure credential management |
| Oracle 21c XE | Local database engine |
| SQL (DDL + DML) | Schema setup and queries |

---

## ⚠️ Troubleshooting

| Error | Fix |
|---|---|
| `ORA-00942` Table not found | Run the SQL setup script in SQL Developer first |
| Connection Error | Start Oracle XE: `net start OracleServiceXE` (Windows) |
| Module Not Found | Run `pip install oracledb python-dotenv` |

---
