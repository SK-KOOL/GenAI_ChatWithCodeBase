import os
import shutil
import stat
import time
import uuid

from git import Repo

BASE_DIR = "app/repositories"

os.makedirs(BASE_DIR, exist_ok=True)


def remove_readonly(func, path, _):
    """
    Clear readonly bit and reattempt delete
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_delete(path):

    if not os.path.exists(path):
        return

    retries = 5

    for i in range(retries):

        try:

            shutil.rmtree(
                path,
                onerror=remove_readonly
            )

            break

        except PermissionError:

            time.sleep(1)

            if i == retries - 1:
                raise Exception(
                    f"Unable to delete repository: {path}"
                )


def clone_repository(repo_url: str):

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_name = f"{repo_name}_{uuid.uuid4().hex[:8]}"
    repo_path = os.path.join(BASE_DIR, repo_name)

    safe_delete(repo_path)

    Repo.clone_from(repo_url, repo_path)

    return repo_path