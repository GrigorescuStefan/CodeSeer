FROM python:3.11-slim

WORKDIR /app

RUN pip install bandit semgrep ruff

COPY scanner/ scanner/

ENV INPUT_PATH=/input
ENV OUTPUT_PATH=/output
ENV PYTHONPATH=/app

CMD ["python", "scanner/entrypoint.py"]