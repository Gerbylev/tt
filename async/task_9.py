import asyncio
import aiofiles
from collections import Counter
from typing import Dict, Tuple, List

async def analyze_text_file(file_path: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    word_counter: Counter = Counter()
    char_counter: Counter = Counter()
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        async for line in f:
            words = line.strip().split()
            word_counter.update(word.lower() for word in words if word)
            char_counter.update(char for char in line if not char.isspace())
    return dict(word_counter), dict(char_counter)

async def analyze_files(file_paths: List[str]) -> Tuple[Dict[str, int], Dict[str, int]]:
    tasks = [analyze_text_file(path) for path in file_paths]
    results = await asyncio.gather(*tasks)
    total_word_counter: Counter = Counter()
    total_char_counter: Counter = Counter()
    for word_freq, char_freq in results:
        total_word_counter.update(word_freq)
        total_char_counter.update(char_freq)
    return dict(total_word_counter), dict(total_char_counter)