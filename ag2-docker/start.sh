# start.sh
#!/bin/bash
set -e

# Start Xvfb on display :99 with a screen size of 1280x800 and 24-bit color depth.
Xvfb :99 -screen 0 1280x800x24 &
export DISPLAY=:99

# Start a minimal window manager (fluxbox) for managing windows in X.
fluxbox &

# Start x11vnc to share the Xvfb display on port 5900.
# -nopw: no password required (adjust for production!)
# -forever: keep running after a client disconnects.
# -shared: allow multiple clients to connect.
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 &

# Give services time to initialize.
sleep 3

# Now run your Python script (which will launch the headless browser)
python websurferagent_test.py
