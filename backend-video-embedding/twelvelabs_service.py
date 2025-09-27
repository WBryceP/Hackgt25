import os
import json
import time
import httpx
from fastapi import HTTPException
from typing import List
from twelvelabs import TwelveLabs


class TwelveLabsService:
    def __init__(self):
        api_key = os.getenv("TL_API_KEY") or os.getenv("TWELVELABS_API_KEY")
        if not api_key:
            raise ValueError("TWELVELABS API key missing. Set TL_API_KEY or TWELVELABS_API_KEY")
        # Initialize SDK client (avoid passing timeout kwarg for compatibility across versions)
        self.client = TwelveLabs(api_key=api_key)
        # Optional REST timeout for fallback HTTP calls
        timeout = None
        try:
            timeout_env = os.getenv("TL_TIMEOUT")
            if timeout_env:
                timeout = float(timeout_env)
        except Exception:
            timeout = None
        self.index_id = None
        # REST fallback client
        self._api_key = api_key
        self._base_url = os.getenv("TL_BASE_URL", "https://api.twelvelabs.io/v1.3")
        self._http = httpx.Client(timeout=timeout or 60)

    async def ensure_index(self) -> str:
        try:
            if self.index_id:
                return self.index_id

            index_name = os.getenv("TL_INDEX_NAME", "video-embedding-index")
            model_name = os.getenv("TL_MODEL_NAME", "pegasus1.2")
            # Try SDK list, else REST list
            found_id = None
            try:
                if hasattr(self.client, "indexes") and hasattr(self.client.indexes, "list"):
                    indexes = self.client.indexes.list()
                    for idx in indexes:
                        if getattr(idx, "index_name", None) == index_name and getattr(idx, "id", None):
                            found_id = idx.id
                            break
                else:
                    raise AttributeError("indexes not available on SDK")
            except Exception:
                # REST fallback list
                resp = self._http.get(f"{self._base_url}/indexes", headers={"x-api-key": self._api_key})
                if resp.status_code == 200:
                    data = resp.json()
                    # API returns { "data": [ ... ], "page_info": {...} }
                    items = None
                    if isinstance(data, dict):
                        items = data.get("data") or data.get("items")
                    if items is None and isinstance(data, list):
                        items = data
                    if isinstance(items, list):
                        for idx in items:
                            try:
                                if idx.get("index_name") == index_name:
                                    found_id = idx.get("id") or idx.get("_id")
                                    if found_id:
                                        break
                            except Exception:
                                continue

            if not found_id:
                # Create index via SDK, else REST
                try:
                    if hasattr(self.client, "indexes") and hasattr(self.client.indexes, "create"):
                        index = self.client.indexes.create(
                            index_name=index_name,
                            models=[{"model_name": model_name, "model_options": ["visual", "audio"]}],
                        )
                        found_id = getattr(index, "id", None)
                    else:
                        raise AttributeError("indexes.create not available on SDK")
                except Exception:
                    payload = {
                        "index_name": index_name,
                        "models": [{"model_name": model_name, "model_options": ["visual", "audio"]}],
                    }
                    resp = self._http.post(
                        f"{self._base_url}/indexes",
                        headers={"x-api-key": self._api_key, "Content-Type": "application/json"},
                        json=payload,
                    )
                    if resp.status_code >= 400:
                        raise HTTPException(status_code=resp.status_code, detail=resp.text)
                    try:
                        j = resp.json()
                    except Exception:
                        j = {}
                    found_id = (j.get("id") or j.get("_id"))

            if not found_id:
                raise HTTPException(status_code=500, detail="Failed to create TwelveLabs index")
            self.index_id = found_id
            return self.index_id
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Error ensuring index: {str(e)}")

    async def submit_video(self, download_url: str) -> str:
        try:
            if not self.index_id:
                await self.ensure_index()
            # Ensure plain string for SDK and REST payloads
            download_url_str = str(download_url)
            task_id = None
            try:
                if hasattr(self.client, "tasks") and hasattr(self.client.tasks, "create"):
                    task = self.client.tasks.create(index_id=self.index_id, video_url=download_url_str)
                    task_id = getattr(task, "id", None)
                else:
                    raise AttributeError("tasks.create not available on SDK")
            except Exception:
                # REST fallback requires multipart/form-data
                files = {
                    "index_id": (None, self.index_id),
                    "video_url": (None, download_url_str),
                }
                resp = self._http.post(
                    f"{self._base_url}/tasks",
                    headers={"x-api-key": self._api_key},
                    files=files,
                )
                if resp.status_code >= 400:
                    raise HTTPException(status_code=resp.status_code, detail=resp.text)
                try:
                    j = resp.json()
                except Exception:
                    j = {}
                task_id = j.get("id") or j.get("_id")
                if not task_id:
                    raise HTTPException(status_code=500, detail="Failed to create video indexing task")
                return task_id
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            # Try to surface richer info from SDK/HTTP errors if present
            detail = None
            for attr in ("body", "message", "detail"):
                try:
                    v = getattr(e, attr, None)
                    if v:
                        detail = v
                        break
                except Exception:
                    pass
            if not detail:
                try:
                    detail = e.args[0] if e.args else str(e)
                except Exception:
                    detail = str(e)
            raise HTTPException(status_code=500, detail=f"Error submitting video: {detail}")

    async def poll_until_ready(self, task_id: str) -> str:
        try:
            def on_task_update(task):
                # Keep simple logging; avoid additional features
                try:
                    print(f"  Status={getattr(task, 'status', 'unknown')}")
                except Exception:
                    pass

            try:
                task = self.client.tasks.wait_for_done(
                    sleep_interval=5, task_id=task_id, callback=on_task_update
                )
                status = getattr(task, "status", None)
                video_id = getattr(task, "video_id", None)
            except Exception:
                status = None
                video_id = None
                # REST polling fallback
                for _ in range(720):  # up to an hour
                    resp = self._http.get(
                        f"{self._base_url}/tasks/{task_id}", headers={"x-api-key": self._api_key}
                    )
                    if resp.status_code >= 400:
                        raise HTTPException(status_code=resp.status_code, detail=resp.text)
                    t = resp.json()
                    status = t.get("status")
                    video_id = t.get("video_id")
                    try:
                        print(f"  Status={status}")
                    except Exception:
                        pass
                    if status in ("ready", "failed", "canceled"):
                        break
                    time.sleep(5)

            if status != "ready":
                raise HTTPException(status_code=500, detail=f"Indexing failed with status {status}")
            if not video_id:
                raise HTTPException(status_code=500, detail="Missing video_id after indexing")
            return video_id
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error polling task: {str(e)}")

    async def get_task_status(self, task_id: str) -> dict:
        try:
            task = self.client.tasks.retrieve(task_id)
            # The SDK returns a TasksRetrieveResponse; map to a simple dict
            status = getattr(task, "status", "unknown") or "unknown"
            progress_pct = None
            # Some SDKs expose progress as percentage or step counts; be defensive
            if hasattr(task, "progress"):
                try:
                    progress = getattr(task, "progress")
                    if isinstance(progress, (int, float)):
                        progress_pct = float(progress)
                except Exception:
                    progress_pct = None
            return {
                "status": status,
                "progressPct": progress_pct if progress_pct is not None else 0,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving task status: {str(e)}")

    async def run_filter(self, video_id: str):
        try:
            prompt = (
                "Identify all contiguous time spans where: "
                "(a) a claim or factual assertion is spoken or clearly stated, "
                "(b) statistics, numbers, percentages, dates, or counts are mentioned, or "
                "(c) charts/graphs/tables or numeric overlays appear on screen. "
                "Return concise clips that begin slightly before and end shortly after the relevant content so the context is preserved. "
                "Keep descriptions short and concrete."
            )

            schema = {
                "type": "object",
                "properties": {
                    "clips": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "startSec": {"type": "number"},
                                "endSec": {"type": "number"},
                                "audioDescription": {"type": "string"},
                                "visualDescription": {"type": "string"},
                                "hasStatistic": {"type": "boolean"},
                                "statisticText": {"type": "string"},
                                "hasGraphic": {"type": "boolean"},
                                "graphicDescription": {"type": "string"},
                                "reason": {"type": "string"},
                            },
                            "required": [
                                "startSec",
                                "endSec",
                                "audioDescription",
                                "visualDescription",
                            ],
                        },
                    }
                },
                "required": ["clips"],
            }

            try:
                res = self.client.analyze(
                    video_id=video_id,
                    prompt=prompt,
                    max_tokens=2048,
                    response_format={
                        "type": "json_schema",
                        "json_schema": schema,
                    },
                )
            except Exception:
                # Fallback to built-in highlights if analyze is unavailable or fails
                return await self.get_highlights(video_id)

            # Normalize SDK response into a plain dict
            data = None
            if hasattr(res, "model_dump"):
                try:
                    data = res.model_dump()
                except Exception:
                    data = None
            if data is None and hasattr(res, "data"):
                payload = res.data
                if isinstance(payload, (str, bytes)):
                    try:
                        data = json.loads(payload)
                    except Exception:
                        data = None
                elif isinstance(payload, dict):
                    data = payload

            if not data or "clips" not in data or not isinstance(data["clips"], list):
                return []

            clips: List[dict] = []
            for c in data["clips"]:
                try:
                    start_sec = float(c.get("startSec", 0.0) or 0.0)
                    end_sec = float(c.get("endSec", 0.0) or 0.0)
                    audio_desc = str(c.get("audioDescription", "") or "")
                    visual_desc = str(c.get("visualDescription", "") or "")
                except Exception:
                    continue

                if end_sec <= start_sec:
                    continue

                # Combine into a single description for API compatibility
                if audio_desc and visual_desc:
                    description = f"Audio: {audio_desc} | Visuals: {visual_desc}"
                elif audio_desc:
                    description = f"Audio: {audio_desc}"
                elif visual_desc:
                    description = f"Visuals: {visual_desc}"
                else:
                    description = ""

                clips.append(
                    {
                        "startSec": start_sec,
                        "endSec": end_sec,
                        "description": description,
                    }
                )

            return clips
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error running filter: {str(e)}")

    async def get_highlights(self, video_id: str) -> List[dict]:
        try:
            res = self.client.summarize(video_id=video_id, type="highlight")
            clips: List[dict] = []
            if hasattr(res, "highlights") and res.highlights:
                for h in res.highlights:
                    # Expect fields: highlight, start_sec, end_sec
                    start_val = getattr(h, "start_sec", 0.0) or 0.0
                    end_val = getattr(h, "end_sec", 0.0) or 0.0
                    # Enforce positive non-zero duration; pad if necessary
                    if end_val <= start_val:
                        end_val = start_val + 2.0
                    desc = getattr(h, "highlight", "") or "Highlight"
                    clips.append(
                        {
                            "startSec": float(start_val),
                            "endSec": float(end_val),
                            "description": str(desc),
                        }
                    )
            return clips
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving highlights: {str(e)}")

