FROM python:3.11-slim

WORKDIR /app

RUN pip install \
    bandit==1.9.4 \
    ruff==0.6.9 \
    semgrep==1.92.0 

COPY scanner/ scanner/

ENV INPUT_PATH=/input
ENV OUTPUT_PATH=/output
ENV PYTHONPATH=/app

CMD ["python", "scanner/entrypoint.py"]