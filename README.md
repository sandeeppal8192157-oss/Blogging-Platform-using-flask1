# Full-Stack Flask Blogging Platform

A secure, data-driven web application built using the Flask framework. This platform was developed systematically over a 7-week engineering track, progressing from a basic structure to a production-ready application featuring user authentication, complete CRUD mechanics, relational commenting systems, and case-insensitive global search.

---

## 🏗️ System Architecture & How We Built It

The application follows the **Model-View-Controller (MVC)** pattern split across logical components using Flask Blueprints:
* **Models (`models.py`):** Flask-SQLAlchemy structures mapping our relational database tables using object-relational mapping.
* **Views/Templates (`templates/`):** Dynamic HTML interfaces powered by the Jinja2 rendering engine and styled with Bootstrap.
* **Controllers/Routes (`routes.py`):** The core backend business logic, session handling, and application workflows.

---

## 🚀 Step-by-Step Feature Implementation Reference

### 1. Flask Setup & Application Factory (Week 1)
* **Modular Design:** Configured the application using the factory pattern (`create_app()`) to make configuration switches seamless between development, testing, and production environments.

### 2. User Authentication & Security (Week 2)
* **Session Management:** Integrated **Flask-Login** to handle secure user sessions, tracking cookies, and protecting sensitive routes via `@login_required`.
* **Password Hashing:** Implemented industrial-grade security helpers from **Werkzeug** using `pbkdf2:sha256` encryption to ensure user passwords are never stored in plain text.

### 3. Core Blog CRUD Operations (Week 3)
* **Data Control:** Configured explicit database entries for creating, reading, updating, and deleting blog posts.
* **Route Protection:** Added server-side security evaluations (`abort(403)`) to halt unauthorized requests if a user attempts to edit or delete a post they did not author.

### 4. User Profiles & Database Pagination (Week 4)
* **Custom Timelines:** Developed a dynamic routing system (`/user/<username>`) querying isolated author timelines.
* **Query Scaling:** Integrated Flask-SQLAlchemy's `.paginate()` system to restrict the homepage timeline layout to **2 posts per page** to prevent query performance drops.

### 5. Relational Commenting System (Week 5)
* **Relational Mapping:** Designed a `Comment` model linked concurrently through strict Foreign Key constraints to both a target `User` (the author) and a specific `Post` (the parent article).
* **Cascade Deletes:** Enabled cascading rules (`cascade="all, delete-orphan"`) so if a user deletes a blog post, its attached comments are scrubbed out automatically, maintaining database health.

### 6. Global Full-Text Search (Week 6)
* **Case-Insensitive Queries:** Deployed multi-column search filtration across post titles, bodies, and author names simultaneously using the SQL `.ilike()` operator.

### 7. Automated Testing & WSGI Deployment (Week 7)
* **Isolated Verification:** Developed a standalone `tests.py` using Python's `unittest` suite that targets an ephemeral, in-memory database (`sqlite:///:memory:`) to validate routing behaviors without altering live records.
* **Production Gateway:** Formulated a standardized `wsgi.py` entry point necessary for running high-concurrency production servers like Gunicorn.

---

## 📊 Relational Database Schema

The database utilizes three main tables connected via one-to-many relationships:

* **`User` Table:** Holds user accounts (`id`, `username`, `email`, `password`). Linked to `Post` and `Comment`.
* **`Post` Table:** Holds articles (`id`, `title`, `content`, `date_posted`, `user_id`). Linked to `Comment`.
* **`Comment` Table:** Holds feedback (`id`, `content`, `date_posted`, `user_id`, `post_id`).

---

## 💻 Local Installation & Setup Guide

