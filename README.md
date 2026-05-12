# CodeSeer

AI-Assisted Static Code Security Scanner (CI/CD Ready)

## Overview

CodeSeer is a containerized static analysis tool designed to detect security vulnerabilities in Python codebases.<br>
It integrates into CI/CD pipelines and produces both machine-readable and human-readable reports.

## Features
- Static security analysis using Bandit
- Code quality and best-practice linting using Ruff
- Multi-tool scan aggregation (Bandit + Ruff + Semgrep-ready architecture)
- Containerized execution (Docker-based, environment-independent)
- CI/CD integration (GitHub Actions ready)
- JSON + HTML report generation # Not yet unified JSON but separate JSONs
- Structured input/output separation (`/input` → `/output`)
- Pipeline gating based on HIGH severity issues
- Extensible architecture for additional scanners and AI-based analysis

## Architecture
Input Code → CodeSeer Container → Unified Security Report  
(/input) → (scanners + aggregation) → (/output)

- Bandit → security vulnerabilities
- Ruff → linting & best practices
- Semgrep → pattern-based analysis
- Aggregation layer → unified normalized output
- Report generator → JSON + HTML output

## Usage (Docker)
### Run locally
```
docker run --rm \
  -v $(pwd)/samples:/input \
  -v $(pwd)/reports:/output \
  ghcr.io/YOUR_USERNAME/codeseer:[image tag]
```
### Output
After execution:
reports/ </br>
 ├── bandit-report.json </br>
 ├── ruff-report.json </br>
 ├── semgrep-report.json </br>
 └── report.html

## CI/CD Integration
### Example GitHub Actions usage:
```
- name: Run CodeSeer
  run: |
    docker run --rm \
      -v ${{ github.workspace }}/[input path]:/input \
      -v ${{ github.workspace }}/[reports output path]:/output \
      ghcr.io/grigorescustefan/codeseer:[image tag]
```
### Exit Codes
0 → No high severity issues<br>
1 → High severity vulnerabilities detected<br>
<b>It's important to mention that vulnerabilities will still be presented in a report regardless of severity, the pipeline should only fail when high severity ones are found.</b>

## Technologies
- Python 3.11
- Bandit 1.9.4
- Ruff 0.6.9
- Semgrep 1.92.0
- Docker
- GitHub Actions

## Future Improvements
- Semantic analysis layer (CodeBERT / transformer-based prioritization)
- VSCode extension integration (local developer workflow)
- WebView-based report UI inside editor
- Policy engine for customizable severity rules

## [WIP] Debugging Mode for VSCode extension
In order to start the extension:
- open `codeseer-vscode/src/extension.ts`
- Run -> Start Debugging (it will open another VSCode window)
- Open only the folder you want to have analyzed
- Open the bar up top for `Show and Run Commands` (Ctrl + Shift + P) and search for "Run CodeSeer Scan"
- In the open folder another one will be created called `reports` where the JSONs and the HTML will be created
- When the scan is done, it will automatically open the `HTML` file in the browser