# Django app
FROM python:3.11-alpine AS intertidal
EXPOSE 80
WORKDIR /app

# add system deps
RUN apk update \
    && apk add git libmagic curl \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/cache/apk/*

# install python deps
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

# add project files
COPY . /app

# add prod assets

# collect static assets for production
RUN python manage.py collectstatic --noinput

# run migrations and start server
CMD ["docker/docker-entrypoint.sh"]