### 1. Clone the Codebase
```bash
git clone [https://github.com/yourusername/flask-blog-platform.git](https://github.com/yourusername/flask-blog-platform.git)
cd "Blogging Platform using flask"# 🚀 Full-Stack Flask Blogging Platform

A secure, data-driven, and interactive web application engineered using the **Python Flask** framework. This platform was built systematically over an 8-week development cycle, moving from basic routing to a robust architecture featuring cryptographic user authentication, a relational commenting system, full-text global search, and automated test-driven quality assurance.

---

## 🏗️ System Architecture Overview

The platform is designed around a modular **Model-View-Controller (MVC)** architectural pattern using **Flask Blueprints**:
* **Models (`app/models.py`):** Defines the database structure using Flask-SQLAlchemy Object-Relational Mapping (ORM).
* **Views (`app/templates/`):** Dynamic frontend user interfaces rendered using the Jinja2 template engine and styled with Bootstrap.
* **Controllers (`app/routes.py`):** The backend core logic handling HTTP routing, database queries, and session management.

---

## 📊 Relational Database Schema

The application handles data persistence using an SQLite database with three core entities configured in a **One-to-Many Relationship**:

* **`User` Model:** Manages user credentials. One user can author multiple posts and write multiple comments.
* **`Post` Model:** Manages blog articles. Each post belongs to a single user and can hold multiple comments. Includes a cascade deletion setup (`cascade="all, delete-orphan"`) to automatically wipe associated comments if a post is deleted.
* **`Comment` Model:** Tracks article feedback. Stores distinct foreign keys (`user_id` and `post_id`) linking it concurrently to both an author and a parent post.

---

## 🛠️ Core Features Implemented

### 🔒 1. Secure Authentication & Password Hashing
* Integrated **Flask-Login** to handle secure user sessions, tracking tracking cookies, and protecting sensitive routes via `@login_required`.
* Implemented cryptographic password security via **Werkzeug** helpers using `pbkdf2:sha256` hashing routines to verify users safely without saving plain-text passwords.

### 📝 2. Secure Content CRUD Operations
* Built full data control forms for creating, reading, updating, and deleting blog entries.
* Implemented defensive route guarding (`abort(403)`) to block cross-user edits, ensuring only the original author can alter or remove a post.

### 📄 3. User Profiles & Pagination
* Created author-specific timeline routes (`/user/<username>`) querying isolated post histories.
* Implemented backend pagination using `.paginate(per_page=2)` to chunk query results, ensuring optimal data speeds and clean frontend navigation.

### 🔍 4. Multi-Column Global Search Engine
* Integrated a global keyword search filter utilizing the SQL **`.ilike()`** operator to execute case-insensitive matching across post titles, content bodies, and usernames simultaneously.

### 🧪 5. Automated Testing Suite
* Built an automated verification script (`tests.py`) using Python’s native `unittest` framework.
* Configured the environment to spin up a temporary, isolated **in-memory database** (`sqlite:///:memory:`) to test endpoints safely without polluting production records.

---

## 💻 Local Installation & VS Code Configuration

Follow these exact steps to set up the development environment inside Visual Studio Code:

### 1. Environment Setup
Clone your repository, open the folder in VS Code, and run the following commands in your integrated PowerShell terminal:
```powershell
# Create a local Python virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install all framework dependencies
pip install -r requirements.txt
2. Configure VS Code Python Interpreter
Press Ctrl + Shift + P to open the VS Code Command Palette.

Type and select Python: Select Interpreter.

Choose the path pointing to your virtual environment: .\venv\Scripts\python.exe.

3. Initialize the Database Schema
If your database file blog.db is missing its tables, run this backend fallback command to automatically stamp your relational tables:

PowerShell
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
4. Run the Application
Start your local development server by executing:

PowerShell
python app.py
Open your browser and navigate to: http://127.0.0.1:5000/

🧪 Running the Tests
To run the automated validation tests directly from the terminal, run:

PowerShell
python tests.py
📜 Author
Sandeep Pal – Full-Stack Developer Internship Track


---

### 💾 Step 4: Save & Push to GitHub
Once you save the file in VS Code, execute these commands in your terminal to update your repository:
```powershell
git add README.md
git commit -m "Docs: Added comprehensive README.md file for VS Code"
git push





