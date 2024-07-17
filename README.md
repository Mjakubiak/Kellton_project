# Kellton_project
# Django Family Budget App

A Django application for managing family budgets, incomes, and expenses.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### 1. Clone the Repository

```shell
git clone https://github.com/Mjakubiak/Kellton_project.git
cd Kellton_project
```

### 2. Build and Run the Application
```shell
docker-compose up -d --build 
```

This command will:

    Build the Docker images for your Django application and PostgreSQL database.
    Run database migrations.
    Load initial data from initial_data.json.
    Start the Django development server on port 8000.
    Run tests.

### 3. Access the Application
To use it as a user you have to log in first:
```
http://localhost:8000/api-login/login/
```
Then you can access the api:
```
http://localhost:8000/api/
```
### License

This project is licensed under the MIT License. See the LICENSE file for details.