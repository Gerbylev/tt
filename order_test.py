from math import isclose

import pytest

from Order import Order, Product


def test_add_product_total_cost():
    order = Order()
    p1 = Product(type="electronics", name="Smartphone", cost=20000)
    p2 = Product(type="clothes", name="Jacket", cost=8000)
    order.add_product(p1)
    order.add_product(p2)
    expected = 20000 + 8000
    assert isclose(order.total_cost(), expected, rel_tol=1e-6)

def test_set_discount_by_type():
    order = Order()
    p1 = Product(type="electronics", name="Smartphone", cost=20000)
    p2 = Product(type="clothes", name="Jacket", cost=8000)
    order.add_product(p1)
    order.add_product(p2)
    order.set_discount_by_type(0.1, "electronics")
    expected = 18000 + 8000
    assert isclose(order.total_cost(), expected, rel_tol=1e-6)

def test_set_global_discount():
    order = Order()
    p1 = Product(type="electronics", name="Smartphone", cost=20000)
    p2 = Product(type="clothes", name="Jacket", cost=8000)
    order.add_product(p1)
    order.add_product(p2)
    order.set_discount(0.05)
    expected = 28000 * 0.95
    assert isclose(order.total_cost(), expected, rel_tol=1e-6)

def test_both_discounts():
    order = Order()
    p1 = Product(type="electronics", name="Smartphone", cost=20000)
    p2 = Product(type="clothes", name="Jacket", cost=8000)
    order.add_product(p1)
    order.add_product(p2)
    order.set_discount_by_type(0.1, "electronics")
    order.set_discount(0.05)
    expected = (20000 * 0.9 + 8000) * 0.95
    assert isclose(order.total_cost(), expected, rel_tol=1e-6)

def test_cost_by_type():
    order = Order()
    p1 = Product(type="electronics", name="Smartphone", cost=20000)
    p2 = Product(type="electronics", name="Laptop", cost=50000)
    p3 = Product(type="clothes", name="Jacket", cost=8000)
    order.add_product(p1)
    order.add_product(p2)
    order.add_product(p3)
    order.set_discount_by_type(0.1, "electronics")
    order.set_discount(0.05)
    expected_electronics = 63000 * 0.95
    expected_clothes = 8000 * 0.95
    assert isclose(order.cost_by_type("electronics"), expected_electronics, rel_tol=1e-6)
    assert isclose(order.cost_by_type("clothes"), expected_clothes, rel_tol=1e-6)

def test_order_str_output(capsys):
    order = Order()
    p1 = Product(type="electronics", name="Smartphone", cost=20000)
    order.add_product(p1)
    order.set_discount_by_type(0.1, "electronics")
    order.set_discount(0.05)
    print(order)
    captured = capsys.readouterr().out
    assert "Заказ:" in captured
    assert "Smartphone" in captured
    assert "electronics" in captured
    assert "10.0%" in captured
    assert "5.0%" in captured
    assert "Итоговая стоимость заказа" in captured

if __name__ == "__main__":
    pytest.main()