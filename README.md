# Python Project Template

FastAPI-based Python service template with GitLab CI/CD pipeline.

# Project Structure

```
.
├── .env.example
├── Dockerfile
├── README.md
├── requirements.txt
├── scripts
├── utils
├── models
├── tests
├── app.py
```

# Using default Dockerfile

```bash
docker build -t fastapi-template .
docker run -d -p 80:80 fastapi-template
```

# Models

In `models/db/` folder you can find models for your project with postgresql.

# Schemas

In `models/schemas/` folder you can find schemas for your project with pydantic.

# Utils

In `utils/` folder you can find utils for your project.

# Scripts

In `scripts/` folder you should put your scripts for your project.

# Requirements

In `requirements.txt` you should put your requirements for your project. Now it's only fastapi inside.

# .env

In `.env.example` you should put your environment variables for your project.
