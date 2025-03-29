import asyncio
import os
import time
from typing import List


async def delete_old_files(directory: str, days: int) -> List[str]:
    now: float = time.time()
    threshold: float = now - days * 86400

    async def delete_file(file_path: str) -> str:
        await asyncio.to_thread(os.remove, file_path)
        return file_path

    tasks = [
        delete_file(os.path.join(directory, file))
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file)) and os.stat(os.path.join(directory, file)).st_mtime < threshold
    ]

    res = await asyncio.gather(*tasks)
    return res
