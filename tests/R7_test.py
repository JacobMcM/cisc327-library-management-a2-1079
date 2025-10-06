import pytest
import re
from datetime import datetime, timedelta
from library_service import (
    add_book_to_catalog,
    get_patron_status_report,
    calculate_late_fee_for_book,
    return_book_by_patron,
    borrow_book_by_patron
)
from database import reset_database


def test_get_standard_status_report():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. Sample data begins with user 123456 holding the only copy of 1984 with
    # a due back date of October 13, 2025
    reset_database()

    result = get_patron_status_report("123456")
    outstanding_books = result['outstanding_books']
    records = result['records']

    late_fee = 0.0
    for outstanding_book in outstanding_books:
        late_fee += calculate_late_fee_for_book("123456", outstanding_book['book_id'])['fee_amount']

    assert result['num_outstanding'] == 1  # test that it equals 1 and equals number of outstanding_book
    assert result['num_outstanding'] == len(outstanding_books)
    assert result['late_fee'] == late_fee

    assert len(outstanding_books) == 1
    outstanding_books = outstanding_books[0]

    assert len(records) == 1
    records = records[0]

    date_pattern = r"^\d{4}-\d{2}-\d{2}"

    assert outstanding_books['book_id'] == 3
    assert outstanding_books['title'] == "1984"
    assert outstanding_books['author'] == 'George Orwell'
    assert re.fullmatch(date_pattern, outstanding_books['borrow_date']) is not None
    assert re.fullmatch(date_pattern, outstanding_books['due_date']) is not None

    assert records['book_id'] == 3
    assert records['title'] == "1984"
    assert records['author'] == 'George Orwell'
    assert re.fullmatch(date_pattern, records['borrow_date']) is not None
    assert records['return_date'] == "Outstanding"


def test_status_report_for_patron_with_no_history():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. Sample data begins with user 123456 holding the only copy of 1984 with
    # a due back date of October 13, 2025. no other patron has taken out a book.
    reset_database()

    result = get_patron_status_report("654321")  # this user has never borrowed a book
    outstanding_books = result['outstanding_books']
    records = result['records']

    assert result['num_outstanding'] == 0
    assert result['late_fee'] == 0.0
    assert outstanding_books == []
    assert records == []

def test_report_updates_after_borrow():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. Sample data begins with user 123456 holding the only copy of 1984 with
    # a due back date of October 13, 2025. no other patron has taken out a book.

    # assert standard book displayed
    test_get_standard_status_report()

    status, message = borrow_book_by_patron("123456", 1)  # the great gatsby is ID = 1

    assert status == True
    assert "successfully borrowed" in message.lower()

    result = get_patron_status_report("123456")
    outstanding_books = result['outstanding_books']
    records = result['records']

    late_fee = 0.0
    for outstanding_book in outstanding_books:
        late_fee += calculate_late_fee_for_book("123456", outstanding_book['book_id'])['fee_amount']

    assert result['num_outstanding'] == 2  # test that it equals 0 and equals number of outstanding_book
    assert result['num_outstanding'] == len(outstanding_books)
    assert result['late_fee'] == late_fee

    assert len(outstanding_books) == 2
    outstanding_books = outstanding_books[1]  # newest borrow is at the bottom

    assert len(records) == 2
    records = records[1]

    assert outstanding_books['book_id'] == 1
    assert outstanding_books['title'] == "The Great Gatsby"
    assert outstanding_books['author'] == "F. Scott Fitzgerald"
    assert outstanding_books['borrow_date'] == datetime.now().strftime("%Y-%m-%d")
    assert outstanding_books['due_date'] == (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    assert records['book_id'] == 1
    assert records['title'] == "The Great Gatsby"
    assert records['author'] == "F. Scott Fitzgerald"
    assert records['borrow_date'] == datetime.now().strftime("%Y-%m-%d")
    assert records['return_date'] == "Outstanding"

def test_report_updates_after_return():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. Sample data begins with user 123456 holding the only copy of 1984 with
    # a due back date of October 13, 2025. no other patron has taken out a book.

    # assert standard book displayed
    test_get_standard_status_report()

    status, message = return_book_by_patron("123456", 3)

    assert status == True
    assert "successfully returned" in message.lower()

    result = get_patron_status_report("123456")
    outstanding_books = result['outstanding_books']
    records = result['records']

    assert result['num_outstanding'] == 0  # test that it equals 0 and equals number of outstanding_book
    assert result['num_outstanding'] == len(outstanding_books)
    assert result['late_fee'] == 0.0

    assert outstanding_books == []

    assert len(records) == 1
    records = records[0]

    date_pattern = r"^\d{4}-\d{2}-\d{2}"

    assert records['book_id'] == 3
    assert records['title'] == "1984"
    assert records['author'] == 'George Orwell'
    assert re.fullmatch(date_pattern, records['borrow_date']) is not None
    assert records['return_date'] == datetime.now().strftime("%Y-%m-%d")



