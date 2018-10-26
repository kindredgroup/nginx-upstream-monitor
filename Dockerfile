FROM python:3
MAINTAINER Karel Bemelmans <karel.bemelmans@kindredgroup.com>

# Install our own scripts into the container
COPY scripts /

# Run it
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]
