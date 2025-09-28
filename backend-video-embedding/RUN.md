# Backend Video Embedding - Useful Commands

These are the exact commands we used locally to restart the service and exercise the endpoints.

## One-time setup (venv + deps)

```bash
cd "/Users/brycepardo/Documents/Fall 2025/Hackgt/Hackgt25/backend-video-embedding"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Restart the service on port 8001

```bash
# Stop anything on 8001 (ignore errors if nothing is running)
kill -9 $(lsof -ti:8001) 2>/dev/null || true

# Start the FastAPI app
cd "/Users/brycepardo/Documents/Fall 2025/Hackgt/Hackgt25/backend-video-embedding"
. .venv/bin/activate
export TL_API_KEY='REPLACE_WITH_YOUR_KEY'
export TL_INDEX_NAME='video-embedding-index'
export TL_MODEL_NAME='pegasus1.2'
uvicorn main:app --host 0.0.0.0 --port 8001
```

Tip: If you prefer to keep the server running in the background, append ` &` at the end of the `uvicorn` command, then use `jobs` or `ps`/`lsof` to manage it.

## Health check

```bash
sleep 1; curl -sS http://localhost:8001/health
```

## Invoke /embed with a public sample video

```bash
curl -sS -X POST http://localhost:8001/embed \
  -H 'Content-Type: application/json' \
  -d '{"downloadUrl":"https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}'
```

## Notes
- `TL_MODEL_NAME='pegasus1.2'` is recommended for analyze/generate features.
- If you change the port, update the health and embed URLs accordingly.
