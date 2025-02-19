import pytest
from magic_methot.Matrix import Matrix


def test_addition():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    expected = Matrix([[6, 8], [10, 12]])
    assert m1 + m2 == expected

def test_multiplication():
    m1 = Matrix([[1, 2, 3], [4, 5, 6]])
    m2 = Matrix([[7, 8], [9, 10], [11, 12]])
    expected = Matrix([[58, 64], [139, 154]])
    assert m1 * m2 == expected

def test_transpose():
    m1 = Matrix([[1, 2, 3], [4, 5, 6]])
    expected = Matrix([[1, 4], [2, 5], [3, 6]])
    assert m1.transpose() == expected

def test_addition_exception():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="Матрицы должны иметь одинаковую размерность"):
        _ = m1 + m2

def test_multiplication_exception():
    m1 = Matrix([[1, 2]])
    m2 = Matrix([[1, 2]])
    with pytest.raises(ValueError, match="Матрицы не могут быть перемножены из-за несовместимых размерностей"):
        _ = m1 * m2

if __name__ == "__main__":
    pytest.main()