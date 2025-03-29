import pytest
import asyncio
from collections import Counter
from async_7.task_9 import analyze_file, analyze_files


@pytest.mark.asyncio
async def test_analyze_file():
    with open("test1.txt", "w", encoding="utf-8") as f:
        f.write("hello world hello")

    word_count, char_count = await analyze_file("test1.txt")

    assert word_count == Counter({"hello": 2, "world": 1})
    assert char_count["h"] == 2  # Проверка на символ


@pytest.mark.asyncio
async def test_analyze_empty_file():
    with open("empty.txt", "w", encoding="utf-8"):
        pass  # Создаём пустой файл

    word_count, char_count = await analyze_file("empty.txt")

    assert word_count == Counter()
    assert char_count == Counter()


@pytest.mark.asyncio
async def test_analyze_files():
    with open("test2.txt", "w", encoding="utf-8") as f:
        f.write("async python async")

    results = await analyze_files(["test1.txt", "test2.txt"])

    assert results["test1.txt"][0]["hello"] == 2
    assert results["test2.txt"][0]["async"] == 2


@pytest.mark.asyncio
async def test_analyze_unicode():
    with open("unicode.txt", "w", encoding="utf-8") as f:
        f.write("Привет мир! Привет")

    word_count, char_count = await analyze_file("unicode.txt")

    assert word_count == Counter({"Привет": 2, "мир!": 1})
    assert char_count["П"] == 2
    assert char_count["р"] == 3
