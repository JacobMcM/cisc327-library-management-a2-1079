import pytest
from library_service import (
    search_books_in_catalog,
    add_book_to_catalog,
    get_all_books
)

# these tests require the database to be cleared before each test, and then populated with standard starting data, to avoid collisions
# they will be written with this assumption in mind, and therefore may contain unintentional collision errors if run more then once

# global patron_id reference
patron_id = "456456"

# Note: all of these tests will always fail because Book return is not implemented


def test_search_matches_catalog_format():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    all_books = get_all_books()

    assert len(all_books) == 3

    result = search_books_in_catalog("", "author")

    # I am asserting that an empty search query will return all books
    assert len(result) == 3

    for book in result:
        # assert that each book in result is of the same format as the books returned for the catalog
        assert book in all_books


def test_exact_matching_isbn():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    result = search_books_in_catalog("9780743273565", "isbn")  # great gatsby isbn

    assert len(result) == 1
    assert result[0]['title'] == "The Great Gatsby"

                                                 # v added extra digit
    result = search_books_in_catalog("97807432735650", "isbn")

    assert len(result) == 0

                                    # v removed one digit
    result = search_books_in_catalog("780743273565", "isbn")

    assert len(result) == 0

def test_partial_mapping_author():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    success, message = add_book_to_catalog("Animal Farm", "George Orwell", "9879879879879", 5)
    # assert Animal Farm added successfully
    assert success == True
    assert "successfully added" in message.lower()

    success, message = add_book_to_catalog("Yellow Book", "George The Monkey", "1112223334445", 5)
    # assert Yellow Book added successfully
    assert success == True
    assert "successfully added" in message.lower()


    result = search_books_in_catalog("G", "author") # this test is important to determine if

    assert len(result) == 4
    titles = result[0]['title'] + result[1]['title'] + result[2]['title'] + result[3]['title']  # since order is ambiguous
    assert "1984" in titles
    assert "Animal Farm" in titles
    assert "Yellow Book" in titles
    assert "The Great Gatsby" in titles # since fitzgerald has a G

    result = search_books_in_catalog("George", "author")

    assert len(result) == 3
    titles = result[0]['title'] + result[1]['title'] + result[2]['title']  # since order is ambiguous
    assert "1984" in titles
    assert "Animal Farm" in titles
    assert "Yellow Book" in titles

    result = search_books_in_catalog("george o", "author")

    assert len(result) == 2
    titles = result[0]['title'] + result[1]['title'] # since order is ambiguous
    assert "1984" in titles
    assert "Animal Farm" in titles


def test_partial_mapping_title():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    success, message = add_book_to_catalog("2019", "some historian", "11223344556", 5)
    # assert Animal Farm added successfully
    assert success == True
    assert "successfully added" in message.lower()

    result = search_books_in_catalog("a", "title")  # this test is important to determine if

    assert len(result) == 2
    titles = result[0]['title'] + result[1]['title'] # since order is ambiguous
    assert "The Great Gatsby" in titles
    assert "To Kill a Mockingbird" in titles

    result = search_books_in_catalog(" a ", "title")

    assert len(result) == 1
    assert result[0]['title'] == "To Kill a Mockingbird"

    result = search_books_in_catalog("19", "title")

    assert len(result) == 2
    titles = result[0]['title'] + result[1]['title']  # since order is ambiguous
    assert "1984" in titles
    assert "2019" in titles
