# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install PostgreSQL development packages to build psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for the Docker container
ENV PYTHONUNBUFFERED 1

# Run Django development server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
