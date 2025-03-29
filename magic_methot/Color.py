from typing import Union


class Color:
    red: int
    green: int
    blue: int

    def __init__(self, red: int, green: int, blue: int) -> None:
        for value, name in zip((red, green, blue), ('red', 'green', 'blue')):
            if not isinstance(value, int):
                raise TypeError(f"{name} должен быть числом")
            if not (0 <= value <= 255):
                raise ValueError(f"{name} должен быть в диапазоне от 0 до 255")
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other: "Color") -> "Color":
        if not isinstance(other, Color):
            return NotImplemented
        red = min(self.red + other.red, 255)
        green = min(self.green + other.green, 255)
        blue = min(self.blue + other.blue, 255)
        return Color(red, green, blue)

    def __mul__(self, factor: Union[float, int]) -> "Color":
        if not isinstance(factor, (float, int)):
            raise TypeError("factor должен быть числом")
        if not (0 <= factor <= 1):
            raise ValueError("factor должен быть от 0 до 1")
        red = round(self.red * factor)
        green = round(self.green * factor)
        blue = round(self.blue * factor)
        return Color(red, green, blue)

    def __rmul__(self, factor: Union[float, int]) -> "Color":
        return self.__mul__(factor)

    def __lt__(self, other):
        if not isinstance(other, Color):
            return False
        if self.red == other.red:
            if self.green == other.green:
                return self.blue < other.blue
            return self.green < other.green
        return self.red < other.red


    def __gt__(self, other):
        if not isinstance(other, Color):
            return False
        if self.red == other.red:
            if self.green == other.green:
                return self.blue > other.blue
            return self.green > other.green
        return self.red > other.red



    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return False
        return (self.red, self.green, self.blue) == (other.red, other.green, other.blue)

    def __repr__(self) -> str:
        return f"Color({self.red}, {self.green}, {self.blue})"

if __name__ == "__main__":
    c1 = Color(201, 200, 100)
    c2 = Color(201, 201, 100)
    print(c1 > c2)

