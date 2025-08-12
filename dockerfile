FROM python:3.12-slim
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir "flask==3.1.*"

WORKDIR /app
COPY . /app

CMD ["python", "app.py"]
