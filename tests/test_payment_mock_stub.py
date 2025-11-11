import pytest
from services.library_service import *
from database import reset_database
from unittest.mock import Mock
from services.payment_service import PaymentGateway


# ------ pay_late_fees tests ---------

# Test successful payment
def test_valid_payment(mocker):
    """"""

    # stubs
    mocker.patch("services.library_service.calculate_late_fee_for_book",
                 return_value={'fee_amount': 1.5, 'days_overdue': 3, 'status': 'Overdue fee calculation successful'})
    mocker.patch("database.get_book_by_id",
                 return_value={'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald',
                               'isbn': '9780743273565', 'total_copies': 3, 'available_copies': 3})

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)
    mock_payment_gateway.process_payment.return_value = (
        True, "txn_123456_5", f"Payment of ${1.5:.2f} processed successfully")

    success, message, tr_id = pay_late_fees("123456", 1, mock_payment_gateway)

    assert success == True
    assert "processed successfully" in message.lower()
    assert "txn_123456" in tr_id

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with(patron_id="123456", amount=1.5,
                                                            description="Late fees for 'The Great Gatsby'")

# payment declined by gateway
def test_payment_declined(mocker):
    """"""

    # stubs
    mocker.patch("services.library_service.calculate_late_fee_for_book",
                 return_value={'fee_amount': 1.5, 'days_overdue': 3, 'status': 'Overdue fee calculation successful'})
    mocker.patch("database.get_book_by_id",
                 return_value={'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald',
                               'isbn': '9780743273565', 'total_copies': 3, 'available_copies': 3})

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway, return_value=PaymentGateway)
    mock_payment_gateway.process_payment.return_value = (False, "", "Payment declined")

    success, message, tr_id = pay_late_fees("123456", 1, mock_payment_gateway)

    assert not success
    assert "Payment failed" in message
    assert "Payment declined" in message
    assert tr_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with(patron_id="123456", amount=1.5,
                                                            description="Late fees for 'The Great Gatsby'")


# invalid patron ID (verify mock NOT called)
def test_invalid_patron_ID():
    """"""

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message, tr_id = pay_late_fees(None, 1, mock_payment_gateway)

    assert not success
    assert "Invalid patron ID. Must be exactly 6 digits." in message
    assert tr_id is None
    mock_payment_gateway.process_payment.assert_not_called()

    success, message, tr_id = pay_late_fees("bad_id", 1, mock_payment_gateway)

    assert not success
    assert "Invalid patron ID. Must be exactly 6 digits." in message
    assert tr_id is None
    mock_payment_gateway.process_payment.assert_not_called()

    success, message, tr_id = pay_late_fees("12345", 1, mock_payment_gateway)

    assert not success
    assert "Invalid patron ID. Must be exactly 6 digits." in message
    assert tr_id is None
    mock_payment_gateway.process_payment.assert_not_called()

    success, message, tr_id = pay_late_fees("1234567", 1, mock_payment_gateway)

    assert not success
    assert "Invalid patron ID. Must be exactly 6 digits." in message
    assert tr_id is None
    mock_payment_gateway.process_payment.assert_not_called()


# zero late fees (verify mock NOT called)
def test_zero_late_fees(mocker):
    """"""

    # stubs
    mocker.patch("services.library_service.calculate_late_fee_for_book",
                 return_value={'fee_amount': 0.0, 'days_overdue': 0, 'status': 'This borrowed book is not due yet'})

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message, tr_id = pay_late_fees("123456", 1, mock_payment_gateway)

    assert not success
    assert "No late fees to pay for this book." in message
    assert tr_id is None
    mock_payment_gateway.process_payment.assert_not_called()


# network error exception handling
def test_error_exception(mocker):
    """"""

    # stubs
    mocker.patch("services.library_service.calculate_late_fee_for_book",
                 return_value={'fee_amount': 1.5, 'days_overdue': 3, 'status': 'Overdue fee calculation successful'})
    mocker.patch("database.get_book_by_id",
                 return_value={'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald',
                               'isbn': '9780743273565', 'total_copies': 3, 'available_copies': 3})

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)
    mock_payment_gateway.process_payment.side_effect = ValueError("Network error encountered")

    success, message, tr_id = pay_late_fees("123456", 1, mock_payment_gateway)

    assert success == False
    assert "Payment processing error" in message
    assert "Network error encountered" in message
    assert tr_id is None

    mock_payment_gateway.process_payment.assert_called_once()
    mock_payment_gateway.process_payment.assert_called_with(patron_id="123456", amount=1.5,
                                                            description="Late fees for 'The Great Gatsby'")


# ------ refund_late_fee_payment tests ---------

# Test successful refund,
def test_successful_refund():
    """"""

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)
    mock_payment_gateway.refund_payment.return_value = (
        True, f"Refund of ${1.5:.2f} processed successfully. Refund ID: refund_txn_123456_5_5")

    success, message = refund_late_fee_payment("txn_123456_5", 1.5, mock_payment_gateway)

    assert success == True
    assert "processed successfully" in message.lower()

    mock_payment_gateway.refund_payment.assert_called_once()
    mock_payment_gateway.refund_payment.assert_called_with("txn_123456_5", 1.5)


# invalid transaction ID rejection
def test_invalid_transaction_id():
    """"""

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment(None, 1.5, mock_payment_gateway)

    assert success == False
    assert "Invalid transaction ID." in message
    mock_payment_gateway.refund_payment.assert_not_called()

    success, message = refund_late_fee_payment("xn_123456_5", 1.5, mock_payment_gateway)

    assert success == False
    assert "Invalid transaction ID." in message
    mock_payment_gateway.refund_payment.assert_not_called()

    success, message = refund_late_fee_payment("rtxn_123456_5", 1.5, mock_payment_gateway)

    assert success == False
    assert "Invalid transaction ID." in message
    mock_payment_gateway.refund_payment.assert_not_called()


# and invalid refund amounts (negative, zero, exceeds $15 maximum).
def test_invalid_refund_amt():
    """"""

    # mock
    mock_payment_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("txn_123456_5", -1.5, mock_payment_gateway)

    assert success == False
    assert "Refund amount must be greater than 0." in message
    mock_payment_gateway.refund_payment.assert_not_called()

    success, message = refund_late_fee_payment("txn_123456_5", 0.0, mock_payment_gateway)

    assert success == False
    assert "Refund amount must be greater than 0." in message
    mock_payment_gateway.refund_payment.assert_not_called()

    success, message = refund_late_fee_payment("txn_123456_5", 15.5, mock_payment_gateway)

    assert success == False
    assert "Refund amount exceeds maximum late fee." in message
    mock_payment_gateway.refund_payment.assert_not_called()
