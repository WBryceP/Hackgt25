import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from typing import List, Dict, Optional
from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.tasks import TasksRetrieveResponse

# Load env from project root and optionally from a module-local .env
load_dotenv(find_dotenv(usecwd=True))
module_env_path = Path(__file__).resolve().parent / ".env"
if module_env_path.exists():
    load_dotenv(module_env_path, override=False)


@dataclass
class TLParams:
    video_url: str
    index_name: str
    model_name: str = "pegasus1.2"
    model_options: Optional[List[str]] = None


class HighlightService:
    def __init__(self, params: TLParams):
        api_key = os.getenv("TL_API_KEY") or os.getenv("TWELVELABS_API_KEY")
        if not api_key:
            raise RuntimeError("TL_API_KEY not set in environment.")
        self.client = TwelveLabs(api_key=api_key)
        self.params = params

    def _status_callback(self, task: TasksRetrieveResponse):
        print(f"  Status={task.status}")

    def run(self, prompt: str, temperature: float) -> List[Dict]:
        """
        Creates an index with Pegasus, uploads the video, waits for indexing,
        then returns a list of highlight dicts (influenced by the prompt).
        """
        # 1) Create index with Pegasus
        index = self.client.indexes.create(
            index_name=self.params.index_name,
            models=[
                IndexesCreateRequestModelsItem(
                    model_name=self.params.model_name,
                    model_options=self.params.model_options or ["visual", "audio"],
                )
            ],
        )
        print(f"Created index: id={index.id}")

        # 2) Create task for the video and wait until ready
        task = self.client.tasks.create(index_id=index.id, video_url=self.params.video_url)
        print(f"Created task: id={task.id}")
        task = self.client.tasks.wait_for_done(task_id=task.id, callback=self._status_callback)

        if task.status != "ready":
            raise RuntimeError(f"Indexing failed with status {task.status}")

        print(f"Upload complete. The unique identifier of your video is {task.video_id}.")

        # 3) Summarize highlights
        res = self.client.summarize(
            video_id=task.video_id,
            type="highlight",
            prompt=prompt,
            temperature=temperature,
        )

        highlights: List[Dict] = []
        if hasattr(res, "highlights") and res.highlights:
            for h in res.highlights:
                highlights.append(
                    {
                        "start_sec": getattr(h, "start_sec", None),
                        "end_sec": getattr(h, "end_sec", None),
                        "highlight": getattr(h, "highlight", None),
                        "highlight_summary": getattr(h, "highlight_summary", None),
                    }
                )

        return highlights