import tempfile
import os

def reverse_words_in_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as f_in, \
         open(output_filename, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            words = line.strip().split()
            reversed_line = ' '.join(reversed(words))
            f_out.write(reversed_line + "\n")

def test_task5():
    test_cases = [
        ("Hello world", "world Hello"),
        ("Python is fun", "fun is Python"),
        ("", ""),
        ("   Leading and trailing spaces   ", "spaces trailing and Leading"),
    ]
    for i, (input_text, expected_output) in enumerate(test_cases):
        with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp_in, \
             tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp_out:
            tmp_in.write(input_text + "\n")
            tmp_in.close()
            reverse_words_in_file(tmp_in.name, tmp_out.name)
        with open(tmp_out.name, 'r', encoding='utf-8') as f:
            result = f.read().strip()
        os.unlink(tmp_in.name)
        os.unlink(tmp_out.name)
        assert result == expected_output, f"Test case {i+1} failed: expected '{expected_output}', got '{result}'"

if __name__ == '__main__':
    test_task5()
