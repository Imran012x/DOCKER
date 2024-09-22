# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
