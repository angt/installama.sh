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

repo = api.list_repo_tree(
    repo_id=repo_id,
    repo_type="dataset",
    recursive=True
)

repo_lfs_blob = {
    item.blob_id for item in repo
    if isinstance(item, RepoFile) and item.lfs is not None
}

lfs_not_in_repo = [
    item for item in lfs
    if item.oid not in repo_lfs_blob
]

print(f"Current LFS blob_ids to keep: {len(repo_lfs_blob)}")
print(f"Old LFS files to delete:      {len(lfs_not_in_repo)}")

if lfs_not_in_repo:
    api.permanently_delete_lfs_files(
        repo_id=repo_id,
        repo_type="dataset",
        rewrite_history=False,
        lfs_files=lfs_not_in_repo,
    )
else:
    print("Nothing to delete.")
