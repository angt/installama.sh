import os
from datetime import datetime, timedelta, timezone
from huggingface_hub import HfApi

api = HfApi()
repo_id = os.environ.get("HF_REPO")
date = datetime.now(timezone.utc) - timedelta(days=60)

if not repo_id:
    raise ValueError("HF_REPO environment variable is not set")

files = api.list_lfs_files(
    repo_id=repo_id,
    repo_type="dataset",
)

old = [f for f in files if f.pushed_at < date]

for f in old:
    print(f" - {f.pushed_at}  {f.filename}")

if old:
    api.permanently_delete_lfs_files(
        repo_id=repo_id,
        repo_type="dataset",
        rewrite_history=False,
        lfs_files=old,
    )
