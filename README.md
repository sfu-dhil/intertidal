[![Docker Image Latest Badge](https://ghcr-badge.egpl.dev/sfu-dhil/intertidal/latest_tag?trim=major&label=latest)](https://github.com/sfu-dhil/intertidal/pkgs/container/intertidal)
[![Docker Image Size badge](https://ghcr-badge.egpl.dev/sfu-dhil/intertidal/size)](https://github.com/sfu-dhil/intertidal/pkgs/container/intertidal)

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
    docker logs -f intertidal_vite
    docker logs -f intertidal_nginx
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

### Yarn (javascript)

    # add new package
    docker exec -it intertidal_vite yarn add [package]

    # update a package
    docker exec -it intertidal_vite yarn upgrade [package]

    # update all packages
    docker exec -it intertidal_vite yarn upgrade

After you update a dependency make sure to rebuild the images

    docker compose down
    docker compose up -d --build

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

Setup the new version dir

    sudo mkdir -p .data/postgres/<NEW POSTGRES VERSION>/docker
    sudo chown 999:999 -R .data/postgres/<NEW POSTGRES VERSION>
    # example:
    sudo mkdir -p .data/postgres/18/docker
    sudo chown 999:999 -R .data/postgres/18


Using `https://github.com/tianon/docker-postgres-upgrade` to upgrade the postgres version

    docker run --rm \
        --volume .data/postgres:/var/lib/postgresql \
        --env PGDATAOLD=/var/lib/postgresql/<OLD POSTGRES VERSION>/docker \
        --env PGDATANEW=/var/lib/postgresql/<NEW POSTGRES VERSION>/docker \
        --env POSTGRES_USER=intertidal \
        --env POSTGRES_PASSWORD=password \
        tianon/postgres-upgrade:<OLD POSTGRES VERSION>-to-<NEW POSTGRES VERSION> \
        --link

example:

    docker run --rm \
        --volume .data/postgres:/var/lib/postgresql \
        --env PGDATAOLD=/var/lib/postgresql/17/docker \
        --env PGDATANEW=/var/lib/postgresql/18/docker \
        --env POSTGRES_USER=intertidal \
        --env POSTGRES_PASSWORD=password \
        tianon/postgres-upgrade:17-to-18 \
        --link

## Multi-resolution backdrop video

Install `ffmpeg` (via homebrew): `brew install ffmpeg`

Generate the Dash (with HLS fallback) video (see [DASH Adaptive Streaming for HTML video](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API/DASH_Adaptive_Streaming) for general guidelines):

```shell
# setup some env variables (makes it a bit easier) and directories
export STATIC_VIDEO_DIR=".data/static-assets/videos"
export WORKING_DIR=".data"
export BACKDROP_DIR="$STATIC_VIDEO_DIR/backdrop"
# export BACKDROP_2_DIR="$STATIC_VIDEO_DIR/backdrop_test_2"
mkdir -p $BACKDROP_DIR

# generate stabilised version of Beach_original.MOV (slightly less shaky but zoomed in a bit)
ffmpeg -i $STATIC_VIDEO_DIR/Beach_original.MOV -vf vidstabdetect=shakiness=9:accuracy=90 -f null -; ffmpeg -i $STATIC_VIDEO_DIR/Beach_original.MOV -vf vidstabtransform=input=transforms.trf:smoothing=30:zoom=5:crop=black,unsharp=5:5:1.0:5:5:0.0 $WORKING_DIR/Beach_stabilised.MOV

# add a 1 second fade in and out to the stabilised video
ffmpeg -i $WORKING_DIR/Beach_stabilised.MOV -vf "fade=t=in:st=0:d=1,fade=t=out:st=31:d=1" -c:a copy $WORKING_DIR/Beach_stabilised_fade.MOV

# generate dash manifest and HLS fallback
ffmpeg -i $WORKING_DIR/Beach_stabilised_fade.MOV \
    -map 0:v -map 0:v -map 0:v -map 0:a \
    -s:v:0 640x360 -b:v:0 1200k \
    -s:v:1 1280x720 -b:v:1 2500k \
    -s:v:2 1920x1080 -b:v:2 4500k \
    -c:a aac -b:a 256k \
    -c:v libsvtav1 \
    -f dash \
    -adaptation_sets "id=0,streams=v id=1,streams=a" \
    -seg_duration 2 -sc_threshold 0 -b_strategy 0 -g 100 -keyint_min 100 \
    -use_timeline 1 -use_template 1 -hls_playlist 1 \
    $BACKDROP_DIR/master.mpd
```

## Audio files (convert to ogg)


```shell
# setup some env variables (makes it a bit easier) and directories
export STATIC_AUDIO_DIR=".data/static-assets/audio"

# generate ogg files
ffmpeg -i $STATIC_AUDIO_DIR/intertidal_draft_ambient_soundscape.wav -acodec aac $STATIC_AUDIO_DIR/intertidal_draft_ambient_soundscape.m4a
```