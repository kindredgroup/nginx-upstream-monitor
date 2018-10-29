FROM python:3.7
MAINTAINER Karel Bemelmans <karel.bemelmans@kindredgroup.com>

# Add our own python modules and make sure they are up to date
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install our own scripts into the container
COPY scripts /

# Run it
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]
