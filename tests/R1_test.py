import pytest
from library_service import (
    add_book_to_catalog
)


def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()


def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message


# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.

def title_too_long():
    char_20 = "[ this is 20 chars ]"

    test_book = char_20 + char_20 + char_20 + char_20 + char_20\
            + char_20 + char_20 + char_20 + char_20 + char_20\
            + "this is over 200 chars"

    success, message = add_book_to_catalog(test_book, "Test Author", "123456789", 5)

    assert success == False
    assert "200 characters" in message


def test_author_too_long():
    char_20 = "[ this is 20 chars ]"

    test_author = char_20 + char_20 + char_20 + char_20 + char_20\
            + "this is over 100 chars"

    success, message = add_book_to_catalog("Test Book", test_author, "123456789", 5)

    assert success == False
    assert "100 characters" in message


def test_isbn_non_integer():

    success, message = add_book_to_catalog("Test Book", "Test Author", "thirteen char", 5)

    # this test would fail with current implementation because there is no checks if ISBN is an integer
    assert success == False
    assert "digits only" in message # if feature implemented correctly error msg would contain "ISBN must be composed of digits only."


def test_total_copies_non_integer():
    success, message = add_book_to_catalog("Test Book", "Test Author", "thirteen char", "invalid")

    assert success == False
    assert "positive integer" in message


def test_total_copies_is_zero():
    success, message = add_book_to_catalog("Test Book", "Test Author", "thirteen char", 0)

    assert success == False
    assert "positive integer" in message


def test_reject_duplicate_book():
    # this test would require a test database which is cleared before each test, to avoid collisions
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)

    assert success == True
    assert "successfully added" in message.lower()

    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)

    assert success == False
    assert "isbn already exists" in message.lower()



