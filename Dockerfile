FROM python:3.11-slim

WORKDIR /app

RUN pip install bandit

COPY scanner/ scanner/

ENV SCAN_PATH=/scan

CMD ["python", "scanner/entrypoint.py"]