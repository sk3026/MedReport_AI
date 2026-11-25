# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY backend ./backend

# Copy only the vector database required by the RAG system
COPY vectorstore ./vectorstore

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]