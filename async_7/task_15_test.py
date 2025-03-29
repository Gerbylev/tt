import asyncio
import os
import time
from pathlib import Path
import pytest

from async_7.task_15 import delete_old_files


@pytest.mark.asyncio
async def test_delete_old_files_deletes_old_files(tmp_path: Path):
    old_file = tmp_path / "old_file.txt"
    old_file.write_text("старое содержимое")
    old_mtime = time.time() - (10 * 86400)
    os.utime(old_file, (old_mtime, old_mtime))

    deleted = await delete_old_files(str(tmp_path), days=5)

    assert old_file.exists() is False
    assert str(old_file) in deleted


@pytest.mark.asyncio
async def test_delete_old_files_preserves_new_files(tmp_path: Path):
    new_file = tmp_path / "new_file.txt"
    new_file.write_text("новое содержимое")

    deleted = await delete_old_files(str(tmp_path), days=5)

    assert new_file.exists() is True
    assert str(new_file) not in deleted


@pytest.mark.asyncio
async def test_delete_old_files_empty_directory(tmp_path: Path):
    deleted = await delete_old_files(str(tmp_path), days=5)
    assert deleted == []


@pytest.mark.asyncio
async def test_delete_old_files_multiple_files(tmp_path: Path):
    files = []
    now = time.time()

    for i in range(10):
        file = tmp_path / f"file_{i}.txt"
        file.write_text(f"Файл {i}")
        file_mtime = now - (i + 1) * 86400
        os.utime(file, (file_mtime, file_mtime))
        files.append((file, file_mtime))

    deleted = await delete_old_files(str(tmp_path), days=5)

    deleted_files_count = sum(1 for file, mtime in files if mtime <= now - 5 * 86400)

    assert len(deleted) == deleted_files_count
    assert all(not file.exists() for file, mtime in files if mtime < now - 5 * 86400)
    assert all(file.exists() for file, mtime in files if mtime > now - 5 * 86400)