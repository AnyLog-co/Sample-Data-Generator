import os
import subprocess
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__).split(".github", 1)[0], "setup.cfg")


def get_git_info():
    try:
        commit = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        branch = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        return commit, branch

    except subprocess.CalledProcessError as e:
        print(f"Error getting Git info: {e}")
        return None, None


def update_version():
    commit_id, branch = get_git_info()
    formatted_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    short_commit = commit_id[:6] if commit_id else "Missing Git ID"
    git_suffix = f"({branch} - {short_commit} [{formatted_now}])"

    lines = []
    with open(CONFIG_FILE, "r") as f:
        for line in f:
            if line.strip().startswith("version"):
                # Extract base version (e.g. "1.4.2603"), strip any existing {} suffix
                raw = line.split("=", 1)[1].strip()
                base_version = raw.split("(")[0].strip()
                line = f"version = {base_version} {git_suffix}\n"
            lines.append(line)

    with open(CONFIG_FILE, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    update_version()