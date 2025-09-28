import os, time, requests

BASE = "https://api.youtubedownloadapi.com/v1"

def download_to_disk(youtube_url: str, out_path: str, quality: int = 720, rapidapi_key: str | None = None):
    key = rapidapi_key or os.getenv("RAPIDAPI_KEY")
    if not key:
        raise RuntimeError("RAPIDAPI_KEY not set")

    H = {
        "Content-Type": "application/json",
        "x-rapidapi-key": key,
        "X-RapidAPI-Host": "yt-video-audio-downloader-api.p.rapidapi.com",
    }
    # start
    r = requests.post(f"{BASE}/download", headers=H,
                      json={"url": youtube_url, "format": "mp4", "quality": quality})
    r.raise_for_status()
    jobId = r.json()["jobId"]
    # poll
    while True:
        s = requests.get(f"{BASE}/status/{jobId}", headers=H).json()
        if s["status"] == "error":
            raise RuntimeError(s.get("message", "download failed"))
        if s["status"] == "ready":
            filename = s["filename"]
            break
        time.sleep(2)
    # fetch
    with requests.get(f"{BASE}/file/{jobId}/{filename}", headers=H, stream=True) as resp:
        resp.raise_for_status()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
    return {"path": out_path}
