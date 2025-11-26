![Docker Image Latest Badge](https://ghcr-badge.egpl.dev/sfu-dhil/intertidal/latest_tag?trim=major&label=latest)
![Docker Image Size badge](https://ghcr-badge.egpl.dev/sfu-dhil/intertidal/size)

# Intertidal

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Initialize the Application

    docker compose up -d --build

Intertidal Frontend will be available at `http://localhost:8080/`
Intertidal Admin will be available at `http://localhost:8080/admin/`

### Install/Switch the admin theme

    # Bootstrap
    docker exec -it intertidal_app python manage.py loaddata admin_interface_theme_bootstrap.json

    # Django
    docker exec -it intertidal_app python manage.py loaddata  admin_interface_theme_django.json

    # Foundation
    docker exec -it intertidal_app python manage.py loaddata  admin_interface_theme_foundation.json

    # U.S. Web Design Standards
    docker exec -it intertidal_app python manage.py loaddata  admin_interface_theme_uswds.json

### Create your superuser

    docker exec -it intertidal_app python manage.py createsuperuser

Enter `username`, `email`, and `password` as prompted

example:

    docker exec -it intertidal_app python manage.py createsuperuser --username="admin" --email="dhil@sfu.ca"

## General Usage

### Starting the Application

    docker compose up -d

### Stopping the Application

    docker compose down

### Rebuilding the Application (after upstream or js/python package changes)

    docker compose up -d --build

### Viewing logs (each container)

    docker logs -f intertidal_app
    docker logs -f intertidal_db
    docker logs -f intertidal_mail

### Accessing the Application

    http://localhost:8080/

### Accessing the Database

Command line:

    PGPASSWORD=password psql docker exec -it intertidal_db --username=intertidal intertidal

Through a database management tool:
- Host:`127.0.0.1`
- Port: `15432`
- Username: `intertidal`
- Password: `password`

### Accessing Mailhog (catches emails sent by the app)

    http://localhost:8025/

### Database Migrations

Migrate up to latest

    docker exec -it intertidal_app python manage.py migrate

Create new migrations

    docker exec -it intertidal_app python manage.py makemigrations

## Updating Application Dependencies

### Pip (python)

Manage python dependencies in `requirements.txt`
>All packages should be locked to a specific version number if possible (Ex `Django==4.2.7`)
>Some special packages cannot be locked and should be noted as such (Ex `psycopg[binary]`)

After making changes, you need to run pip or rebuild the image

    docker exec -it intertidal_app pip install -r requirements.txt
    # or
    docker compose up -d --build

#### Update a package

Edit version number in `requirements.txt` with new locked version number
>Ex `pip==24.0.0`

    docker exec -it intertidal_app pip install -r requirements.txt
    # or
    docker compose up -d --build

## Upgrade Postgres Docker version

First turn off everything

    docker compose down

Then backup the postgres data folder

    cp -R .data/postgres .data/postgres-backup

Finally run a handy docker image [pgautoupgrade](https://github.com/pgautoupgrade/docker-pgautoupgrade) for upgrading postgres (match postgres version and make sure to use bookworm to match default postgres linux)

    docker run --rm -it \
        -v ${PWD}/.data/postgres:/var/lib/postgresql/data/pgdata \
        -e POSTGRES_USER=<POSTGRES_USER> \
        -e POSTGRES_PASSWORD=<POSTGRES_PASSWORD> \
        -e PGDATA=/var/lib/postgresql/data/pgdata \
        -e PGAUTO_ONESHOT=yes \
        pgautoupgrade/pgautoupgrade:{VERSION-HERE}-bookworm

example:

    docker run --rm -it \
        -v ${PWD}/.data/postgres:/var/lib/postgresql/data/pgdata \
        -e POSTGRES_USER=intertidal \
        -e POSTGRES_PASSWORD=password \
        -e PGDATA=/var/lib/postgresql/data/pgdata \
        -e PGAUTO_ONESHOT=yes \
        pgautoupgrade/pgautoupgrade:17-bookworm
