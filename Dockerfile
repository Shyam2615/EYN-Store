# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirments.txt

# Expose port 8000 to allow external connections
EXPOSE 8000

# Define the command to run on startup
CMD ["python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
