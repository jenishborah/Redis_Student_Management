# Redis-Based Student Management System

A **menu-driven Student Management System** developed using **Python** with **Redis (NoSQL Database)** as the backend.  
The system manages student academic records, performs CRUD operations, calculates total marks automatically, and assigns grades based on predefined academic criteria.

This project demonstrates database integration, input validation, automated grading logic, and structured data visualization using Python and Redis.

---

## Features

Redis database integration (NoSQL, in-memory storage)  
Full CRUD operations:
- Add Student  
- View Student  
- Update Marks  
- Delete Student  
- List All Students  

Automatic total marks calculation  
Automatic grade assignment  
Input validation for marks and student data  
Tabular output display  
Logging support for error tracking  


---

## Assessment Components

| Component | Maximum Marks |
|----------|---------------|
| Sessional Test-1 | 10 |
| Mid-Term | 30 |
| Sessional Test-2 | 10 |
| End-Semester | 40 |
| **Total** | **100** |

---

## Grading Policy

| Total Marks | Grade |
|------------|------|
| 95–100 | O |
| 85–94 | A+ |
| 75–84 | A |
| 65–74 | B+ |
| 55–64 | B |
| 45–54 | P |
| Below 45 | F |

Grades are calculated automatically whenever marks are entered or updated.

---

## Technologies Used

- **Python** – Core programming language  
- **Redis** – NoSQL in-memory database  
- **redis-py** – Python Redis client library  
- **Tabulate** – Table formatting library  
- **Git & GitHub** – Version control and project hosting  

---


---

##  Installation & Setup

### Clone Repository

```bash
git clone https://github.com/jenishborah/Redis_Student_Management-.git
cd Redis_Student_Management-
```
### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### Install Dependencies

```bash
pip install -r requirements.txt
```
### Install & Start Redis Server (Linux/WSL)

```bash
sudo apt install redis-server
sudo service redis-server start
```

```bash
# Check Redis connection:
redis-cli ping
```
### Run the Application

```bash
python main.py
```
### For Gui

```bash
python gui_main.py
```

