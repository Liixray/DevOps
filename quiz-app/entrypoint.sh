#!/bin/sh
set -e

echo "Waiting for MySQL..."
until python - <<PY
import socket, os, time
host=os.environ.get('DATABASE_HOST','mysql')
port=int(os.environ.get('DATABASE_PORT','3306'))
s=socket.socket()
try:
    s.settimeout(1.0)
    s.connect((host,port))
    print("MySQL reachable")
except Exception as e:
    print("Not ready")
    raise SystemExit(1)
finally:
    s.close()
PY
do
  sleep 1
done

echo "Creating tables (if needed)..."
python - <<PY
from db import db
try:
    from app import app
    with app.app_context():
        db.create_all()
except Exception as e:
    print("Create_all failed:", e)
PY

exec gunicorn --bind 0.0.0.0:5000 app:app --log-level info --error-logfile - --access-logfile -