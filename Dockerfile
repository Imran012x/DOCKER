#For Streamlit Deployment:[Backend]
# # Use the official Python image as a base
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements.txt into the container
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the current directory contents into the container at /app
# COPY . .

# # Expose the port that Streamlit runs on
# EXPOSE 8501

# # Command to run the Streamlit app
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]


# # You want to package your app so it runs the same on any computer.
# # You want to automate setup (no more "works on my machine" problems!).
# # You want to ship your code + environment as one piece.



#For RailWay Deployment:[Fronted+Backend]
# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose the dynamic port
EXPOSE $PORT

# Run Streamlit using the dynamic port
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.enableCORS=false"]
