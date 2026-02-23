FROM python:3.11-slim

WORKDIR /app

RUN python -m pip install --no-cache-dir -U pip

# Copy backend into the image
COPY backend/ /app/

# Install dependencies from pyproject.toml
RUN pip install --no-cache-dir -e ".[dev]"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]