import os
import time
from huggingface_hub import HfApi, utils
from functools import wraps

api = HfApi()
repo_id = os.environ.get("HF_REPO")

if not repo_id:
    raise ValueError("HF_REPO environment variable is not set")

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in reversed(range(5)):
            try:
                return func(*args, **kwargs)
            except Exception:
                if not i:
                    raise
                time.sleep(10)
    return wrapper

@retry
def upload_folder():
    api.upload_folder(
        repo_id=repo_id,
        folder_path="output",
        repo_type="dataset",
        commit_message="Update"
    )

utils.disable_progress_bars()
upload_folder()
