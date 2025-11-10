import pytest

from services.library_service import (
    add_book_to_catalog,
    borrow_book_by_patron

)
from database import reset_database, get_book_by_isbn

from app import create_app

app_instance = create_app()
client = app_instance.test_client()


# these tests require the database to be cleared before each test, and then populated with standard starting data, to avoid collisions
# they will be written with this assumption in mind, and therefore may contain unintentional collision errors if run more then once


def test_catalog_displays_standard_books():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the database
    reset_database()

    response = client.get("/catalog")
    decoded_response = response.data.decode('utf-8').replace(" ", "").replace("\n", "")

    # proper table structure for catalog
    table_structure = "<thead><tr><th>ID</th><th>Title</th><th>Author</th><th>ISBN</th><th>Availability</th><th" \
                      ">Actions</th></tr></thead>"

    great_gatsby = "<td>TheGreatGatsby</td><td>F.ScottFitzgerald</td><td>9780743273565</td><td><spanclass" \
                   "=\"status-available\">3/3Available</span></td>"

    assert table_structure in decoded_response
    assert great_gatsby in decoded_response

def test_new_book_displayed():
    # this test only works if database is reset before it is run to avoid collisions
    reset_database()

    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)

    # assert book successfully added to database
    assert success == True
    assert "successfully added" in message.lower()

    response = client.get("/catalog")
    decoded_response = response.data.decode('utf-8').replace(" ", "").replace("\n", "")

    test_book = "<td>TestBook</td><td>TestAuthor</td><td>1234567890123</td><td><spanclass" \
                   "=\"status-available\">5/5Available</span></td>"

    assert test_book in decoded_response


def test_availability_updated():
    # this test only works if database is reset before it is run to avoid collisions
    reset_database()

    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)

    # assert book successfully added to database
    assert success == True
    assert "successfully added" in message.lower()

    book = get_book_by_isbn("1234567890123")  # Test Book isbn
    book_id = book['id']

    success, message = borrow_book_by_patron("654321", book_id)

    # assert book successfully added to database
    assert success == True
    assert "successfully borrowed" in message.lower()

    response = client.get("/catalog")
    decoded_response = response.data.decode('utf-8').replace(" ", "").replace("\n", "")

    # availability is now 4 instead of 5
    test_book = "<td>TestBook</td><td>TestAuthor</td><td>1234567890123</td><td><spanclass" \
                   "=\"status-available\">4/5Available</span></td>"

    assert test_book in decoded_response

def test_book_unavailable():
    # this test only works if database is reset before it is run to avoid collisions
    reset_database()

    success, message = add_book_to_catalog("Test Book w 1 available", "Test Author", "1111111111111", 1)

    # assert book successfully added to database
    assert success == True
    assert "successfully added" in message.lower()

    book = get_book_by_isbn("1111111111111")  # Test Book isbn
    book_id = book['id']

    borrow_book_by_patron("654321", book_id)

    response = client.get("/catalog")
    decoded_response = response.data.decode('utf-8').replace(" ", "").replace("\n", "")

    # availability is now "Not Available"
    test_book = "<td>TestBookw1available</td><td>TestAuthor</td><td>1111111111111</td><td><spanclass" \
                   "=\"status-unavailable\">NotAvailable</span>"

    assert test_book in decoded_response
