# CodeSeer
AI-Powered-Static-Code-Analyzer-CI/CD-Integration

## Overview
This project aims to integrate AI-assisted static code analysis into CI/CD workflows in order to detect vulnerabilities earlier in the software development lifecycle.

## Technologies
- Python
- Bandit
- Docker
- GitHub Actions
- Hugging Face Transformers

## Setup

### Create virtual environment
python -m venv venv

### Activate environment (Windows)
.\venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

## Running Static Analysis

bandit -r .\samples\

## Generate JSON Report

bandit -r .\samples\ -f json -o report.json

## Run Analyzer

python .\scanner\analyzer.py