# GuessWho?

GuessWho? is an application that identifies the faces of Korean idols and actors from an image or a video using a face recognition model connected to a face embedding vector database.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Svelte
- **Database**: Redis
- **Face Recognition Model**: InsightFace
- **Containerization**: Docker, Docker Compose

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Cloning the Repository

```bash
git clone https://github.com/yourusername/guesswho.git
cd guesswho
```

### Running the Application



1. Navigate to the project directory:

    ```bash
    cd guesswho
    ```

2. Build and start the containers:

    ```bash
    docker-compose up --build
    ```

3. Access the application:
    - Frontend: `http://localhost`
    - Backend: `http://localhost:8000`