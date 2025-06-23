FROM ghcr.io/astral-sh/uv:0.7.12-python3.12-alpine AS builder

# This is just so `stdout` and `stderr` are unbuffered by default
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# This allows statements and log messages to immediately appear in the Knative logs
ENV PYHTONUNBUFFERED=1

# Enable bytecode compilation and Copy from the cache instead of
# linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter
# across both images. If using a managed Python version, it needs to be
# copied from the build image into the final image
ENV UV_PYTHON_DOWNLOADS=0

# Install the project's dependencies using the lockfile and settings
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
	--mount=type=bind,source=uv.lock,target=uv.lock \
	--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked --no-dev

# Then, use a final image without uv
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same
FROM python:3.12-alpine

# This is just so `stdout` and `stderr` are unbuffered by default
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
# This allows statements and log messages to immediately appear in the Knative logs
ENV PYHTONUNBUFFERED=1

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Run the app
CMD ["python", "main.py"]