#!/bin/sh
set -e
# Start MLLP server and file watcher
python /app/mllp_server.py &
python /app/watcher.py &
wait -n
