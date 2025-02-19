import os
from dataclasses import dataclass
import json
from abc import ABC, abstractmethod
import tempfile
import pytest


class SaveLoadInterface(ABC):
    @abstractmethod
    def save(self, bookshelf, filename):
        pass

    @abstractmethod
    def load(self, filename):
        pass

class JsonSaverLoader(SaveLoadInterface):
    def save(self, bookshelf, filename):
        data = {
            "max_weight": bookshelf.max_weight,
            "books": [
                {"author": book.author, "weight": book.weight, "cost": book.cost}
                for book in bookshelf.books
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bs = Bookshelf(data["max_weight"])
        bs.books = [Book(b["author"], b["weight"], b["cost"]) for b in data["books"]]
        return bs

class TxtSaverLoader(SaveLoadInterface):
    def save(self, bookshelf, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{bookshelf.max_weight}\n")
            for book in bookshelf.books:
                f.write(f"{book.author} {book.weight} {book.cost}\n")

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        max_weight = float(lines[0].strip())
        bs = Bookshelf(max_weight)
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            author = parts[0]
            weight = float(parts[1])
            cost = float(parts[2])
            bs.books.append(Book(author, weight, cost))
        return bs

@dataclass
class Book:
    author: str
    weight: float
    cost: float

    def __repr__(self):
        return f"Book(author='{self.author}', weight={self.weight}, cost={self.cost})"

class Bookshelf:
    def __init__(self, max_weight):
        self.max_weight = max_weight
        self.books = []

    def current_total_weight(self):
        return sum(book.weight for book in self.books)

    def current_total_cost(self):
        return sum(book.cost for book in self.books)

    def add_book(self, book):
        if self.current_total_weight() + book.weight <= self.max_weight:
            self.books.append(book)
            return True
        else:
            raise Exception(f"Нельзя добавить книгу: превышение допустимого веса.")

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            return True
        raise Exception("Нельзя удалить книгу")

    def find_books_by_author(self, author):
        return [book for book in self.books if book.author == author]

    def __repr__(self):
        books_str = "\n".join(str(book) for book in self.books)
        return (f"Bookshelf(max_weight={self.max_weight}, current_weight={self.current_total_weight()}, "
                f"total_cost={self.current_total_cost()})\nBooks:\n{books_str}")

    def save_state(self, filename, saver: SaveLoadInterface):
        saver.save(self, filename)

    @classmethod
    def load_state(cls, filename, loader: SaveLoadInterface):
        return loader.load(filename)

def test_task12():
    shelf = Bookshelf(10)
    book1 = Book("Author1", 3, 100)
    book2 = Book("Author2", 4, 150)
    book3 = Book("Author3", 5, 200)
    assert shelf.add_book(book1) == True, "Книга 1 должна добавиться"
    assert shelf.add_book(book2) == True, "Книга 2 должна добавиться"
    with pytest.raises(Exception, match="Нельзя добавить книгу: превышение допустимого веса."):
        shelf.add_book(book3)
    assert shelf.current_total_weight() == 7, "Общий вес должен быть 7"
    assert shelf.current_total_cost() == 250, "Общая стоимость должна быть 250"

    assert shelf.remove_book(book1) == True, "Книга 1 должна удалиться"
    assert shelf.current_total_weight() == 4, "После удаления вес должен быть 4"
    with pytest.raises(Exception, match="Нельзя удалить книгу"):
        shelf.remove_book(book3)

    book4 = Book("Author2", 2, 80)
    shelf.add_book(book4)
    found = shelf.find_books_by_author("Author2")
    assert len(found) == 2, "Должно быть найдено 2 книги от Author2"


    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp_json:
        json_filename = tmp_json.name
    json_saver = JsonSaverLoader()
    shelf.save_state(json_filename, json_saver)
    loaded_shelf_json = Bookshelf.load_state(json_filename, json_saver)
    os.unlink(json_filename)
    assert loaded_shelf_json.max_weight == shelf.max_weight, "Максимальный вес не совпадает (JSON)"
    assert len(loaded_shelf_json.books) == len(shelf.books), "Количество книг не совпадает (JSON)"
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as tmp_txt:
        txt_filename = tmp_txt.name
    txt_saver = TxtSaverLoader()
    shelf.save_state(txt_filename, txt_saver)
    loaded_shelf_txt = Bookshelf.load_state(txt_filename, txt_saver)
    os.unlink(txt_filename)
    assert loaded_shelf_txt.max_weight == shelf.max_weight, "Максимальный вес не совпадает (TXT)"
    assert len(loaded_shelf_txt.books) == len(shelf.books), "Количество книг не совпадает (TXT)"
    print("Все тесты задания 12 пройдены.")

if __name__ == '__main__':
    test_task12()
