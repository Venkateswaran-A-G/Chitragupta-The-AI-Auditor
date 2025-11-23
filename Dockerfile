# Use an official lightweight Python image as the base.
FROM python:3.9-slim

# Set environment variables to make Python output clearer in logs.
ENV PYTHONUNBUFFERED True

# Set the working directory inside the container to /app.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy the local code to the container's working directory.
COPY . ./

# Install production dependencies from requirements.txt.
# We use --no-cache-dir to keep the image size down.
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080, which is the default port the ADK Runner listens on.
EXPOSE 8080

# Define the command to run when the container starts.
# This starts your main.py server.
CMD exec python main.py
