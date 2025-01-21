# Base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install necessary system packages
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# # Set the environment variables
# ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8010

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]