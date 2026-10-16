Act as a Senior Full-Stack Developer and DevOps Engineer. Please create a complete web application to manage a warehouse inventory. Follow the technical requirements and architecture outlined below:

### 1. Tech Stack & Architecture
- **Backend:** Python using the Flask framework.
- **Frontend:** HTML, CSS, and JavaScript (structured for Flask: HTML templates in the `templates/` folder, static CSS/JS assets in the `static/` folder).
- **Database:** MySQL.
- **Local Environment:** Set up a Python virtual environment inside the `.venv/` folder and include a `requirements.txt` file listing all necessary packages.
- **Environment Variables:** Use a `.env` file (managed via `python-dotenv`) to store all sensitive data (passwords, database credentials, host configurations). Use `camelCase` naming conventions where applicable.

### 2. Database Schema (MySQL)
Create a database named `warehouse` containing a table for products with the following columns (using `camelCase` for column names):
- `id` (INT, Primary Key, Auto Increment)
- `productName` (VARCHAR)
- `price` (DECIMAL)
- `description` (TEXT)
- `stockAmount` (INT)

### 3. Dockerization & Docker Compose
The application must be fully dockerized using a `compose.yml` file in the root directory that orchestrates 2 services:
1. **Database Container:** Official MySQL image configured to automatically create the `warehouse` database upon initialization.
2. **Application Container:**
   - Create a `Dockerfile` using the official Python image from Docker Hub.
   - Copy the application source code, install dependencies from `requirements.txt`, and define the entrypoint (`CMD` / `ENTRYPOINT`).
   - The custom Docker image built for this app should be named `appexample`.
   - Configure `compose.yml` so both containers communicate over an internal Docker network, passing environment variables from `.env`.

### 4. Deliverables & Code Quality
Once the application is fully functional, provide the following:
- **Unit Tests:** Write a few basic unit tests (using `pytest` or `unittest`) testing core routes or database connectivity.
- **Documentation:** A `README.md` file explaining setup, configuring `.env`, running locally, executing tests, and running the app via Docker Compose.
- **Vulnerability Analysis:** A brief security review in the `README.md` addressing common vulnerabilities (e.g., SQL injection, sensitive data exposure) and how they were mitigated.