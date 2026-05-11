# CodeSeer
AI-Assisted Static Code Analysis for CI/CD Security Pipelines

## Overview
CodeSeer is a DevSecOps-oriented project that integrates static code analysis into CI/CD workflows to detect and report security vulnerabilities early in the software development lifecycle.

The system automates vulnerability detection using Bandit, applies a policy-based evaluation layer, and generates both machine-readable (JSON) and human-readable (HTML) security reports.

---

## Features
- Automated static code analysis using Bandit
- CI/CD integration via GitHub Actions
- Policy-based vulnerability evaluation engine
- Automated pass/fail security gating
- JSON and HTML report generation
- Artifact-based report download (GitHub Actions UI)

---

## Technologies
- Python
- Bandit
- GitHub Actions
- Docker (planned/optional)
- Hugging Face Transformers (future AI extension)

---

## Project Structure
- samples/ # Vulnerable code examples
- scanner/ # Evaluation and reporting logic
- .github/workflows/ # CI/CD pipeline definition
- report.json # Machine-readable output
- report.html # Human-readable security report

---

## CI/CD Pipeline

On every push to `main` or `dev`:

1. Checkout repository
2. Set up Python environment
3. Run Bandit static analysis
4. Generate JSON vulnerability report
5. Evaluate security policy (fail on HIGH severity)
6. Generate HTML report for visualization
7. Upload reports as GitHub Actions artifacts

---

## Running Locally
### 1. Create environment
```
python -m venv venv
```

### 2. Activate environment (Windows)
```
.\venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

## Manual execution
<b>Usually this is not necessary due to the scope and focus being on automated analysis, but it can be done for ease of understanding and debugging.</b>

### 1. Run static analysis
```
bandit -r ./samples -f json -o report.json
```

### 2. Evaluate results
```
python scanner/evaluate.py
```

### 3. Generate HTML report
```
python scanner/report_generator.py
```