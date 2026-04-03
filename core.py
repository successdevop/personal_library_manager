import datetime
import random
import json
from operator import itemgetter
from storage import load_json_data, save_json_data
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
    for book in data:
        if book.get("title").casefold() == book_r.casefold():
            data.remove(book)
            print("Book removed")
            return
    print("Book not found")


def display_all_books(data: list):
    """ this function displays all books in our library"""
    for index, book in enumerate(data, 1):
        print(f"{index}. {book['title'].capitalize()} - {book['author'].capitalize()} ({'Available' if book['available'] else 'Borrowed'})")


def borrow_book(data: list) -> str:
    """
    this function searches for the book that the user wants to borrow, if the book is available
    to be borrowed, the key value changes to False, to indicate it has been borrowed.
    If it is not available it prints a message telling that the book is not available to be borrowed
    :param data: library list of books
    :return: a string message
    """
    if not data:
        return "No book in the library"

    name = validate_string("Please enter your name: ")
    book_title_to_be_borrowed = validate_string("Enter book title: ")

    for books in data:
        if books.get("title").casefold() == book_title_to_be_borrowed.casefold() and books["available"]:
            books["available"] = False
            books["returned_at"] = None
            books["borrowed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            users = load_json_data('users.json')
            if not users:
                user = {"name": name, "borrowed_books": []}
                user["borrowed_books"].append(book_title_to_be_borrowed)
                users.append(user)

                with open('users.json', mode='w', encoding='utf-8') as write_file:
                    json.dump(users, write_file, indent=4)

                update_json_data(data, filename='data.json')
            else:
                for user in users:
                    if user["name"] == name:
                        user["borrowed_books"].append(book_title_to_be_borrowed)
                        break
                update_json_data(users, 'users.json')
                update_json_data(data, 'data.json')
            return f"{books['title']} borrowed to {name.capitalize()} and to be returned in ten days time"

        elif books.get("title").casefold() == book_title_to_be_borrowed.casefold():
            return "Book has been borrowed"
    return "Book not found"


def return_borrowed_book():
    """
    this function searches our borrower's database(json file), if users are found that means books have been
    borrowed. then we check the name of the borrower and the title of the book borrowed, if found, the availability
    would be set to True, the time returned would be documented and the book would be deleted from the borrower's
    list of borrowed books and a message would be returned. Otherwise, it would return book not found.
    :return: a message string text
    """
    found = False
    users = load_json_data('users.json')
    if not users:
        return "No books borrowed"

    name = validate_string("Please enter your name: ")
    book_title_borrowed = validate_string("Please enter the title of book borrowed: ")

    for user in users:
        if user['name'] == name and book_title_borrowed.casefold() in user["borrowed_books"]:
            library_ = load_json_data('data.json')
            for books in library_:
                if books["title"].casefold() == book_title_borrowed.casefold():
                    books["available"] = True
                    books["borrowed_at"] = None
                    books["returned_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    break

            user["borrowed_books"].remove(book_title_borrowed)

            if len(user['borrowed_books']) < 1:
                users.remove(user)

            update_json_data(users, filename='users.json')
            update_json_data(library_, filename='data.json')

            found = True

    if not found:
        return "Book not found"
    else:
        return {f"{name.capitalize()} has returned the book ({book_title_borrowed})"}


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
    average_rating = total_rating // len(rated_books)

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
    top_rated = sorted(data, key=itemgetter('rating'))[-3:]
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

    if text.isnumeric():
        new_text = int(text)
        if 1 <= new_text <= 5:
            for books in book_library_data:
                if books.get(category_of_search) >= new_text:
                    print(f"** Book_title: {books['title']} - | - Author: {books['author']}")
                    found = True
        else:
            print("Enter a rating between 1 to 5 next time. Bye....")
            return
    else:
        for books in book_library_data:
            if text.casefold() in books.get(category_of_search).casefold():
                print(f"** Book_title: {books['title']} - | - Author: {books['author']}")
                found = True

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
    :return: None/performs an action
    """
    unread_books = [book for book in data if not book["read"]]
    if not unread_books:
        print("All books have been read")
        return

    book_to_update = random.choice(unread_books)

    for book in data:
        if book.get("title") == book_to_update["title"]:
            book["read"] = True
            book["rating"] = book_rating(book["read"])
            update_json_data(data)
            print(f"I have just finished reading the book ({book_to_update['title']}). Book updated")
            break


def generate_reading_list(data: list, genre=None):
    """this function suggests unread books, optionally filtered by genre"""
    # Return list of unread books as tuples (title, author)

    unread_books = [books for books in data if not books["read"]]
    if not unread_books:
        print("No unread books")
        return

    found = False

    if genre is not None:
        for books in unread_books:
            if books.get("genre").casefold() == genre.casefold():
                print(f"{(books["title"], books["author"])}")
                found = True
        if not found:
            print("There are no unread books with such genre")
        return

    for books in unread_books:
        print(f"{(books["title"], books["author"])}")


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
    print("0. Exit")
