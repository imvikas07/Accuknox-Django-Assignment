# Social Network API

## Installation

### Requirements
- Docker
- Docker Compose

### Steps
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd social_network
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Apply migrations:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. Access the application at `http://localhost:8000`

## API Endpoints

### Authentication
- Signup: `POST /api/signup/`
- Login: `POST /api/login/`

### User Management
- Search Users: `GET /api/search/?query=`

### Friend Requests
- Send/Accept/Reject Friend Request: `POST /api/friend-requests/`
- List Friends: `GET /api/friends/`
- List Pending Requests: `GET /api/pending-requests/`

## Postman Collection
- [Postman Collection Link](<postman-collection-url>)

