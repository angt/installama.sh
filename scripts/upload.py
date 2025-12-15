import os
import time
import httpx
from huggingface_hub import HfApi, utils

def create_client():
    return httpx.Client(
        timeout=httpx.Timeout(300.0, connect=60.0),
        headers={"user-agent": "upload-folder/1.0"},
        event_hooks={"request": [utils._http.hf_request_event_hook]},
        follow_redirects=True,
    )

def upload_folder():
    api = HfApi()
    for attempt in range(1, 6):
        try:
            api.upload_folder(
                repo_id=os.environ.get("HF_REPO"),
                folder_path="output",
                repo_type="dataset",
                allow_patterns="*.zst",
                commit_message="Update"
            )
            return
        except Exception as e:
            print(f"Upload failed: {e}")
            time.sleep(10 * attempt)

    raise Exception("Upload failed")

if __name__ == "__main__":
    utils.disable_progress_bars()
    utils.set_client_factory(create_client)
    upload_folder()
