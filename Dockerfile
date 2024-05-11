# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies from the Pipfile
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /app
COPY . /app


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment varible
ENV FLASK_ENV=production

# Run app.py when the container launches
#CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application with Gunicorn
CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:5000", "app:app"]
