#Official python image (bc I am using flask)
FROM python:3.12

# Working directory is inside the container (container is being made in app folder)
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY app/requirements.txt .
# Install dependencies (no cache ensures most recent versions of files)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV DATABASE_URL=sqlite:///ClubHub\app\application\database\database.db

# Run the Flask application
CMD ["flask", "run"]
