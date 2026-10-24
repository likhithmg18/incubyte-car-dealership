# Car Dealership Inventory System

A full-stack car dealership inventory management application built with Django REST Framework, PostgreSQL, React, Vite, and Tailwind CSS.

## Features

- User registration and login using JWT authentication
- Protected vehicle inventory APIs
- Search vehicles by make, model, category, and price range
- Purchase vehicles with quantity validation
- Admin-only vehicle creation, updates, deletion, and restocking
- React-based inventory dashboard
- Backend automated tests

## Technology Stack

**Backend:** Python, Django, Django REST Framework, Simple JWT  
**Database:** PostgreSQL  
**Frontend:** React, Vite, Tailwind CSS  
**Version Control:** Git and GitHub

## Prerequisites

- Python 3.12 or compatible version
- Node.js and npm
- PostgreSQL
- Git

## Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/likhithmg18/incubyte-car-dealership.git
   cd incubyte-car-dealership
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install backend dependencies using your project's dependency file, if provided.

4. Configure the PostgreSQL database and set the required environment variables, including `DB_PASSWORD` and `DJANGO_SECRET_KEY`.

5. Apply migrations and create an administrator:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the backend:

   ```powershell
   python manage.py runserver
   ```

Backend URL: `http://127.0.0.1:8000/`

## Frontend Setup

Open another terminal:

```powershell
cd frontend
npm install
```

Create `frontend/.env` locally with:

```text
VITE_API_URL=http://127.0.0.1:8000/api
```

Start the frontend:

```powershell
npm run dev
```

Frontend URL: `http://localhost:5173/`

## Testing

Run backend tests from the project root:

```powershell
python manage.py test vehicles
```

The latest recorded test run passed **20 tests**. Run the tests again before submission to confirm the current result.

## Screenshots

Add screenshots of the login/register screen, inventory dashboard, vehicle search, and administrator functions here before submission.

## My AI Usage

AI assistance was used to help understand the requirements, plan the implementation, troubleshoot errors, and develop and review code and tests. The final implementation should be reviewed and tested by the author.

## AI Conversation Logs

See [`PROMPTS.md`](PROMPTS.md) for the required AI conversation logs or public conversation links.

## Repository

[GitHub repository](https://github.com/likhithmg18/incubyte-car-dealership)


# Car Dealership Inventory System

A full-stack inventory management application developed for the Incubyte assignment using Django REST Framework, PostgreSQL, React, Vite, and Tailwind CSS.

## Features

- User registration and JWT-based login
- Protected vehicle inventory APIs
- Search and filter vehicles
- Purchase vehicles with stock validation
- Admin-only vehicle creation, updates, deletion, and restocking
- React inventory dashboard
- Automated backend tests

## Technology Stack

- **Backend:** Python, Django, Django REST Framework
- **Authentication:** JWT using Simple JWT
- **Database:** PostgreSQL
- **Frontend:** React, Vite, Tailwind CSS
- **Version control:** Git and GitHub

## Prerequisites

- Python 3.12
- Node.js and npm
- PostgreSQL
- Git

## Backend Setup

Clone the repository:

```bash
git clone https://github.com/likhithmg18/incubyte-car-dealership.git
cd incubyte-car-dealership
```

Create and activate a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r requirements.txt
```

Configure PostgreSQL and set the required environment variables, including `DB_PASSWORD` and `DJANGO_SECRET_KEY`. Create the database expected by your Django settings.

Apply migrations:

```powershell
python manage.py migrate
```

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Start the backend:

```powershell
python manage.py runserver
```

Backend: `http://127.0.0.1:8000/`

## Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
```

Create a local `frontend/.env` file containing:

```text
VITE_API_URL=http://127.0.0.1:8000/api
```

Start the frontend:

```powershell
npm run dev
```

Frontend: `http://localhost:5173/`

## Running Tests

From the project root, run:

```powershell
python manage.py test vehicles
```

The latest recorded run passed 20 backend tests. Run the command again before submission and update this section if the result changes.

## Screenshots

Add screenshots of the login/register screen, inventory dashboard, vehicle search, and administrator functions before submission.

## My AI Usage

ChatGPT was used to help understand the assignment, plan implementation steps, troubleshoot development issues, and assist with API development, testing, and documentation. The implementation was tested locally. I reviewed the generated suggestions and made changes while building the project.

## AI Conversation Logs

See [PROMPTS.md](PROMPTS.md) for the AI conversation records and links.

## Repository

[GitHub repository](https://github.com/likhithmg18/incubyte-car-dealership)
