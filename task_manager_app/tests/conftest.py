import os
import sys


def _read_env_file(path: str) -> dict:
    """Very small .env parser: KEY=VALUE, ignores comments and blank lines."""
    data = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                k, v = line.split('=', 1)
                data[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return data


# Ensure tests can import the application packages regardless of cwd
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..'))  # task_manager_app
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
PARENT = os.path.abspath(os.path.join(PROJECT_ROOT, '..'))

# Optional: load overrides from a .env file located at project root
env = _read_env_file(os.path.join(PROJECT_ROOT, '.env'))

def _abs_from_project_root(value: str) -> str:
    if os.path.isabs(value):
        return value
    return os.path.abspath(os.path.join(PROJECT_ROOT, value))

if 'SRC_DIR' in env:
    SRC_DIR = _abs_from_project_root(env['SRC_DIR'])
if 'REPO_ROOT' in env:
    PROJECT_ROOT = _abs_from_project_root(env['REPO_ROOT'])
if 'PARENT' in env:
    PARENT = _abs_from_project_root(env['PARENT'])

for path in (SRC_DIR, PROJECT_ROOT, PARENT):
    if path and path not in sys.path:
        sys.path.insert(0, path)

# Change working directory to the `src` dir so relative KV file loads like
# "views/Input.kv" resolve to `src/views/...` which exists in the repo.
try:
    os.chdir(SRC_DIR)
except Exception:
    # If SRC_DIR doesn't exist, keep current cwd; tests may handle missing files.
    pass

