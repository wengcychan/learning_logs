FROM python:3.12

WORKDIR /learning_log

# Copy the requirements.txt file and install the Python dependencies
COPY requirements.txt /learning_log/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /learning_log/

# Expose the port the Django application will run on
EXPOSE 8000

# Set the command to start the Django development server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]