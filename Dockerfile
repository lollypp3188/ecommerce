# Use a specific version of Python on Alpine for a small image footprint
FROM python:3.11.9-alpine3.20

# Ensure Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Copy the requirement files first for caching
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the application source code
COPY ./app /app

# Create and prepare the scripts directory
RUN mkdir -p /scripts
COPY ./entrypoint.sh /scripts/entrypoint.sh

# Set the working directory
WORKDIR /app

# Expose port 8000 for the application
EXPOSE 8000

# Toggle for development mode
ARG DEV=false

# Create a virtual environment and upgrade pip
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

# Install runtime dependencies for your app
RUN apk add --update --no-cache postgresql-client jpeg-dev zlib-dev

# Install build dependencies required during the build stage
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib-dev jpeg-dev linux-headers

# Install Python dependencies
RUN /py/bin/pip install -r /tmp/requirements.txt

# Conditionally install development dependencies
RUN if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi

# Cleanup temporary files and remove build dependencies
RUN rm -rf /tmp && \
    apk del .tmp-build-deps

# Add a non-root user and setup necessary directories for runtime
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# Set the environment path to include script and virtual env binaries
ENV PATH="/scripts:/py/bin:$PATH"

# Switch to non-root user for security
USER django-user

# Set the entrypoint script
ENTRYPOINT ["/scripts/entrypoint.sh"]

# Default command to execute
CMD ["run.sh"]
