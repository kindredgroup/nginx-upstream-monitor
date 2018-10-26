#!/bin/sh
#
# Our entrypoint script:
#  - sets some defaults if not provided
#  - does sanity checks
#  - launches the python script

# Defaults
POST_WARNINGS=${POST_WARNINGS:-true}
POST_ERRORS=${POST_ERRORS:-true}

# Configuration parameters for the nginx endpoint
NGINX_SERVER_URL=${NGINX_SERVER_URL:-"http://localhost:8080"}

# Some debug info
echo "DEBUG variables:"
echo "- POST_WARNINGS:      $POST_WARNINGS"
echo "- POST_ERRORS:        $POST_ERRORS"
echo ""
echo "- NGINX_SERVER_URL:   $NGINX_SERVER_URL"

./upstreams.py $NGINX_SERVER_URL

