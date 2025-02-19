import os
import tempfile


def process_integers_file(input_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        content = f.read()
    numbers = [int(x) for x in content.split()]
    if not numbers:
        raise "Error"
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    minimum = min(numbers)
    return (total, average, maximum, minimum)

# Тесты для задания 7
def test_task7():
    test_cases = [
        ("1 2 3 4 5", (15, 3.0, 5, 1)),
        ("10", (10, 10.0, 10, 10)),
        ("-1 -5 -3", (-9, -3.0, -1, -5)),
        ("1 2 3 4", (10, 2.5, 4, 1))
    ]
    for i, (input_text, expected_output) in enumerate(test_cases):
        with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp_in:
            tmp_in.write(input_text)
        result = process_integers_file(tmp_in.name)
        os.unlink(tmp_in.name)
        assert result == expected_output, f"Test case {i+1} failed: expected {expected_output}, got {result}"

if __name__ == '__main__':
    test_task7()
