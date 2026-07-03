#!/bin/sh
set -e

# app specific setup here
python manage.py migrate
python manage.py remove_stale_contenttypes --include-stale-apps --noinput

mkdir -p /app/static
MEDIA_FOLDER_UID=${MEDIA_FOLDER_UID-101}
MEDIA_FOLDER_GID=${MEDIA_FOLDER_GID-101}
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /app/static
# collect static if needed
python manage.py collectstatic --noinput

export GIT_COMMIT=$(git rev-parse HEAD)
export GIT_COMMIT_SHORT=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git branch --show-current)
export GIT_TAG=$(git tag --points-at HEAD | head -n 1)

# fix media folder permissions for nginx
mkdir -p /media/audio /media/images
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /media /media/audio /media/images
mkdir -p /static-assets/audio /static-assets/images /static-assets/videos
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /static-assets /static-assets/audio /static-assets/images /static-assets/videos
mkdir -p /static-vite/dist/assets
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /static-vite/dist /static-vite/dist/assets

# ensure django file cache directory exists
mkdir -p /django-cache

reload_extra_files=""
if [[ "$GUNICORN_CMD_ARGS" == *"--reload"* ]]; then
    reload_extra_files=$(find /app/intertidal_app /app/intertidal_project -type f \( -iname "*.html" -or -iname "*.js" -or -iname "*.css" \) -print0 | xargs -0 -I{} printf "--reload-extra-file %s " "{}")
fi
# Set environment variables UVICORN_RELOAD and UVICORN_LOG_LEVEL to override for development
gunicorn --bind 0.0.0.0:80 --no-control-socket \
    --max-requests 100 --max-requests-jitter 10 \
    --log-level error --reload-engine=poll $reload_extra_files \
    intertidal_project.wsgi:application