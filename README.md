# CodeSeer

AI-Assisted Static Code Security Scanner (CI/CD Ready)

## Overview

CodeSeer is a containerized static analysis tool designed to detect security vulnerabilities in Python codebases.<br>
It integrates into CI/CD pipelines and produces both machine-readable and human-readable reports.

## Features
- Static analysis using Bandit
- Containerized execution (Docker)
- CI/CD ready (GitHub Actions support)
- JSON + HTML report generation
- Input/output volume separation
- Fail pipeline on HIGH severity issues

## Architecture
Input Code  →  CodeSeer Container  →  Reports Output<br>
   (/input)           ↓                  (/output)<br>
                Bandit Scan<br>
                Policy Engine<br>
                HTML Generator<br>

## Usage (Docker)
### Run locally
```
docker run --rm \
  -v $(pwd)/samples:/input \
  -v $(pwd)/reports:/output \
  ghcr.io/YOUR_USERNAME/codeseer:latest
```
### Output
After execution:
reports/<br>
 ├── report.json<br>
 └── report.html

## CI/CD Integration
### Example GitHub Actions usage:
```
- name: Run CodeSeer
  run: |
    docker run --rm \
      -v ${{ github.workspace }}/samples:/input \
      -v ${{ github.workspace }}/reports:/output \
      ghcr.io/grigorescustefan/codeseer:[tag]
```
### Exit Codes
0 → No high severity issues<br>
1 → High severity vulnerabilities detected<br>
<b>It's important to mention that vulnerabilities will still be presented in a report regardless of severity, the pipeline should only fail when high severity ones are found.</b>
## Technologies
- Python 3.11
- Bandit
- Docker
- GitHub Actions