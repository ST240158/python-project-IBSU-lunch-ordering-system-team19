# IT0206 Assessment 2 — Rubric Mapping and Readiness Review

| Criterion | Weight | Evidence in final project | Status | Readiness |
|---|---:|---|---|---|
| Project Proposal | 5 | `docs/proposal.md` | Present | 🟢 |
| Requirements Analysis | 10 | `docs/srs.md` | Present and mapped to implementation | 🟢 |
| System Design | 10 | ERD/MVC/class diagrams + technical documentation | Present | 🟢 |
| Object-Oriented Programming | 15 | domain classes and supporting service/controller classes; inheritance, abstraction, polymorphism, composition, properties, overriding and dunders | Implemented | 🟢 |
| Database Design & CRUD | 10 | 6 application tables plus lookup/status data; repositories; parameterised SQL; transactions; order delete added | Implemented | 🟢 |
| Python Collections & File Handling | 5 | Lists, tuples, sets, dicts, nested collections, comprehensions; CSV/JSON/TXT | Implemented | 🟢 |
| Testing | 5 | 158 pytest passes in the current environment; coverage should be regenerated before submission; functional tests; UAT form | Mostly complete; UAT signature pending | 🟡 |
| Documentation | 10 | README, installation instructions, user manual, technical docs, diagrams, docstrings | Present | 🟢 |
| GitHub Version Control | 5 | Local finalisation history can be published; original ZIP contained no `.git` history | Historical evidence gap unless an existing team repo is used | 🟡 |
| Presentation & Demonstration | 15 | PPTX + demo script + screenshots | Prepared | 🟢 |
| Professionalism & Code Quality | 10 | Modular MVC, exceptions, logging, parameterised SQL, AI/ethics disclosure | Strong; final GitHub/team evidence still required | 🟡 |

## Minimum-threshold verification

- **Classes:** 41 ≥ 10.
- **Database tables:** 6 ≥ 4.
- **Methods/functions:** well above 25.
- **CRUD:** category, menu-item and order operations implemented.
- **Authentication:** salted PBKDF2 hashed credentials.
- **Roles:** Student and Administrator.
- **Error handling:** custom exceptions and validation.
- **Logging:** application-wide logging configuration.
- **Unit testing:** pytest suite covering models, repositories, services and validation.

## Important submission caveats

1. The supplied ZIP did not contain a Git repository, so original Week 5–11 commit/branch/PR history cannot honestly be recreated. If the team has an existing GitHub repository, use that repository for the final submission.
2. UAT requires a real tester and sign-off; the project provides the record but does not invent a signature.
3. Team-member placeholders in the proposal/README must be replaced before submission.
4. The assessment requires a combined PDF, standalone SQL file, GitHub URL, video demonstration and live presentation. These must be submitted through the LMS as specified by the brief.
