import os
import sys
from huggingface_hub import HfApi, CommitOperationCopy, CommitOperationDelete, RepoFile

api = HfApi()
repo_id = os.environ.get("HF_REPO")

if not repo_id:
    raise ValueError("HF_REPO environment variable is not set")

def get_tree(revision):
    try:
        repo_tree = api.list_repo_tree(
            repo_id=repo_id,
            repo_type="dataset",
            revision=revision,
            recursive=True
        )
        return {
            f.path: f.blob_id for f in repo_tree
            if isinstance(f, RepoFile)
        }
    except Exception:
        return {}

def update_branch(src, dst):
    try:
        api.create_branch(
            repo_id=repo_id,
            repo_type="dataset",
            branch=dst,
            revision=src
        )
        return
    except Exception:
        pass

    dst_tree = get_tree(dst)
    src_tree = get_tree(src)
    ops = []

    for path in dst_tree:
        if path not in src_tree:
            ops.append(CommitOperationDelete(
                path_in_repo=path
            ))

    for path, blob_id in src_tree.items():
        if path not in dst_tree or dst_tree[path] != blob_id:
            ops.append(CommitOperationCopy(
                src_path_in_repo=path,
                path_in_repo=path,
                src_revision=src
            ))

    try:
        commits = api.list_repo_commits(
            repo_id=repo_id,
            repo_type="dataset",
            revision=src
        )
        commit = commits[0].commit_id
    except Exception:
        commit = "unknown"

    if ops:
        api.create_commit(
            repo_id=repo_id,
            repo_type="dataset",
            revision=dst,
            operations=ops,
            commit_message=f"Sync from {src} ({commit})"
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <src> <dst>")
        sys.exit(1)

    update_branch(sys.argv[1], sys.argv[2])
