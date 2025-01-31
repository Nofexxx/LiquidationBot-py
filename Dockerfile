FROM python:3.12-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Use for repository with postgresql
# RUN apk update
# RUN apk add postgresql-dev gcc python3-dev musl-dev
# RUN apk add file-dev

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
