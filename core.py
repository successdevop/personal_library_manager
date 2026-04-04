import datetime
import random
from storage import save_json_data
from config import DATA_FILE, USERS_FILE


def validate_string(prompt: str) -> str:
    """
    this function makes sure that an empty space is not returned
    and the text returned must be greater or equal to three characters
    :param prompt: user string input
    :return: str value
    """
    while True:
        text = input(prompt).strip()
        if text and len(text) >= 3:
            return text
        print("Input cannot be empty")


def validate_numbers(prompt: str) -> int:
    """
    this function makes sure that negative numbers or decimal numbers are not returned
    :param prompt: user string input
    :return: an int value
    """
    while True:
        num = input(prompt)
        if num.isnumeric() and len(num) == 4:
            return int(num)
        print("Invalid year")


def read_book() -> bool:
    """
    this function returns either true or false depending on whether the book has been read
    :return: bool
    """
    answer = (True, False)
    return answer[random.randint(0, 1)]


def book_rating(val: bool):
    """
    this function checks the val boolean input, which can be either true of false, if it is True,
    the function generates random numbers between, 1 to 5, and returns an int value otherwise it
    returns None
    :param val: a boolean value
    :return: int or None value
    """
    if val is True:
        return random.randint(1, 5)

    return None


def generate_id(data: list) -> float:
    """
    this function generates a unique id for every book object created.
    It uses the while loop to check if the number exit, if it does, it
    generates another id and if it doesn't it returns the number generated
    :return: an int value
    """
    bk_id = 1
    while True:
        if not any(bk["id"] == bk_id for bk in data):
            return bk_id
        bk_id += 1


def add_book(data: list):
    """This function adds a new book to the library after checking through our json file/document
        to be sure that such book does not already exist
    """

    title = validate_string("Enter the title: ")
    author = validate_string("Enter the author's name: ")
    year = validate_numbers("Enter the year of publication: ")
    genre = validate_string("Enter the genre: ")
    read = read_book()
    rating = book_rating(read)
    book_id = generate_id(data)

    book = {"id": book_id, "title": title, "author": author, "year": year, "genre": genre, "read": read, "rating": rating,
            "available": True, "borrowed_at": None, "returned_at": None}

    for b in data:
        if book["title"].casefold() == b["title"].casefold() and book["author"].casefold() == b["author"].casefold():
            print("Book already exists")
            return

    data.append(book)
    save_json_data(data=data, filename=DATA_FILE)
    print(f"Book Added!!! Title: {title}")


def remove_book(data: list):
    """this function removes a book from the libreary by the book's title"""
    book_r = input("Enter the title of the book: ")
    book = next((b for b in data if b["title"].casefold() == book_r.casefold()), None)
    if not book:
        print("Book not found")
        return

    data.remove(book)
    save_json_data(data, DATA_FILE)
    print("Book removed")


def display_all_books(data: list):
    """ this function displays all books in our library"""
    for index, book in enumerate(data, 1):
        print(f"{index}. {book['title'].capitalize()} - {book['author'].capitalize()} ({'Available' if book['available'] else 'Borrowed'})")


