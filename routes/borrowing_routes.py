"""
Borrowing Routes - Book borrowing and returning endpoints
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from library_service import borrow_book_by_patron, return_book_by_patron, get_patron_status_report
from database import get_patron_borrowed_books, get_borrow_records_by_patron

borrowing_bp = Blueprint('borrowing', __name__)

@borrowing_bp.route('/borrow', methods=['POST'])
def borrow_book():
    """
    Process book borrowing request.
    Web interface for R2: Book Borrowing
    """
    patron_id = request.form.get('patron_id', '').strip()
    
    try:
        book_id = int(request.form.get('book_id', ''))
    except (ValueError, TypeError):
        flash('Invalid book ID.', 'error')
        return redirect(url_for('catalog.catalog'))
    
    # Use business logic function
    success, message = borrow_book_by_patron(patron_id, book_id)
    
    flash(message, 'success' if success else 'error')
    return redirect(url_for('catalog.catalog'))

@borrowing_bp.route('/return', methods=['GET', 'POST'])
def return_book():
    """
    Process book return.
    Web interface for R3: Book Return Processing
    """
    if request.method == 'GET':
        return render_template('return_book.html')
    
    patron_id = request.form.get('patron_id', '').strip()
    
    try:
        book_id = int(request.form.get('book_id', ''))
    except (ValueError, TypeError):
        flash('Invalid book ID.', 'error')
        return render_template('return_book.html')
    
    # Use business logic function
    success, message = return_book_by_patron(patron_id, book_id)
    
    flash(message, 'success' if success else 'error')
    return render_template('return_book.html')


@borrowing_bp.route('/patron_status', methods=['GET', 'POST'])
def patron_status():
    """
    Process book return.
    Web interface for R3: Book Return Processing
    """

    patron_id = request.args.get('patron_id', '').strip()

    if not patron_id:
        return render_template('patron_status.html', patron_id='', outstanding_books=[], late_fee='', records=[])

    status_report = get_patron_status_report(patron_id)

    return render_template('patron_status.html',
                           patron_id=patron_id,
                           outstanding_books=status_report['outstanding_books'],
                           num_outstanding=status_report['num_outstanding'],
                           late_fee=status_report['late_fee'],
                           records=status_report['records'])
