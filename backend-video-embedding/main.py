import os, asyncio
from typing import Iterable, List, Optional
from urllib.parse import urlparse
import hashlib
import re

from fastapi import FastAPI, HTTPException
from models import EmbedRequest, Clip, FactCheckResponse, EnrichedClip
import httpx
from highlight_service import HighlightService, TLParams

RESEARCH_HOST = os.getenv("RESEARCH_HOST", "http://backend-research:8000")
FACTCHECK_PATH = "/fact-check"                        # lives on backend-research
FACTCHECK_TIMEOUT = float(os.getenv("FACTCHECK_TIMEOUT", "30"))
FACTCHECK_RPS = int(os.getenv("FACTCHECK_RPS", "3"))  # <= 3 requests per second
HIGHLIGHTS_TIMEOUT = float(os.getenv("HIGHLIGHTS_TIMEOUT", "60"))

PROMPT = (
    "Extract segments where someone is stating a fact or making a claim, showing "
    "numbers, or graphs and charts. Prefer segments that are informative "
    "or where the speaker is trying to be convincing. In your summary "
    "be sure to include the fact or claim they are making in detail."
)
TEMPERATURE = 0.5
MODEL_OPTIONS = ["visual", "audio"]
TEST_FLAG = True

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
            test_flag=TEST_FLAG,
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

def chunked(seq: List, n: int) -> Iterable[List]:
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

async def call_factcheck(client: httpx.AsyncClient, clip: "Clip") -> Optional[FactCheckResponse]:
    """
    Calls backend-research /fact-check with the NEW request schema:
      { startSec, endSec, claim }
    Maps response to FactCheckResponse (which includes startSec/endSec as well).
    """
    try:
        payload = {
            "startSec": clip.startSec,
            "endSec": clip.endSec,
            "claim": clip.description,
        }
        resp = await client.post(f"{RESEARCH_HOST}{FACTCHECK_PATH}", json=payload)
        if resp.status_code >= 400:
            return None
        data = resp.json()
        return FactCheckResponse(**data)
    except Exception:
        return None
    
@app.post("/highlights_enriched", response_model=List[EnrichedClip])
async def create_highlights_enriched(req: "EmbedRequest"):
    """
    1) Generate clips (same logic as /highlights)
    2) For each clip, call backend-research /fact-check with {startSec,endSec,claim}
    3) Enforce ≤ 3 requests per second (FACTCHECK_RPS)
    4) Return [{ clip, factCheck }, ...]
    """
    # step 1: get clips
    try:
        index_name = _index_name_from_url(str(req.downloadUrl))
        params = TLParams(
            video_url=str(req.downloadUrl),
            index_name=index_name,
            model_options=MODEL_OPTIONS,
            test_flag=TEST_FLAG,
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
            clips.append(Clip(startSec=float(start), endSec=float(end), description=text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"highlights error: {e}")

    if not clips:
        return []

    # step 2–3: rate-limit fact-check calls (batches of size FACTCHECK_RPS, ~1s between)
    enriched: List[EnrichedClip] = []
    async with httpx.AsyncClient(timeout=FACTCHECK_TIMEOUT) as client:
        for batch in chunked(clips, max(1, FACTCHECK_RPS)):
            tasks = [call_factcheck(client, c) for c in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=False)
            for c, fc in zip(batch, batch_results):
                enriched.append(EnrichedClip(clip=c, factCheck=fc))

            if len(enriched) < len(clips):
                await asyncio.sleep(1.05)  # small cushion to stay under 3/sec

    return enriched