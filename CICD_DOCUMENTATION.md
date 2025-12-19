# CI/CD Pipeline Documentation

## Overview
This project uses GitHub Actions for continuous integration and continuous deployment (CI/CD). The pipeline automates testing, security scanning, Docker image building, and deployment across multiple environments.

## Workflows

### 1. Main CI/CD Pipeline (`ci-cd.yml`)
**Triggers:** 
- Push to `main`, `doctor-frontend`, or `develop` branches
- Pull requests to `main`, `doctor-frontend`, or `develop` branches
- Daily at 2 AM UTC

**Jobs:**

#### Test Job
- Sets up Python 3.11 environment
- Installs project dependencies
- Runs pylint for code quality
- Executes all unit tests using `run_tests_dispatch.py`
- Generates coverage reports
- Uploads coverage to Codecov

```bash
# To run tests locally (what CI does):
python run_tests_dispatch.py all
```

#### Security Job
- Runs Bandit for security vulnerabilities
- Checks dependencies with Safety
- Flags high-risk issues
- Continues even if issues found (for awareness)

#### Build Job
- Builds Docker image using Buildx
- Logs into GitHub Container Registry (GHCR)
- Tags image with branch name and commit SHA
- Pushes image to registry (only on non-PR events)

#### Deployment Jobs
- **deploy-dev**: Triggered on push to `develop` branch
- **deploy-staging**: Triggered on push to `doctor-frontend` branch
- **deploy-prod**: Triggered on push to `main` branch

### 2. Monitoring Workflow (`monitoring.yml`)
**Triggers:**
- Daily at midnight UTC
- Manual workflow dispatch

**Jobs:**

#### Dependency Check
- Audits Python packages for known vulnerabilities
- Uses pip-audit tool

#### Docker Image Check
- Builds and runs Docker image
- Performs basic health check on running container

#### Code Quality
- Checks code formatting (Black)
- Validates import sorting (isort)
- Runs Flake8 linting

## Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key variables:
- `FLASK_APP`: Entry point for Flask application
- `FLASK_ENV`: Development or production mode
- `SECRET_KEY`: Session secret (must be unique in production)
- `DATA_DIR`: Location of CSV data files

### GitHub Secrets
For production deployment, configure these secrets in GitHub Settings → Secrets:

- `REGISTRY_USERNAME`: Docker registry username
- `REGISTRY_PASSWORD`: Docker registry password
- `DEPLOY_KEY`: SSH key for deployment servers
- `SLACK_WEBHOOK`: Slack notifications (optional)

## Local Testing

### Run Tests Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests (both unittest and pytest)
python run_tests_dispatch.py all

# Run only pytest tests
python run_tests_dispatch.py pytest

# Run only unittest tests
python run_tests_dispatch.py unittest

# Generate coverage report
python run_tests_dispatch.py coverage
```

### Build Docker Image
```bash
# Build the image
docker build -t clinexa:latest .

# Run with docker-compose
docker-compose up -d

# Run tests in container
docker-compose run --rm tests

# View logs
docker-compose logs -f web
```

## Branch Strategy

| Branch | Environment | Trigger | Action |
|--------|-------------|---------|--------|
| `main` | Production | Tag/Release | Deploy to prod |
| `doctor-frontend` | Staging | Push | Deploy to staging |
| `develop` | Development | Push | Deploy to dev |
| `feature/*` | Testing | PR | Run tests only |

## Monitoring & Alerts

### GitHub Actions Status
- Check workflow status in Actions tab
- Enable email notifications: Settings → Notifications

### Test Coverage
- Coverage reports uploaded to Codecov
- View at: https://codecov.io/gh/your-repo

### Docker Registry
- Images available at: `ghcr.io/your-org/clinexa`
- Tagged by branch and commit SHA

## Troubleshooting

### Workflow Fails on Test Job
```bash
# 1. Check if tests pass locally
python run_tests_dispatch.py all

# 2. Verify Python dependencies
pip install -r requirements.txt

# 3. Check for import errors
python -m py_compile src/**/*.py
```

### Docker Build Fails
```bash
# 1. Build locally to identify issues
docker build -t clinexa:test .

# 2. Check Dockerfile syntax
docker build --no-cache -t clinexa:test .

# 3. Verify all files are in context
cat .dockerignore
```

### Registry Push Fails
- Verify GitHub token has `write:packages` permission
- Check GHCR authentication
- Ensure `REGISTRY` environment variable is set correctly

## Security Best Practices

1. **Secrets Management**
   - Never commit `.env` files
   - Store secrets in GitHub Secrets, not code
   - Rotate credentials regularly

2. **Container Security**
   - Use slim Python base images
   - Scan images with Trivy: `trivy image clinexa:latest`
   - Keep dependencies updated

3. **Code Quality**
   - All PRs must pass tests before merge
   - Coverage threshold: 70% minimum
   - Security scans must complete (warnings acceptable)

4. **Access Control**
   - Branch protection rules for `main`
   - Require status checks to pass
   - Require code reviews before merge

## Manual Deployment

For emergency deployments without waiting for CI/CD:

```bash
# Build locally
docker build -t clinexa:$(git rev-parse --short HEAD) .

# Push to registry
docker push ghcr.io/your-org/clinexa:$(git rev-parse --short HEAD)

# Deploy (platform-specific)
# Example for Docker Swarm:
docker service update --image ghcr.io/your-org/clinexa:TAG clinexa
```

## Performance Metrics

- **Average CI/CD Time**: 5-10 minutes
- **Docker Build Time**: 2-3 minutes
- **Test Execution Time**: 1-2 minutes
- **Total Pipeline Duration**: 10-15 minutes

## Future Enhancements

- [ ] Add Kubernetes deployment
- [ ] Implement blue-green deployments
- [ ] Add database migration checks
- [ ] Integrate SonarQube for code analysis
- [ ] Setup notifications (Slack, Email)
- [ ] Add load testing
- [ ] Implement rollback automation
