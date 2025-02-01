# Python Project Template

FastAPI-based Python service template with GitLab CI/CD pipeline.

# How to use

## Clone the template

git clone ssh://git@git.dapp-devs.com:2222/lumos-labs/tools/python-template.git your-new-project

## Enter the project directory

cd your-new-project

## Remove the old git history

rm -rf .git

## Initialize new git repository

git init

## Add the new remote

git remote add origin https://git.dapp-devs.com/your-group/your-new-repo.git

## Add all files

git add .

## Commit

git commit -m "Initial commit from template"

## Push to main branch

git push -u origin main

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
