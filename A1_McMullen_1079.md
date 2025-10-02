

### 2. Project Implementation Status

Report your findings in a table with columns function name, 
implementation status (complete/partial), what is missing (if any) 
and save in a markdown file named `A1_LastName_last4digitID.md`. Make 
sure you write your name, ID and group number at the top of the file.

## Jacob McMullen, 20341079 (no group)

| Function Name | Implementation Status | Missing Features                                                                                                                                                                                                                               |
|---------------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1            | Partial               | -ISBN accepts any string, not just digits                                                                                                                                                                                                      |
| R2            | Complete              | N/A                                                                                                                                                                                                                                            |
| R3            | Partial               | -Dedicated interface for book borrowing does not exist, has no parameters<br>-borrowing limit is 6 (not 5) books<br>-project (including requirements) have no consideration for how to process a patron borrowing the same book multiple times |
| R4            | Partial               | -Form exists, but is non functional<br>(e.g. does not verify book/patron, update copies/record, or calculate late fees)                                                                                                                        |
| R5            | Partial               | -API endpoint exists, but implementation of late fee calculation does not exist                                                                                                                                                                |
| R6            | Partial               | -Form exists, but is non functional<br>(e.g. does not search for books, does not support partial/exact matching, does not return in same format as catalog)                                                                                    |
| R7            | Not Implemented       | -Functionality not implemented in any capacity                                                                                                                                                                                                 |

### 3. Writing Unit Test
- Write unit test script using python pytest framework for all the functionalities specified in `requirements_specification.md` file
- For each function, write at least 4-5 test cases, including positive and negative test cases
- Create a separate folder named `tests` and store the test script file there. You may create separate script files for each function
- Update the `A1_LastName_last4digitID.md` file to include a summary of the tests scripts
- A sample of test script is given in [`sample_test.py`](sample_test.py) file  

### Summaries:

R1:\
test_add_book_valid_input - given for us\
test_add_book_invalid_isbn_too_short - given for us\
title_too_long - catalog should reject if title over 200 chars\
test_author_too_long - catalog should reject if author over 100 chars
test_isbn_non_integer - catalog should reject if isbn is a non-integer
test_total_copies_non_integer - catalog should reject if total copies is a non-integer
test_total_copies_is_zero - catalog should reject if total copies is zero
test_reject_duplicate_book - catalog should reject if duplicate book submitted

R2:\
test_catalog_displays_standard_books - catalog html should display standard books correctly\
test_new_book_displayed - catalog html should display newly added books correctly\
test_availability_updated - catalog html should update availability when it changes\
test_book_unavailable - catalog html should display "Not Available" if book availability equals 0\

R3:\
test_borrow_book_success - Successful borrow procedure\
test_patron_id_is_not_integer - form should reject if patron id is not an integer\
test_patron_id_is_not_6_digits - form should reject if patron id is exactly 6 digits\
test_prevent_borrowing_book_with_no_availability - form should reject if book has no availability\
test_borrow_limit_of_5_enforced - form should reject if patron has already borrowed 5 books\

R4:\
test_return_book_success - Successful return procedure\
test_wrong_patron_for_borrowed_book - form should reject if incorrect patron for book is entered\
test_wrong_return_from_patron - form should reject if incorrect book for patron is rendered\
test_book_id_is_invalid - form should reject if book id is invalid\

R5:\
test_successful_late_fee_calculation - Standard fees are correctly calculated\
test_successful_late_fee_calculation_boundaries - Fees calculated correctly at the boundaries of the formula\
test_fee_is_zero_if_not_overdue - No fee charged for non-overdue books\
test_calculate_fee_for_patron_who_has_not_borrowed - No fee charged for invalid requests\

R6:\
test_search_matches_catalog_format - Format in catalog is identical to search results\
test_exact_matching_isbn - ISBNs are matched exactly, even if search has matching pre/suffix\
test_partial_mapping_author - Authors are matched partially, as long as search is a substring of any author\
test_partial_mapping_title - titles are matched partially, as long as search is a substring of any title\

R7:\
Due to time constraints I was unable to complete R7 tests. Given the scope of my other tests, I hope I have demonstrated my understanding                                                                                                                                                                                                  |