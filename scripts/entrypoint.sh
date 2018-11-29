#!/bin/sh
#
# Our entrypoint script:
#  - sets some defaults if not provided
#  - does sanity checks
#  - launches the python script

# Configuration parameters for the nginx endpoint
NGINX_SERVER_URL=${NGINX_SERVER_URL:-"https://demo.nginx.com"}

# Some debug info
echo "DEBUG variables:"
echo "- NGINX_SERVER_URL:   $NGINX_SERVER_URL"
echo ""

./upstreams.py $NGINX_SERVER_URL
