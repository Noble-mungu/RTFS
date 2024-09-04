# syntax=docker/dockerfile:1

FROM python:3.11.4-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Copy the source code into the container.
COPY . ./

# Expose the port that the application listens on.
EXPOSE 8000

# # Copy the start script and make sure it's executable
# COPY start.sh /app/start.sh
# RUN chmod +x /app/start.sh

# Run the start script
CMD ["python", "kafka_producer_random.py" , "python kafka_producer_random_2.py"]

