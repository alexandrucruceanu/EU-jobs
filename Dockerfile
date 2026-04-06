# Stage 1: Data Build
FROM python:3.11-slim AS builder

WORKDIR /app

# Non-interactive shell
ENV DEBIAN_FRONTEND=noninteractive

# Copy necessary files for the data build
COPY scripts/ /app/scripts/
COPY data/ /app/data/
COPY site/ /app/site/

# Ensure the output directory exists
RUN mkdir -p /app/site

# Run the build script to generate the JSON data files
# build_site_data.py only uses standard libraries (csv, json, os, glob, shutil)
RUN python scripts/build_site_data.py

# Stage 2: Runtime (Nginx)
FROM nginx:alpine

# Copy the built site content
COPY --from=builder /app/site /usr/share/nginx/html

# Copy custom Nginx configuration for security hardening
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
