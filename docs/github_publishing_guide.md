# GitHub Publishing Guide — IT0206 Assessment 2

## 1. Repository Name

Use the assessment convention:

```text
python-project-restaurant-team<TeamID>
```

Example:

```text
python-project-restaurant-team12
```

## 2. Before Publishing

Run:

```bash
python -m compileall -q src tests
python -m pytest -q
python -m pytest -q --cov=src.models --cov=src.repositories --cov=src.services --cov=src.utils --cov=src.exceptions --cov-report=term-missing
```

Expected final test result:

```text
160 passed
0 failed
```

Review `.gitignore` and ensure no `.venv`, cache files, private secrets or unnecessary runtime artifacts are committed.

## 3. Git Setup

If the team has an existing GitHub repository with historical assessment work, use it instead of starting a new history.

For a new final repository:

```bash
git init
git branch -M main
git add .
git commit -m "Prepare final assessment release"
git remote add origin https://github.com/<USERNAME>/<REPOSITORY>.git
git push -u origin main
```

## 4. Recommended Feature-Branch Workflow

For future changes, use branches such as:

```text
feature/authentication
feature/menu-management
feature/order-workflow
feature/reporting
feature/testing
feature/documentation
```

Push a branch:

```bash
git checkout -b feature/reporting
git add .
git commit -m "Add reporting and analytics"
git push -u origin feature/reporting
```

Create a genuine GitHub Pull Request, obtain review, then merge it into `main`. Do not fabricate pull requests or historical contributions.

## 5. Final Main Branch Requirement

Before submission, verify that `main` launches successfully:

```bash
python -m src.main
```

The assessment brief requires the main/master branch to contain a working, buildable version at submission time.

## 6. README First View

The first part of `README.md` should clearly show:
- Project title.
- All team members and IDs.
- Project description.
- Setup/install commands.
- Run command.
- Test command.
- Repository structure.

## 7. Final GitHub Check

```bash
git status
git log --oneline --decorate --graph -20
git branch -a
```

Then open the GitHub repository in a browser and verify that the README, source code, SQL script, tests and documentation are visible.
