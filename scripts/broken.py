import os
from huggingface_hub import HfApi
from huggingface_hub.hf_api import RepoFile

api = HfApi()
repo_id = os.environ.get("HF_REPO")

if not repo_id:
    raise ValueError("HF_REPO environment variable is not set")

lfs = api.list_lfs_files(
    repo_id=repo_id,
    repo_type="dataset"
)
lfs_oid = {item.oid for item in lfs}

repo = api.list_repo_tree(
    repo_id=repo_id,
    repo_type="dataset",
    recursive=True
)

repo_lfs = [
    item for item in repo
    if isinstance(item, RepoFile) and item.lfs is not None
]

broken = [
    item for item in repo_lfs
    if item.blob_id not in lfs_oid
]

print(f"Broken LFS files (blob_id not in storage): {len(broken)}")
for item in broken:
    print(f" - {item.path}")
    print(f"   blob_id:  {item.blob_id}")
    print(f"   sha256:   {item.lfs.sha256 if item.lfs else None}")
    print(f"   xet_hash: {item.xet_hash}")
    print()
