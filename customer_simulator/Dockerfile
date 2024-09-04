# syntax=docker/dockerfile:1

FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . ./

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Set the command to run the application
CMD ["python", "CustomerSimulator_2.py"]
