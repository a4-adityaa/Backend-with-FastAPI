import pytest
from apps.Connection_Through_ORM.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# setting up fixture that runs before the acutal test runs
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



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


def test_bank_account_initial_amt(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amt(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_deposit_amount(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,3) == 55



@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100, 100),
    (50, 40, 10),
    (100, 80, 20),
    (25, 5, 20)
])
def test_bank_transction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_fund(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401