import pytest
from _pytest.python_api import raises

from magic_methot.Color import Color


def test_addition_normal():
    c1 = Color(10, 20, 30)
    c2 = Color(20, 30, 40)
    result = c1 + c2
    expected = Color(30, 50, 70)
    assert result == expected


def test_addition_clamping():
    c1 = Color(200, 200, 200)
    c2 = Color(100, 100, 100)
    result = c1 + c2
    expected = Color(255, 255, 255)
    assert result == expected


def test_multiplication():
    c = Color(100, 150, 200)
    factor = 0.5
    result = c * factor
    expected = Color(round(100 * factor), round(150 * factor), round(200 * factor))
    assert result == expected


def test_multiplication_invalid_factor():
    c = Color(100, 150, 200)
    with raises(ValueError, match="factor должен быть от 0 до 1"):
        _ = c * 1.5


def test_constructor_invalid_value():
    with raises(ValueError, match="red должен быть в диапазоне от 0 до 255"):
        _ = Color(300, 0, 0)


def test_constructor_invalid_type():
    with raises(TypeError, match="red должен быть числом"):
        _ = Color("red", 0, 0)

if __name__ == "__main__":
    pytest.main()