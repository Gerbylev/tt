from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    type: str
    name: str
    cost: float

    def __repr__(self) -> str:
        return f"Продукт: {self.name}, Тип: {self.type}, Стоимость: {self.cost:.2f}"


class Order:
    def __init__(self):
        self.discount: Optional[float] = None
        self.products: list[Product] = []
        self.type_discount: dict[str, float] = {}

    def add_product(self, product: Product):
        self.products.append(product)

    def set_discount(self, discount: float):
        self.discount = discount

    def set_discount_by_type(self, discount: float, product_type: str):
        self.type_discount[product_type] = discount

    def total_cost(self) -> float:
        total = 0.0
        for product in self.products:
            type_disc = self.type_discount.get(product.type, 0.0)
            price_after_type_discount = product.cost * (1 - type_disc)
            total += price_after_type_discount

        if self.discount is not None:
            total *= (1 - self.discount)

        return total

    def cost_by_type(self, product_type: str) -> float:
        total = 0.0
        for product in self.products:
            if product.type == product_type:
                type_disc = self.type_discount.get(product_type, 0.0)
                price_after_type_discount = product.cost * (1 - type_disc)
                total += price_after_type_discount

        if self.discount is not None:
            total *= (1 - self.discount)

        return total

    def __repr__(self) -> str:
        result = "Заказ:\n"
        if self.products:
            result += "  Товары:\n"
            for product in self.products:
                result += f"    {product}\n"
        else:
            result += "  Нет добавленных товаров.\n"

        result += "  Скидки по типам:\n"
        if self.type_discount:
            for typ, disc in self.type_discount.items():
                result += f"    Тип: {typ}, Скидка: {disc * 100:.1f}%\n"
        else:
            result += "    Нет скидок по типам.\n"

        if self.discount is not None:
            result += f"  Глобальная скидка: {self.discount * 100:.1f}%\n"
        else:
            result += "  Глобальная скидка: отсутствует\n"

        result += f"  Итоговая стоимость заказа: {self.total_cost():.2f}\n"
        return result



if __name__ == "__main__":
    p1 = Product(type="электроника", name="Смартфон", cost=20000)
    p2 = Product(type="электроника", name="Ноутбук", cost=50000)
    p3 = Product(type="одежда", name="Куртка", cost=8000)

    order = Order()
    order.add_product(p1)
    order.add_product(p2)
    order.add_product(p3)

    order.set_discount_by_type(0.1, "электроника")
    order.set_discount(0.05)

    print(order)

    print(f"Стоимость электроники: {order.cost_by_type('электроника'):.2f}")
