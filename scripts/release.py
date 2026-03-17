import os
from huggingface_hub import HfApi

api = HfApi()
repo_id = os.environ.get("HF_REPO")

if not repo_id:
    raise ValueError("HF_REPO environment variable is not set")

api.create_branch(
    repo_id=repo_id,
    repo_type="dataset",
    branch="main",
    revision="latest",
    exist_ok=True,
)
