import asyncio
from time import sleep

import aiofiles
from collections import Counter
from typing import Dict, Tuple, List

async def analyze_file(file_path: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        text: str = await f.read()
    words: List[str] = text.split()
    word_count: Dict[str, int] = dict(Counter(words))
    char_count: Dict[str, int] = dict(Counter(text))
    return word_count, char_count

async def analyze_files(file_paths: List[str]) -> Dict[str, Tuple[Dict[str, int], Dict[str, int]]]:
    tasks = [analyze_file(path) for path in file_paths]
    results = await asyncio.gather(*tasks)
    return {file_path: result for file_path, result in zip(file_paths, results)}


async def main() -> None:
    print("=== Демонстрация анализа файлов ===")
    files: List[str] = ['input1.txt', 'input2.txt']
    results = await analyze_files(files)
    for file, (word_count, char_count) in results.items():
        print(f"\nФайл: {file}")
        print("Частота слов:", word_count)
        print("Распределение символов:", char_count)



if __name__ == "__main__":
    asyncio.run(main())