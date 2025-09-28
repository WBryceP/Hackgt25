FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# App files
COPY main.py models.py highlight_service.py /app/

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

