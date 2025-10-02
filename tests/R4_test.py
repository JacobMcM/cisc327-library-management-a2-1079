import pytest
from library_service import (
    borrow_book_by_patron,
    get_book_by_isbn,
    return_book_by_patron
)
from database import (
    reset_database
)

# these tests require the database to be cleared before each test, and then populated with standard starting data, to avoid collisions
# they will be written with this assumption in mind, and therefore may contain unintentional collision errors if run more then once

# global patron_id reference
patron_id = "456456"

# Note: all of these tests will always fail because Book return is not implemented

def setup():
    # all tests assume that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified
    reset_database()

    # this function produces a setup where patron 456456 has borrowed a copy of the great gatsby
    # it also mirrors a test in R3_test

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
    book_availability = book['available_copies']

    # assert book is in database
    assert book
    assert book_availability > 0

    success, message = borrow_book_by_patron(patron_id, book_id)

    # assert book is successfully borrowed
    assert success == True
    assert "successfully borrowed" in message.lower()



def test_return_book_success():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    # additionally, there are no database functions which exist to manipulate the state of the database for testing,
    # so this all must be done manually using the setup function

    # run setup to enable environment where patron 456456 has borrowed a copy of the great gatsby
    setup()

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
    book_availability = book['available_copies']

    success, message = return_book_by_patron(patron_id, book_id)

    # assert book is successfully returned
    assert success == True
    assert "successfully returned" in message.lower()

    book = get_book_by_isbn("9780743273565")
    book_availability_after = book['available_copies']

    # assert borrow successfully reduced availability by one
    assert book_availability + 1 == book_availability_after

def test_wrong_patron_for_borrowed_book():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    # run setup to enable environment where patron 456456 has borrowed a copy of the great gatsby
    setup()

    book = get_book_by_isbn("9780743273565")  # great gatsby isbn

    book_id = book['id']
                                             # v This patron has not borrowed Great Gatsby
    success, message = return_book_by_patron("999999", book_id)

    # assert book is unsuccessfully returned
    assert success == False
    assert "not currently borrowing" in message.lower()

def test_wrong_return_from_patron():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    # run setup to enable environment where patron 456456 has borrowed a copy of the great gatsby
    setup()

    book = get_book_by_isbn("9780451524935")  # 1984 isbn

    book_id = book['id']
                                             # this patron has borrowed gg not 1984
    success, message = return_book_by_patron(patron_id, book_id)

    # assert book is unsuccessfully returned
    assert success == False
    assert "not currently borrowing" in message.lower()

def test_book_id_is_invalid():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. thus we assume that no book has id = 5

    # Note: this test could be replicated in R3 tests, additionally test_patron_id_is_not_6_digits &
    # test_patron_id_is_not_integer could be implemented here with little issue.

    # run setup to enable environment where patron 456456 has borrowed a copy of the great gatsby
    setup()

    success, message = return_book_by_patron(patron_id, 5)

    # assert book is successfully returned
    assert success == False
    assert "does not exist" in message.lower()

    success, message = return_book_by_patron(patron_id, "invalid")

    # assert book is successfully returned
    assert success == False
    assert "does not exist" in message.lower()
