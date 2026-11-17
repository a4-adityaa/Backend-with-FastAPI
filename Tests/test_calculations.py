from apps.Connection_Through_ORM.calculations import add


def test_add():
    print("testing add function")
    assert add(3,6) == 9

