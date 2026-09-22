# IBSU Lunch Ordering System — Installation Guide

## 1. Prerequisites

- Python 3.11 or newer.
- pip.
- Git (for source-control publishing).
- A terminal such as PowerShell/Command Prompt on Windows.

## 2. Get the Source

Clone the team's GitHub repository or extract the final project bundle.

```bash
git clone https://github.com/<USERNAME>/<REPOSITORY>.git
cd <REPOSITORY>
```

## 3. Create a Virtual Environment

Windows PowerShell/Command Prompt:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5. Start the Application

From the project root:

```bash
python -m src.main
```

The application creates `database/ibsu_lunch.db` and seeds demo data when the relevant tables are empty.

## 6. Demo Credentials

- Administrator: `admin` / `admin123`
- Student: `student` / `student123`

## 7. Run Tests

```bash
python -m pytest -q
```

Expected final result at the time this package was prepared:

```text
160 passed
0 failed
```

## 8. Run Core Coverage

```bash
python -m pytest -q --cov=src.models --cov=src.repositories --cov=src.services --cov=src.utils --cov=src.exceptions --cov-report=term-missing
```

The prepared version achieved 81% coverage across the core models, repositories, services, utilities and exceptions.

## 9. Rebuild from SQL

The standalone script is:

```text
database/schema.sql
```

It can reproduce the six application tables and seed demonstration data.

## 10. Troubleshooting

- If `ModuleNotFoundError` occurs, confirm the terminal's current directory is the project root and use `python -m src.main`.
- If dependencies are missing, activate `.venv` and reinstall requirements.
- If the database becomes corrupted during experimentation, stop the application, remove `database/ibsu_lunch.db`, and restart.
- The application does not require Internet access for core functionality.
