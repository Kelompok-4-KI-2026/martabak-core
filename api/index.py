"""Vercel serverless entrypoint for the Martabak Core FastAPI app.

Vercel's @vercel/python runtime exposes the ASGI ``app`` object found in this
file. The real application lives in ``main.py`` at the project root; we add the
project root to ``sys.path`` so its imports (core/, routers/, models/, ...)
resolve regardless of the runtime working directory.

Required environment variables (set in Vercel dashboard, NOT via .env):
    SECRET_KEY, DATABASE_URL,
    SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import app  # noqa: E402,F401  (FastAPI instance - Vercel detects `app`)
