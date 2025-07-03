# catsay
toy containerized python server using uvicorn


## Quick Start with Docker Compose

Run the following command to build and start the service:
```sh
docker compose up --build
```

## Example Usage with curl

**GET request:**
```sh
curl "http://localhost:8000/
```

**POST request:**
```sh
curl -X POST --data "Meow from POST!" http://localhost:8000/
```
