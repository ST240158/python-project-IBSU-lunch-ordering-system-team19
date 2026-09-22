# Prompt Alignment Review — IBSU Lunch Ordering System

**Reviewed:** 15 September 2026  
**Basis:** `IBSU_Lunch_Ordering_System_Prompt_Plan (1).md` and the implementation in this project.

## Result
The implementation has been corrected to follow the prompt's IBSU-specific specification rather than the generic Restaurant Ordering System template. The prompt explicitly requires MVC, two roles, SQLite/MySQL, CSV/JSON handling, pytest, pandas/matplotlib/tabulate, and excludes GUI/web/mobile/payment/delivery/supplier functionality. fileciteturn0file0L3-L25

## Changes made
| Area | Previous implementation | Corrected implementation |
|---|---|---|
| Main menu | Login + public registrations | Exactly Student Login, Administrator Login, Exit |
| Student menu | Browse/place/view/profile | View Menu, Search Food, Place Order, View My Orders, Cancel Order, Logout |
| Administrator menu | 10-item expanded menu | Exact 8-item prompt menu; advanced functions are available through subflows |
| Order statuses | Pending, Confirmed, Preparing, Ready, Completed, Cancelled | Exactly `received`, `preparing`, `ready`, `collected` |
| Cancellation | Cancelled status | Eligible `received` order is removed transactionally and stock is restored; this avoids inventing a fifth status |
| Passwords | Unsalted SHA-256 | Salted PBKDF2-HMAC-SHA256 with 310,000 iterations and per-password salt |
| HTTP feature | Motivational quote API using `requests` | Removed because it is unrelated to the required IBSU system |
| Database | SQLite only | SQLite default + MySQL connector/backend support |
| Configuration | Python constants | `config.json` selects backend and report output settings |
| Reporting | Included inventory dataframe and HTTP quote feature | Required sales/popularity/category/status reporting only |
| Testing | One stale hard-coded date test | Date test uses current date; all tests pass |
| Domain naming | `Student` class | `StudentCustomer` class added, with `Student` compatibility alias; `student_id` and `admin_id` properties added |

## Verification
- `pytest -q`: **158 passed, 0 failed**.
- Clean console startup with `python -m src.main`: **PASS**.
- Main menu now matches the prompt's exact three options.
- Parameterized SQL remains in repository operations.
- CSV/JSON file handling remains available.
- pandas/matplotlib/tabulate reporting remains available.
- No payment, supplier, GUI, web, mobile or delivery functionality was added.

## Remaining submission work
1. Regenerate the existing PDF/PPTX/DOCX assessment artifacts so their text/screenshots match the corrected four-status workflow and exact menus.
2. Replace team-member placeholders before submission.
3. Obtain genuine UAT sign-off.
4. Publish to the team's real GitHub repository; do not fabricate historical commits or pull requests.
5. Regenerate coverage/test-report figures immediately before submission.
