from typing import List

class Matrix:
    data: List[List[float]]
    rows: int
    cols: int

    def __init__(self, data: List[List[float]]) -> None:
        if not data or not isinstance(data, list):
            raise ValueError("Матрица не может быть пустой")
        row_length = len(data[0])
        for row in data:
            if len(row) != row_length:
                raise ValueError("Все строки должны быть одной длины")
        self.data = data
        self.rows = len(data)
        self.cols = row_length

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны иметь одинаковую размерность")
        result_data = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result_data)

    def __mul__(self, other: "Matrix") -> "Matrix":
        if self.cols != other.rows:
            raise ValueError("Матрицы не могут быть перемножены из-за несовместимых размерностей")
        result_data = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                sum_value = 0.0
                for k in range(self.cols):
                    sum_value += self.data[i][k] * other.data[k][j]
                row.append(sum_value)
            result_data.append(row)
        return Matrix(result_data)

    def transpose(self) -> "Matrix":
        result_data = [
            [self.data[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ]
        return Matrix(result_data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return False
        return self.data == other.data

    def __repr__(self) -> str:
        return f"Matrix({self.data})"


