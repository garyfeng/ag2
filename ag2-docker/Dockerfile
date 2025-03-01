# Use the official Python 3.11 slim image as the base
FROM python:3.11-slim

# Install system dependencies:
# - chromium and chromium-driver: to run the browser.
# - xvfb: to create a virtual display.
# - x11vnc: to share the virtual display via VNC.
# - fluxbox: a lightweight window manager.
# - Additional libraries required by Chromium.
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    xvfb \
    x11vnc \
    fluxbox \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable so that AG2’s browser code finds Chromium
ENV CHROME_BIN=/usr/bin/chromium

# Install AG2 with the browser-use extra and Playwright for browser automation.
RUN pip install --no-cache-dir ag2[browser-use] playwright 
RUN playwright install && \
    if [ "$(uname -s)" = "Linux" ]; then playwright install-deps; fi

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Ensure the startup script is executable
RUN chmod +x /app/start.sh

# Expose port 5900 for VNC access
EXPOSE 5900

# Start the container by running the startup script
CMD ["/bin/bash", "/app/start.sh"]
