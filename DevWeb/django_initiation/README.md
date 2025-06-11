## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and consistent development environments.

### Project-Specific Docker Details
- **Python Version:** 3.13-slim (as specified in the Dockerfile)
- **Dependencies:** Installed from `requirements.txt` inside a Python virtual environment (`.venv`) during the build process.
- **System Packages:** The image installs build tools and libraries required for Django and Pillow (`build-essential`, `libjpeg-dev`, `zlib1g-dev`, `libpq-dev`).
- **Database:** Uses SQLite (`db.sqlite3` is included in the image). No external database service is configured by default.
- **Media Files:** The `media/` directory is included in the image. For persistent media storage during development, you can uncomment the relevant `volumes` lines in `docker-compose.yml`.

### Environment Variables
- The Dockerfile sets:
  - `PYTHONDONTWRITEBYTECODE=1`
  - `PYTHONUNBUFFERED=1`
- If you have a `.env` file for Django settings, you can enable it by uncommenting the `env_file: ./.env` line in `docker-compose.yml`.

### Build and Run Instructions
1. **Build and start the application:**
   ```sh
   docker compose up --build
   ```
   This will build the image and start the Django development server.

2. **Access the application:**
   - The Django app will be available at [http://localhost:8000](http://localhost:8000)

### Ports
- **8000:** Exposed by the `python-app` service for the Django development server.

### Special Configuration
- **User:** The container runs as a non-root user (`appuser`) for improved security.
- **Persistent Data (Optional):**
  - To persist uploaded media and the SQLite database between container restarts, uncomment the `volumes` section in `docker-compose.yml`:
    ```yaml
    volumes:
      - ./media:/app/media
      - ./db.sqlite3:/app/db.sqlite3
    ```
- **Environment Variables:**
  - If your project requires custom environment variables, add them to a `.env` file and uncomment the `env_file` line in the compose file.

---

*These instructions are specific to this Django project and its Docker setup. For further customization (e.g., switching to PostgreSQL), update the Docker and Compose files accordingly.*
