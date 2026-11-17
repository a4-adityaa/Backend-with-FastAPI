import pytest
from apps.Connection_Through_ORM.calculations import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 6, 9),
    (5, 4, 9),
    (4, 5, 9),
    (20, 5, 25)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(5,4) ==1

def test_multiply():
    assert multiply(4,5) == 20

def test_divide():
    assert divide(20,5) ==4
