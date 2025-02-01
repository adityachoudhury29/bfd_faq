# FAQ Project

A Django-based project with an API to fetch frequently asked questions (FAQs) in different languages. The API automatically translates the FAQ questions and answers to supported languages using Google Translate.

## Installation
(NOTE: Before running the project, ensure that the ports :8000, :6380 and :5432 are free)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adityachoudhury29/bharatfd_task.git
   cd bharatfd_task
   ```

2. **Install dependencies:**
   Ensure you have Python 3.x and pip installed. Then, create a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
   ```

   Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and run Redis(on separate terminal instance):**
   - Install Redis on your system if it is not already installed.
     - On Ubuntu/Debian:
       ```bash
       sudo apt update && sudo apt install redis
       ```
     - On macOS (using Homebrew):
       ```bash
       brew install redis
       ```
     - On Windows, use [Redis for Windows](https://github.com/microsoftarchive/redis/releases) or run Redis via WSL.

   - Start the Redis server:
     ```bash
     redis-server
     ```
   Keep this terminal instance running.

4. **Set up the database:**
   Use the default SQLite database provided by Django (Uncomment the SQLite configuration and comment the PostgreSQL configuration in `settings.py`).

   Run migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and visit [http://localhost:8000](http://localhost:8000) to see the live application.

### Docker Setup

If you have Docker and Docker-compose installed and set up, you can use it as well:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adityachoudhury29/bharatfd_task.git
   cd bharatfd_task
   ```
   Setup .env variables and provide necessary credentials:
   ```bash
   cp .env.example .env
   ```
   Also make sure that psql config is uncommented and sqlite config is commented in `settings.py`.
   
2. **Build containers using `docker-compose`:**
   ```bash
   sudo docker-compose build
   ```
3. **Start containers in detached mode:**
   ```bash
   sudo docker-compose up -d
   ```
4. **Make migrations within docker:**
   ```bash
   sudo docker-compose exec web python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   sudo docker-compose exec web python manage.py createsuperuser
   ```
6. **Access the app**:
   The app will be available at [http://localhost:8000](http://localhost:8000).

---

## Admin Panel
You can use the admin panel to view, create as well as edit API records, at [http://localhost:8000/admin](http://localhost:8000/admin).

---

## To run tests
You can run tests using the command: ```pytest```

---

## API Usage

You can interact with the API to fetch FAQs. Here are examples using `curl`:

- **Fetch FAQs in English (default):**
  ```bash
  curl http://localhost:8000/api/faqs/
  ```

- **Fetch FAQs in Hindi:**
  ```bash
  curl http://localhost:8000/api/faqs/?lang=hi
  ```

- **Fetch FAQs in Bengali:**
  ```bash
  curl http://localhost:8000/api/faqs/?lang=bn
  ```

- **Fetch FAQs in Arabic:**
  ```bash
  curl http://localhost:8000/api/faqs/?lang=ar
  ```

- **Fetch FAQs in Chinese:**
  ```bash
  curl http://localhost:8000/api/faqs/?lang=zh
  ```

---

## Contribution Guidelines

1. **Fork the Repository**: 
   Fork the repository and clone your fork locally to make changes.

2. **Create a Branch**: 
   Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Write Tests**: 
   Make sure to write tests for any new functionality or bugfixes. Use `pytest` for testing.

4. **Code Style**: 
   Follow Python's PEP 8 guidelines. Use `black` for code formatting and `flake8` for linting.

5. **Commit Changes**: 
   Make small, atomic commits with descriptive messages:
   ```bash
   git commit -m "feat: add feature"
   #or
   git commit -m "fix: fixed feature"
   ```

6. **Push Changes**:
   Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**: 
   Open a pull request (PR) to the main repository with a description of your changes.

8. **Review Process**: 
   Maintain a positive attitude during the review process, and be open to feedback. Make any requested changes promptly.

---
