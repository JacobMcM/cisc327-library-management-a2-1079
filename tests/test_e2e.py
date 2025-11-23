from playwright.sync_api import Playwright, sync_playwright, Page, expect
from database import reset_database


def test_add_and_borrow_book(playwright: Playwright):
    reset_database()

    base_url = "http://localhost:5000"
    catalog_url = base_url + "/catalog"
    add_book_url = base_url + "/add_book"

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # goto base URL
    page.goto(base_url)

    # verify we are at /catalog
    expect(page).to_have_url(catalog_url)

    # click add book
    page.get_by_role("link", name="Add New Book").click()

    # verify we are at /add_book
    expect(page).to_have_url(add_book_url)

    # fill out details
    page.get_by_role("textbox", name="Title *").fill("E2E_Test_Book_")
    page.get_by_role("textbox", name="Author *").fill("E2E_Test_Book_Author")
    page.get_by_role("textbox", name="ISBN *").fill("1234567890123")
    page.get_by_role("spinbutton", name="Total Copies *").fill("1")

    # click add book to catelog
    page.get_by_role("button", name="Add Book to Catalog").click()

    # verify we are at /catalog
    expect(page).to_have_url(catalog_url)

    # verify 'Book "test" has been successfully added to the catalog' visible
    expect(page.get_by_text("Book \"E2E_Test_Book_\" has been")).to_be_visible()

    # verify new book has been added
    new_book = page.get_by_role("row", name="4 E2E_Test_Book_ E2E_Test_Book_Author 1234567890123 1/1")
    expect(new_book).to_be_visible()

    # Borrow new book
    new_book.get_by_placeholder("Patron ID (6 digits)").click()
    new_book.get_by_placeholder("Patron ID (6 digits)").fill("111111")
    new_book.get_by_role("button").click()

    # verify borrow message appears
    expect(page.get_by_text("Successfully borrowed \"E2E_Test_Book_")).to_be_visible()

    context.close()
    browser.close()
