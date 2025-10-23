# Software Stack Deep Dive – 2025‑10‑23

**TL;DR:** Continuing from our last conversation, a deeper dive into your project history reveals a consistent Python & Docker stack. However, the specific packages expand to include AI/ML libraries (langchain, openai, pandas), web frameworks (flask, gunicorn), database tools (sqlalchemy, psycopg2‑binary), and real‑time/3D libraries (flask‑socketio, three.js). A key part of your software ecosystem, especially for your father's business, likely involves the Microsoft 365 / Power Platform (Power Apps, Power Automate, SharePoint) given your "Microsoft based business" [2025‑07‑15] and GoDaddy hosting [2025‑07‑15]. Your local dev environment would need to account for both this open‑source stack and any potential integrations with Microsoft's ecosystem.

## [AJP‑05] Core Development Stack (Recap)
This is the foundation for all your custom projects, as established previously:

* **Languages/Runtimes:** Python (3.10+), JavaScript (for frontend)
* **Containerization:** Docker Desktop (configured for WSL 2 on Windows)
* **Version Control:** Git
* **Code Editor:** VS Code with Python and Docker extensions

## [AJP‑06] Project‑Specific Software & Python Packages
Your history shows three distinct types of software development projects, each with its own package requirements.

### [AJP‑06‑A] AI & Data Pipeline Projects
These projects ("AI Council" [2025‑10‑13], "MET4morfoses/OS" [2025‑08‑24]) require a stack focused on AI, data, and streaming:

* **openai:** The primary library for all OpenAI API interactions.
* **langchain:** Used for orchestrating the AI agents for the "AI Council" debates.
* **pandas:** For data manipulation within your "Unified Knowledge Pipeline."
* **flask‑socketio / websockets:** For the "decentralized live streaming" component of the "AI Council."
* **flask / gunicorn:** To serve the backend API that manages the agents and streams.

### [AJP‑06‑B] Interactive Web Applications
These projects ("Siddhartha" Journal [2025‑09‑17], "Buddhist Cosmology 3D Map" [2025‑10‑14]) are user‑facing web apps:

* **flask (or django):** The web framework to build the sites.
* **sqlalchemy:** The ORM to manage user data, journal entries, etc.
* **psycopg2‑binary:** The Python driver to connect to a PostgreSQL database (the most common choice for Dockerized Python apps).
* **flask‑login / flask‑bcrypt:** For handling user registration, login, and password hashing for the journal.
* **three.js:** A JavaScript library included in your frontend static files (e.g. `/static/js`) and served by Flask for the 3D map.

### [AJP‑06‑C] Business Process & Utility Apps
These projects are for your father's business, Majestic Design (Materials Management, Equipment Requests, Daily Reports [2025‑07‑11], and the delay form for Nicholas [2025‑10‑09]). You have two likely development paths here:

* **Python Web App Path:** Use the same stack as in [AJP‑06‑B] (flask, sqlalchemy) to build simple, internal web‑based forms.
* **Microsoft Power Platform Path:** Given you are a "Microsoft based business," it is highly probable these tools are (or should be) built using:
  * **Power Apps:** To create the forms for mobile/desktop use.
  * **Power Automate:** To handle the approval/notification logic (e.g., "when an equipment request is submitted, email the manager").
  * **SharePoint Lists / Dataverse:** To act as the simple database behind these apps.

Your local "dev env" for this stack would be your web browser and a Microsoft 365 license.

## [AJP‑07] Consolidated Environment Variables (.env file)
Based on this complete list, your `.env` file for a complex project like the "AI Council" or "Siddhartha" journal should include:

```env
# --- Flask App Settings ---
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=a‑very‑strong‑random‑key‑for‑sessions

# --- OpenAI API Settings ---
OPENAI_API_KEY=sk‑YourSecretKeyGoesHere

# --- Database Connection (PostgreSQL) ---
# These must match the 'environment' section of your db service in docker‑compose.yml
DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydatabase
```

## [AJP‑08] Summary of Local Environment Migration
To move to a "ground zero" machine, you would need to:

* **Install Core Tools:** Git, Python 3.10+, VS Code (with extensions), and Docker Desktop.
* **Install OS‑Specific Needs:** On Windows, enable WSL 2 and configure Docker to use it.
* **Log In to Services:**
  * Log in to your Microsoft 365 account to access the Power Platform.
  * Log in to GoDaddy to manage your domain and hosting.
* **Clone a Project:** `git clone <your‑repo‑url>`.
* **Create Local Files:** Inside the project, create the `.env` file and add your secrets (like `OPENAI_API_KEY`).
* **Run the App:** Run `docker-compose up --build` from your terminal to build the images and start all services (your Python app, the Postgres database, etc.).