def borrow_book(data: list, users: list) -> str:
    """
    this function searches for the book that the user wants to borrow, if the book is available
    to be borrowed, the key value changes to False, to indicate it has been borrowed. Time when
    it was borrowed would be updated and the returned value would be updated to None.
    If it is not available it prints a message telling that the book is not available to be borrowed
    :param data: library list of books
    :param users: list of book borrowers
    :return: a string message
    """
    name = validate_string("Please enter your name: ")
    book_title_to_be_borrowed = validate_string("Enter book title: ")

    for book in data:
        if book.get("title").casefold() == book_title_to_be_borrowed.casefold():
            if not book["available"]:
                return "Book already borrowed"

            book["available"] = False
            book["returned_at"] = None
            book["borrowed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            user = next((u for u in users if u["name"].casefold() == name.casefold()), None)

            if not user:
                user = {"name": name, "borrowed_books": []}
                users.append(user)

            user["borrowed_books"].append(book_title_to_be_borrowed)
            save_json_data(users, USERS_FILE)
            save_json_data(data, DATA_FILE)

            return f"{book['title']} borrowed to {name.capitalize()} and to be returned in ten days time"

    return "Book not found"


def return_borrowed_book(data: list, users: list) -> str:
    """
    this function searches our borrower's database(json file), if users are found that means books have been
    borrowed. then we check the name of the borrower and the title of the book borrowed, if found, the availability
    would be set to True, the time returned would be documented and the book would be deleted from the borrower's
    list of borrowed books and a message would be returned. Otherwise, it would return book not found.
    :return: a message string text
    """
    name = validate_string("Please enter your name: ")
    book_title_borrowed = validate_string("Please enter the title of book borrowed: ")

    user = next((u for u in users if u["name"].casefold() == name.casefold()), None)
    if not user:
        return f"Borrower({name.capitalize()}) not found"

    if book_title_borrowed not in user["borrowed_books"]:
        return "Book not found in borrower's library"

    book = next((b for b in data if b["title"].casefold() == book_title_borrowed.casefold()), None)
    if not book:
        return "Book not found"

    book["available"] = True
    book["borrowed_at"] = None
    book["returned_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    user["borrowed_books"].remove(book_title_borrowed)

    if len(user["borrowed_books"]) < 1:
        users.remove(user)

    save_json_data(users, USERS_FILE)
    save_json_data(data, DATA_FILE)

    return f"{name.capitalize()} has returned the book ({book_title_borrowed})"


def view_statistics(data: list):
    """ this function shows the different statistics about books in our library"""
    total_books = len(data)

    available_books = len([book for book in data if book["available"]])

    borrowed_books = total_books - available_books

    books_per_genre = {}
    counter = 0
    most_common_genre = None
    for book in data:
        genre = book['genre'].casefold()
        books_per_genre[genre] = books_per_genre.setdefault(genre, 0) + 1
    for genre, genre_value in books_per_genre.items():
        if counter < genre_value:
            counter = genre_value
            most_common_genre = genre

    unread_books = len([book for book in data if not book["read"]])

    read_books = total_books - unread_books

    rated_books = [books for books in data if books["rating"]]
    total_rating = 0
    for book in rated_books:
        total_rating += book['rating']
    average_rating = total_rating // len(rated_books) if rated_books else 0

    print(f"""
    ======= Library Statistics =======
    Total books: {total_books}
    Available books: {available_books}
    Borrowed books: {borrowed_books}
    Most common genre: {most_common_genre}
    Total unread books: {unread_books}
    Total read books: {read_books}
    Average book rating: {average_rating}
    """)


def get_top_rated_books(data: list):
    """ this function searches our library and returns the top-rated three books"""
    top_rated = sorted(data, key=lambda x: x.get("rating") or 0)[-3:]
    print("======= Top Rated Books =======")
    for index, book in enumerate(top_rated, 1):
        print(f"{index} {book['title'].capitalize()}")


def book_search_operator(book_library_data, choice, category_of_search):
    """
    this function helps to search for a book or a collection of books
    :param book_library_data: a library where books are stored
    :param choice: Unique message based on what search you are making
    :param category_of_search: title, author or genre
    :return:
    """
    found = False
    text = ""

    if choice == "1":
        text = validate_string("Enter book title: ")
    elif choice == "2":
        text = validate_string("Enter book author: ")
    elif choice == "3":
        text = validate_string("Enter book genre: ")
    elif choice == "4":
        text = input("Please enter ratings between 1 to 5: ")

    if not text.isnumeric():
        for books in book_library_data:
            if text.casefold() in books.get(category_of_search).casefold():
                print(f"*. Book_title: {books['title']} - | - Author: {books['author']}")
                found = True
    else:
        new_text = int(text)
        if 1 <= new_text <= 5:
            for books in book_library_data:
                if books.get(category_of_search) >= new_text:
                    print(f"*. Book_title: {books['title']} - | - Author: {books['author']}")
                    found = True
        else:
            print("Enter a rating between 1 to 5 next time. Bye....")
            return

    if not found:
        print(f"Books with this {category_of_search} not found")


def book_search(data: list):
    """this function displays a list of books searched for"""
    while True:
        print("Search book by category: ")
        print("1. Book title")
        print("2. Book author")
        print("3. Book genre")
        print("4. Book rating")

        choice = input("> ")

        if choice == "1":
            book_search_operator(data, choice, "title")
            break
        elif choice == "2":
            book_search_operator(data, choice, "author")
            break
        elif choice == "3":
            book_search_operator(data, choice, "genre")
            break
        elif choice == "4":
            book_search_operator(data, choice, "rating")
            break
        else:
            print("Invalid choice")


def update_reading_status(data: list):
    """
    the user uses this function to update a book that was previously not read
    It could be any book
    :param data: library book data
    :return: None
    """
    unread_books = [book for book in data if not book["read"]]
    if not unread_books:
        print("All books have been read")
        return

    book_to_update = random.choice(unread_books)

    book = next((b for b in data if b["title"].casefold() == book_to_update["title"].casefold()))
    book["read"] = True
    book["rating"] = book_rating(book["read"])
    save_json_data(data, DATA_FILE)
    print(f"I have just finished reading the book ({book_to_update['title']}). Book updated")


def generate_reading_list(data: list, genre=None):
    """this function suggests unread books, optionally filtered by genre"""
    # Return list of unread books as tuples (title, author)

    unread_books = [books for books in data if not books["read"]]
    if not unread_books:
        print("No unread books")
        return

    # if genre:
    #     for index, books in enumerate(unread_books, 1):
    #         if books.get("genre") != genre.casefold():

    if not genre:
        for index, books in enumerate(unread_books, 1):
            print(f"{index}. {(books['title'], books['author'])}")
    else:
        for books in unread_books:
            if books.get("genre").casefold() == genre.casefold():
                print(f"{(books["title"], books["author"])}")
            else:
                print("There are no unread books with such genre")
                return


def books_per_author(data: list):
    """this function uses dictionary to count books per author"""
    # Return dict with author names as keys, count as values
    authors = {}
    for author in data:
        val = author["author"].casefold()
        if val in authors:
            authors[val] += 1
        else:
            authors[val] = 1
        # authors[val] = authors.setdefault(val, 0) + 1
    print(authors)


def book_overdue_system_check(data: list):
    """
    this function searches our json file/document to find books overdue, that is, books that have been
    borrowed for more than ten day. If it finds, it prints those books, if it doesn't, it prints a
    message to that effect
    :param data: Library book data
    :return: None
    """
    borrowed_books = [b for b in data if b.get("borrowed_at")]
    if not borrowed_books:
        print("No borrowed books")
        return

    found = False
    for book in borrowed_books:
        time_borrowed = datetime.datetime.now().strptime(book["borrowed_at"], "%Y-%m-%d %H:%M")

        if (datetime.datetime.now() - time_borrowed) > datetime.timedelta(days=10):
            print(f"Book title: {book['title']}")
            found = True

    if not found:
        print("No overdue books")


def pagination(data: list, page=1, per_page=5):
    """
    this function loads data into our library in bit, that is, five books per time. This feature helps
    to increase performance
    :param data: library data
    :param page: page per screen
    :param per_page: number of data to be loaded
    :return: None
    """
    start = (page - 1) * per_page
    return data[start:start+per_page]


def sort_books(data: list, key: str) -> list:
    """
    this function helps the library management to sort books according to any key of their choice
    :param data: library book data
    :param key: string value
    :return: a new sorted list
    """
    return sorted(data, key=lambda x: x.get(key) or 0)


def display_menu():
    """Show menu options"""
    print("\n=== Personal Library Manager ===")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for books")
    print("4. Display all books")
    print("5. View statistics")
    print("6. Mark book as read")
    print("7. Generate reading list")
    print("8. Books per authors")
    print("9. Get top rated books")
    print("10. Borrow book")
    print("11. Return book")
    print("12. Overdue books")
    print("13. Pagination")
    print("14. Sort books")
    print("0. Exit")
