FROM python:3-alpine

ARG SECRET_KEY=notset
ARG ALLOWED_HOSTS=localhost, 127.0.0.1, ::1, testserver

WORKDIR /app/polls

# Set needed settings
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=True
ENV TIMEZONE=Asia/Bangkok
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}

# Test for secret key
RUN if [ -z "$SECRET_KEY" ]; then echo "No secret key specified in build-arg"; exit 1; fi

# Copy Files
COPY ./requirements.txt .

# Install Dependencies in docker container
RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000

# Run applications
CMD ["./entrypoint.sh"]
