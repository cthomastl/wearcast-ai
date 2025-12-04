FROM python:3.11-slim


WORKDIR /usr/src/app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app (templates, static, app.py, etc.)
COPY . .

EXPOSE 5000

# Run with Gunicorn, binding to all interfaces (for Docker port mapping)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
