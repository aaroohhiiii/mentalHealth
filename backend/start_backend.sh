#!/bin/bash
cd /Users/karthiksarma/mentalHealth/mentalHealth/backend
export PYTHONNOUSERSITE=1
/Users/karthiksarma/mentalHealth/mentalHealth/backend/venv/bin/python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
