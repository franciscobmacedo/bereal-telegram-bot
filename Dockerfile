# --> Building Stage
FROM python:3.10-slim AS builder

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Create & Activate Virtual Env
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Poetry and Requirements
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
# Because Poetry sometimes has issues with Docker, we revert back to PIP
RUN poetry export -f requirements.txt --output requirements.txt
#COPY requirements.txt .
RUN pip install -r requirements.txt


# --> Operational Stage
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Move from builder to this image
COPY --from=builder /opt/venv /opt/venv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /code
COPY . /code/

CMD ["./run.py", "bot"]
