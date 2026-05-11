FROM python:3.11-slim

WORKDIR /app

RUN pip install bandit semgrep

COPY scanner/ scanner/

# Define default paths (can be overridden at runtime)
ENV INPUT_PATH=/input
ENV OUTPUT_PATH=/output

CMD ["python", "scanner/entrypoint.py"]