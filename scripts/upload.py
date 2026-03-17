import os
import time
import httpx
from huggingface_hub import HfApi, utils

def create_client():
    return httpx.Client(
        timeout=httpx.Timeout(60.0),
        headers={"user-agent": "upload-folder/1.0"},
        event_hooks={"request": [utils._http.hf_request_event_hook]},
        follow_redirects=True,
    )

def upload_folder():
    api = HfApi()
    for i in reversed(range(5)):
        try:
            api.upload_folder(
                repo_id=os.environ.get("HF_REPO"),
                folder_path="output",
                repo_type="dataset",
                commit_message="Update"
            )
            return
        except Exception:
            if not i:
                raise
            time.sleep(10)

if __name__ == "__main__":
    utils.disable_progress_bars()
    utils.set_client_factory(create_client)
    upload_folder()
