# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Streamlit app runs on
EXPOSE 8501

# Set environment variables for Streamlit
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501

# Command to run Streamlit
CMD ["streamlit", "run", "your_script.py"]  # Replace with the actual filename

