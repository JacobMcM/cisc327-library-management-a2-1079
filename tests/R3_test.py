import pytest
from library_service import (
    borrow_book_by_patron,
    get_book_by_isbn,
)
from database import (
    get_patron_borrowed_books,
    insert_borrow_record,
    update_book_availability
)

from datetime import datetime, timedelta


# these tests require the database to be cleared before each test, and then populated with standard starting data, to avoid collisions
# they will be written with this assumption in mind, and therefore may contain unintentional collision errors if run more then once

def test_borrow_book_success():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
    book_availability = book['available_copies']

    # assert book is in database
    assert book
    assert book_availability > 0

    success, message = borrow_book_by_patron("123456", book_id)

    # assert book is successfully borrowed
    assert success == True
    assert "successfully borrowed" in message.lower()

    book = get_book_by_isbn("1234567890123")
    book_availability_after = book['available_copies']

    # assert borrow successfully reduced availability by one
    assert book_availability - 1 == book_availability_after

    book_record = None
    for borrowed_book in get_patron_borrowed_books("123456"):
        if borrowed_book['book_id'] == book_id:
            book_record = borrowed_book
            break

    # assert that book record was created after borrow
    assert book_record


def test_patron_id_is_not_integer():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. It also assumes the borrow_records database is empty

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
    book_availability = book['available_copies']

    # assert book is in database
    assert book
    assert book_availability > 0

    # borrow with an invalid id
    success, message = borrow_book_by_patron("bad id", book_id)

    assert success == False
    assert "invalid patron id" in message.lower()


def test_patron_id_is_not_6_digits():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. It also assumes the borrow_records database is empty

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
    book_availability = book['available_copies']

    # asset book is in database
    assert book
    assert book_availability > 0

    # borrow with an invalid id
    success, message = borrow_book_by_patron("1234567", book_id)

    # assert book is successfully borrowed
    assert success == False
    assert "Invalid patron ID" in message.lower()

    # borrow with an invalid id
    success, message = borrow_book_by_patron("12345", book_id)

    # assert book is successfully borrowed
    assert success == False
    assert "Invalid patron ID" in message.lower()


def test_prevent_borrowing_book_with_no_availability():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. It also assumes the borrow_records database is empty

    book = get_book_by_isbn("9780451524935")  # 1984 isbn

    book_id = book['id']
    book_availability = book['available_copies']

    # assert book is in database
    assert book
    assert book_availability == 1 # in starting sample data, 1984 should always start with 1 availability

    # this test adds ambiguous into the database for the sake of the test (no patron has borrowed 1984),
    # and thus the database should be cleared after test
    update_book_availability(book_id, -1)

    book = get_book_by_isbn("9780451524935")

    book_availability = book['available_copies']

    # assert availability has been successfully modified
    assert book_availability == 0

    success, message = borrow_book_by_patron("123123", book_id)

    # assert patron unsuccessfully borrows their 1984, since its availability is 0
    assert success == False
    assert "maximum borrowing limit" in message.lower()


def test_borrow_limit_of_5_enforced():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. It also assumes the borrow_records database is empty

    patron_id = "654321"

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)

    # add for borrow records
    for i in range(4):
        # this test adds ambiguous into the database for the sake of the test (id = 5 is not in the book database),
        # and thus the database should be cleared after test
        success = insert_borrow_record(patron_id, 5, borrow_date, due_date)
        assert success == True

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
    book_availability = book['available_copies']

    # assert book is in database
    assert book
    assert book_availability > 1  # we will attempt to borrow twice

    success, message = borrow_book_by_patron(patron_id, book_id)

    # assert patron successfully borrows their 5th book
    assert success == True
    assert "successfully borrowed" in message.lower()

    success, message = borrow_book_by_patron(patron_id, book_id)

    # assert patron unsuccessfully borrows their 6th book, since the limit is reached
    assert success == False
    assert "maximum borrowing limit" in message.lower()

    # Note: this test will always fail because borrow limit check is improperly implemented






# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.