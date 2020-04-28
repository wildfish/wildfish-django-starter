FROM python:3.8-slim

RUN mkdir /build
WORKDIR /build

# Build process dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Full python requirements to support development
COPY ./requirements.txt /build/requirements.txt
RUN pip install -r requirements.txt

# Run Django
WORKDIR /project
CMD ["/project/dev-docker/django/run.sh"]