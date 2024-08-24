#!/bin/bash
set -e

alembic upgrade head
python3.10 -m uvicorn app:app --host 0.0.0.0  --port 8000