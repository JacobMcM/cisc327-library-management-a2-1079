import pytest
from library_service import (
    calculate_late_fee_for_book
)

from database import (
    get_patron_borrowed_books,
    insert_borrow_record,
    update_book_availability
)

from datetime import datetime, timedelta


# Given that there is no implementation for the late fee calculation, and the requirements have no conception
# about what happens when a book is borrowed more then once, I will assert that calculation if done by pairing the
# earliest time a book was borrowed for the purposes of calculation

def test_successful_late_fee_calculation():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    patron_id = "7878787"

    due_date = datetime.now() - timedelta(days=3)  # less than 7 days overdue
    borrow_date = due_date - timedelta(days=14)

    # id 1 should be the great gatsby
    success = insert_borrow_record(patron_id, 1, borrow_date, due_date)
    assert success

    due_date = datetime.now() - timedelta(days=10)  # over 7 days, less than maximum
    borrow_date = due_date - timedelta(days=14)

    # id 2 should be To Kill a Mockingbird
    success = insert_borrow_record(patron_id, 2, borrow_date, due_date)
    assert success

    due_date = datetime.now() - timedelta(days=100)  # over maximum cost threshold
    borrow_date = due_date - timedelta(days=14)

    # id 3 should be 1984
    success = insert_borrow_record(patron_id, 3, borrow_date, due_date)
    assert success

    """
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """

    # assert fee calculations are performed correctly
    result = calculate_late_fee_for_book(patron_id, 1)
    assert result['fee_amount'] == 0.5*3
    assert result['days_overdue'] == 3
    assert 'calculation successful' in result['status'].lower()

    value, message = calculate_late_fee_for_book(patron_id, 2)
    assert result['fee_amount'] == 0.5*7 + 1*3
    assert result['days_overdue'] == 10
    assert 'calculation successful' in result['status'].lower()

    value, message = calculate_late_fee_for_book(patron_id, 3)
    assert result['fee_amount'] == 15.0
    assert result['days_overdue'] == 100
    assert 'calculation successful' in result['status'].lower()


def test_successful_late_fee_calculation_boundaries():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    patron_id = "7878787"

    due_date = datetime.now() - timedelta(days=7)  # exactly 7 days overdue
    borrow_date = due_date - timedelta(days=14)

    # id 1 should be the great gatsby
    success = insert_borrow_record(patron_id, 1, borrow_date, due_date)
    assert success

    due_date = datetime.now() - timedelta(days=18)  # exactly the maximum number of days before the fee exceeds 15$
    borrow_date = due_date - timedelta(days=14)

    # id 2 should be To Kill a Mockingbird
    success = insert_borrow_record(patron_id, 2, borrow_date, due_date)
    assert success

    due_date = datetime.now() - timedelta(days=19)  # exactly the minmum number of days after the fee exceeds 15$
    borrow_date = due_date - timedelta(days=14)

    # id 3 should be 1984
    success = insert_borrow_record(patron_id, 3, borrow_date, due_date)
    assert success

    """
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """

    # assert fee calculations are performed correctly
    result = calculate_late_fee_for_book(patron_id, 1)
    assert result['fee_amount'] == 0.5 * 7
    assert result['days_overdue'] == 3
    assert 'calculation successful' in result['status'].lower()

    value, message = calculate_late_fee_for_book(patron_id, 2)
    assert result['fee_amount'] == 0.5 * 7 + 1 * 11
    assert result['days_overdue'] == 10
    assert 'calculation successful' in result['status'].lower()

    value, message = calculate_late_fee_for_book(patron_id, 3)
    assert result['fee_amount'] == 15.0
    assert result['days_overdue'] == 100
    assert 'calculation successful' in result['status'].lower()


def test_fee_is_zero_if_not_overdue():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified

    patron_id = "7878787"

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)  # book issued today

    # id 1 should be the great gatsby
    success = insert_borrow_record(patron_id, 1, borrow_date, due_date)
    assert success

    due_date = datetime.now() + timedelta(days=7)  # halfway through borrow date
    borrow_date = due_date - timedelta(days=14)

    # id 2 should be To Kill a Mockingbird
    success = insert_borrow_record(patron_id, 2, borrow_date, due_date)
    assert success

    due_date = datetime.now()  # book due today, no fee charged
    borrow_date = due_date - timedelta(days=14)

    # id 3 should be 1984
    success = insert_borrow_record(patron_id, 3, borrow_date, due_date)
    assert success

    """
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """

    # assert fee calculations are performed correctly
    result = calculate_late_fee_for_book(patron_id, 1)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == 0
    assert 'not due' in result['status'].lower()

    value, message = calculate_late_fee_for_book(patron_id, 2)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == 0
    assert 'not due' in result['status'].lower()

    value, message = calculate_late_fee_for_book(patron_id, 3)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == 0
    assert 'not due' in result['status'].lower()


def test_calculate_fee_for_patron_who_has_not_borrowed():
    # this test assumes that only the starting sample data (The great gatsby, To Kill a Mockingbird, 1984) is in the
    # database, and it has not been modified. It is also assumed that borrow records are empty

    patron_id = "9898989"

    # assert fee calculations are performed correctly
    result = calculate_late_fee_for_book(patron_id, 1)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == -1  # signal of error
    assert 'not issued' in result['status'].lower()