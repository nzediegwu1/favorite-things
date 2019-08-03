# Pull base image
FROM python:3

# Arguments to be passed during build
ARG DB_USER
ARG POSTGRES_DB
ARG DB_PASS
ARG DB_HOST

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_USER=${DB_USER}
ENV POSTGRES_DB=${POSTGRES_DB}
ENV DB_PASS=${DB_PASS}
ENV DB_HOST=${DB_HOST}
ENV ENVIRONMENT production

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Install dependencies
RUN pip install pipenv
RUN pipenv install --system
RUN python manage.py migrate

EXPOSE 7000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:7000"]

