from typing import List
from urllib.parse import urlparse
import hashlib
import re

from fastapi import FastAPI, HTTPException
from models import EmbedRequest, Clip
from highlight_service import HighlightService, TLParams

PROMPT = (
    "Extract segments where someone is stating a fact or making a claim, showing "
    "numbers, or graphs and charts. Prefer segments that are informative "
    "or where the speaker is trying to be convincing."
)
TEMPERATURE = 0.5
MODEL_OPTIONS = ["visual", "audio"]

app = FastAPI(title="Embedding API", version="1.1.0")


def _index_name_from_url(url: str, max_len: int = 63) -> str:
    """
    Make a deterministic, collision-resistant index name from a URL.
    - human-readable slug from host+path
    - short hash suffix to avoid collisions
    - capped length to stay under typical index-name limits
    """
    parsed = urlparse(url)
    base = f"{parsed.netloc}{parsed.path}"
    slug = re.sub(r"[^a-zA-Z0-9\-]+", "-", base).strip("-").lower()
    slug = re.sub(r"-{2,}", "-", slug) or "video"
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    name = f"{slug}-{h}"
    if len(name) > max_len:
        head = max_len - 1 - len(h)
        name = f"{slug[:head]}-{h}"
    return name


@app.post("/highlights", response_model=List[Clip])
def create_highlights(req: EmbedRequest):
    try:
        index_name = _index_name_from_url(str(req.downloadUrl))
        params = TLParams(
            video_url=str(req.downloadUrl),
            index_name=index_name,
            model_options=MODEL_OPTIONS,
        )
        svc = HighlightService(params)
        raw = svc.run(prompt=PROMPT, temperature=TEMPERATURE)

        clips: List[Clip] = []
        for h in raw or []:
            start = h.get("start_sec")
            end = h.get("end_sec")
            text = h.get("highlight_summary") or ""
            if start is None or end is None or not text:
                continue
            clips.append(
                Clip(startSec=float(start), endSec=float(end), description=text)
            )
        return clips
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
