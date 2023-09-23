## Development

### Option 1: Docker Compose

You may need to configure your IDE to tap into the Docker containers to be able to use debug breakpoints.

```bash
docker-compose -f docker-compose-dev.yml up
```

### Option 2: Manual

```bash
# Tested with Mac OS 12.6 /w M1 Chip

brew install postgresql

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# TODO: env var customization
uvicorn main:app --reload
```

## Code Formatting (Typescript)

```bash
npx prettier --write .
docker-compose -f docker-compose-dev.yml exec ui npx prettier --write .
```

## Swagger

http://localhost:8000/docs
http://localhost:8000/redoc
