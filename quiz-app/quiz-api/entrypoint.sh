#!/bin/sh
set -e

echo "Waiting for MySQL..."
until python - <<PY
import socket, os, sys
host=os.environ.get('DATABASE_HOST','mysql')
port=int(os.environ.get('DATABASE_PORT','3306'))
s=socket.socket()
try:
    s.settimeout(1.0)
    s.connect((host, port))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
do
  echo "MySQL not ready, sleeping 1s..."
  sleep 1
done

echo "Initializing DB (create tables and seed)..."
# db.py already exposes init and seeding when run as __main__
python db.py || echo "db.py failed; continuing"

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 app:app --log-level info --error-logfile - --access-logfile -
