FROM python:3.11-alpine

WORKDIR /app

# Install system packages and poetry first
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev \
    && pip install poetry \
    && poetry config virtualenvs.create false

# Copy only the files necessary for installing Python dependencies.
# This layer will be cached until pyproject.toml or poetry.lock changes.
COPY pyproject.toml poetry.lock README.md /app/

# Install Python dependencies
RUN poetry install --no-dev --no-interaction

# Copy the rest of the project files. This layer will be rebuilt every time
# the project files change, but the previous layers will be cached.
COPY ./aosync /app/aosync

ENV APPOPTICS_TOKEN=''

ENTRYPOINT ["python", "-m", "aosync"]
CMD ["--help"]
