# ACEest Fitness & Gym - Automated CI/CD

## Objective

A Flask fitness/gym application demonstrating Git/GitHub, Pytest, Docker, Jenkins and GitHub Actions.

## Endpoints

- GET `/` - application status
- GET `/health` - health check
- GET `/members` - list members
- POST `/members` - add member
- GET `/members/<id>` - get member
- DELETE `/members/<id>` - delete member

## Requirements

Python 3.12+, Git, Docker and a GitHub account. Jenkins is required for the Jenkins phase.

## Local setup

```bash
git clone https://github.com/2025tm93200-rohit/ACEest-Fitness-Gym-CICD.git
cd ACEest-Fitness-Gym-Flask-CICD
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Manual validation

```bash
python -m py_compile app.py
flake8 app.py tests
pytest -q
```

## Docker

```bash
docker build -t aceest-fitness-gym .
docker run --rm -p 5000:5000 aceest-fitness-gym
docker run --rm aceest-fitness-gym pytest -q
```

## Git workflow

```bash
git init
git add .
git commit -m "feat: initialize ACEest Flask application"
git branch -M main
git remote add origin <YOUR-GITHUB-REPOSITORY-URL>
git push -u origin main
```

Suggested commits:

```text
feat: initialize Flask gym application
feat: add member management endpoints
test: add pytest test suite
build: add Docker container
ci: add GitHub Actions workflow
ci: add Jenkins pipeline
docs: add project documentation
```

## GitHub Actions

`.github/workflows/main.yml` runs on every push and pull request:
Checkout -> Python setup -> dependencies -> syntax check -> Flake8 -> Pytest -> Docker build -> Pytest inside Docker.

## Jenkins

The `Jenkinsfile` performs:
Checkout -> Docker Build -> Syntax Check -> Pytest -> Flake8 Quality Gate -> SonarQube Analysis.

Create a Jenkins Pipeline job using **Pipeline script from SCM**, Git, branch `*/main`, and script path `Jenkinsfile`. The Jenkins agent needs Docker and Git. Configure a Jenkins secret text credential named `sonarqube-token` and set the SonarQube server URL in the pipeline environment if your instance is not running at `http://sonarqube:9000`.

## SonarQube

Add a `sonar-project.properties` file at the project root and point Jenkins to the SonarQube server. For Docker Desktop/WSL-based Jenkins runs, the scanner cannot reliably resolve `http://sonarqube:9000`, so the default pipeline URL is set to `http://host.docker.internal:9000`. If SonarQube is running elsewhere, update the `SONAR_HOST_URL` environment variable in the Jenkins pipeline or the Jenkins credentials/config for the job. The scanner also waits for the SonarQube quality gate before the pipeline continues.

## Submission evidence

Capture screenshots of:

1. Public GitHub repository
2. Meaningful commits
3. Pytest passing
4. Docker build
5. GitHub Actions successful run
6. Jenkins successful BUILD and Quality Gate
