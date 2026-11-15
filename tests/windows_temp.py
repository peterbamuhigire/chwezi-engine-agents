"""Safe cleanup for disposable Git fixtures whose object files are read-only."""

from __future__ import annotations

import os
import shutil
import stat
import tempfile
from pathlib import Path


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def remove_temp_tree(target: Path, fixture_root: Path) -> None:
    """Remove target only inside its verified temporary fixture root.

    On Windows, clear only the read-only bit for a failed deletion and only
    after resolving the path beneath both the target and fixture roots.
    """
    temp_root = Path(tempfile.gettempdir()).resolve(strict=True)
    root = Path(fixture_root).resolve(strict=True)
    tree = Path(target).resolve(strict=True)
    if root == temp_root or not _within(root, temp_root):
        raise ValueError(f"fixture root is not a dedicated temporary directory: {root}")
    if not _within(tree, root):
        raise ValueError(f"cleanup target is outside fixture root: {tree}")

    def onerror(function, failed_path, exc_info) -> None:
        error = exc_info[1]
        failed = Path(failed_path).resolve(strict=False)
        if not _within(failed, root) or not _within(failed, tree):
            raise ValueError(f"refusing cleanup outside verified temporary target: {failed}") from error
        if not isinstance(error, PermissionError):
            raise error
        mode = os.stat(failed_path).st_mode
        if mode & stat.S_IWRITE:
            raise error
        # On Windows this toggles the read-only attribute; it does not grant
        # broad permissions. Keep every other mode bit unchanged.
        os.chmod(failed_path, mode | stat.S_IWRITE)
        function(failed_path)

    shutil.rmtree(tree, onerror=onerror)
