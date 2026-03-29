import os
import random
import sys
import time
from huggingface_hub import HfApi, utils
from functools import wraps

api = HfApi()

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in reversed(range(60)):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not i:
                    raise
                print(f"\n[RETRY] {type(e).__name__}: {e}\n")
                time.sleep(random.uniform(30, 90))
    return wrapper

@retry
def upload(dst):
    api.sync_bucket("output", f"hf://buckets/{dst}")

utils.disable_progress_bars()

if len(sys.argv) == 2:
    upload(sys.argv[1])
