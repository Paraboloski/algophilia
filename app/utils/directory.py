import shutil
from pathlib import Path


class Directory:
    def __init__(self, directory: str):
        self._directory = Path(directory)
        self._mkdir()

    def _mkdir(self):
        self._directory.mkdir(parents=True, exist_ok=True)

    def _rmdir(self):
        if self._directory.exists():
            shutil.rmtree(self._directory)

    def write(self, filename: str, content: str):
        path = self._directory / filename
        with path.open("a", encoding="utf-8") as f:
            f.write(f"{content}\n")
