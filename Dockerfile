# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# Add GDAL installation commands to your Dockerfile
RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev python3-gdal && \

# Copy project files
COPY . /app/

# Expose the port
EXPOSE 8000

# Change ownership of the app directory
ARG UID=1000
ARG GID=1000
RUN chown -R ${UID}:${GID} /app

# Switch to the new user
USER ${UID}:${GID}

# Start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
