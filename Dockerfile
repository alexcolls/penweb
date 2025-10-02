# AWS Lambda container image for Penweb Lambda
# Base image: AWS Lambda Python runtime
FROM public.ecr.aws/lambda/python:3.11

# Ensure Python behaves well in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set Lambda task root as working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy application source
COPY src ./src

# Make project source importable
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}/src:${PYTHONPATH}"

# Install runtime dependencies needed by the project
# (Kept minimal; adjust as needed if you add more)
RUN python -m pip install --upgrade pip \
    && pip install requests beautifulsoup4 python-dotenv

# Set the Lambda handler (module.function)
CMD ["lambda.entrypoint.lambda_handler"]


