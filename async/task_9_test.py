import os
from collections import Counter
from typing import Dict

from task_9 import analyze_text_file, analyze_files
import pytest
import shutil



@pytest.mark.asyncio
async def test_analyze_single_file(tmp_path):
    content: str = "Hello world hello"
    file_path = tmp_path / "test.txt"
    file_path.write_text(content, encoding='utf-8')

    word_freq, char_dist = await analyze_text_file(str(file_path))

    expected_words = {"hello": 2, "world": 1}
    expected_chars = Counter(c for c in content if not c.isspace())
    assert word_freq == expected_words
    assert char_dist == dict(expected_chars)


@pytest.mark.asyncio
async def test_analyze_multiple_files(tmp_path):
    content1: str = "Python asyncio test"
    content2: str = "Test asyncio Python"
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text(content1, encoding='utf-8')
    file2.write_text(content2, encoding='utf-8')

    word_freq, char_dist = await analyze_files([str(file1), str(file2)])

    expected_words: Dict[str, int] = {}
    for word in (content1 + " " + content2).split():
        lw = word.lower()
        expected_words[lw] = expected_words.get(lw, 0) + 1
    expected_chars = Counter(c for c in (content1 + content2) if not c.isspace())

    assert word_freq == expected_words
    assert char_dist == dict(expected_chars)


@pytest.mark.asyncio
async def test_analyze_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding='utf-8')

    word_freq, char_dist = await analyze_text_file(str(file_path))

    assert word_freq == {}
    assert char_dist == {}


@pytest.mark.asyncio
async def test_analyze_shakespeare_files(tmp_path):
    if not (os.path.exists("input1.txt") and os.path.exists("input2.txt")):
        pytest.skip("Файлы input1.txt и/или input2.txt не найдены в текущей директории.")

    file1 = tmp_path / "input1.txt"
    file2 = tmp_path / "input2.txt"
    shutil.copy("input1.txt", file1)
    shutil.copy("input2.txt", file2)

    word_freq, char_dist = await analyze_files([str(file1), str(file2)])

    assert isinstance(word_freq, dict)
    assert len(word_freq) > 0
    assert isinstance(char_dist, dict)
    assert len(char_dist) > 0

