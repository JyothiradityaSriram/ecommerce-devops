FROM python:3.11-slim-trixie

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade \
    pip "setuptools==84.2.1" wheel && \
    pip install --no-cache-dir -r requirements.txt
# Remove pip from the runtime image; dependencies are already installed
RUN rm -rf \
    /usr/local/lib/python3.11/site-packages/pip \
    /usr/local/lib/python3.11/site-packages/pip-*.dist-info \
    /usr/local/bin/pip \
    /usr/local/bin/pip3 \
    /usr/local/bin/pip3.11

COPY . .

RUN useradd -m appuser
USER appuser

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
