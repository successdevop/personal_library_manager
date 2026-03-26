import random
from operator import itemgetter
from database import library


def validate_string(prompt: str) -> str:
    """
    this function makes sure that an empty space is not returned
    and the text returned must be greater or equal to three characters
    :param prompt: user input
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
    :param prompt: it takes a string input
    :return: a string
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
    this function generates random numbers between, 1 to 10
    if the number is between, 1 to 5, it returns the number
    otherwise it returns None
    :return: int or None
    """
    if val is True:
        return random.randint(1, 5)

    return None


def add_book(data: list):
    """This function adds a new book to the library"""

    title = validate_string("Enter the title: ")
    author = validate_string("Enter the author's name: ")
    year = validate_numbers("Enter the year of publication: ")
    genre = validate_string("Enter the genre: ")
    read = read_book()
    rating = book_rating(read)

    book = {"title": title, "author": author, "year": year, "genre": genre, "read": read, "rating": rating}
    for b in data:
        if book["title"].casefold() == b["title"].casefold() and book["author"].casefold() == b["author"].casefold():
            print("Book already exists")
            return
    data.append(book)
    print(f"Book Added!!! Title: {title}")
    print(data)


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
        print(f"{index}. {book['title']} - {book['author']} ({'Available' if book['available'] else 'Borrowed'})")


def view_statistics(data: list):
    """ this function shows the different statistics about books in our library"""
    total_books = len(data)
    total_read_books = 0
    total_unread_books = 0
    average_rating_of_read_books = 0
    most_common_genre_dict = {}
    most_common_genre = ""
    common_genre = 0

    new_data = sorted(data, key=itemgetter("year"))
    books_per_decade = 0

    for stat in data:
        if not stat["read"]:
            total_unread_books += 1
        if stat["rating"]:
            average_rating_of_read_books += stat["rating"]
        most_common_genre_dict[stat["genre"]] = most_common_genre_dict.setdefault(stat["genre"], 0) + 1

    print(f"total books: {total_books}")
    print(f"Unread book count: {total_unread_books}")
    print(f"Average rating of read book: {average_rating_of_read_books / (total_books - total_unread_books)}")
    for k, v in most_common_genre_dict.items():
        if common_genre < v:
            most_common_genre = k
        else:
            most_common_genre = None
    print(f"Most common genre: {most_common_genre}")


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
        text = input("Enter book title: ")
    elif choice == "2":
        text = input("Enter book author: ")
    elif choice == "3":
        text = input("Enter book genre: ")

    for index, books in enumerate(book_library_data, 1):
        if text in books.get(category_of_search):
            print(f"{index}. Book_title: {books['title']} - | - Author: {books['author']}")
            found = True

    if not found:
        print(f"Books with this {category_of_search} not found")


def search_books(data: list):
    """this function displays a list of books searched for"""
    while True:
        print("Search book by category: ")
        print("1. Book title")
        print("2. Book author")
        print("3. Book genre")

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
        else:
            print("Invalid choice")


def mark_book_as_read(data: list):
    """
    the user uses this function to update a book that was previously not read
    It could be any book
    :param data: library book data
    :return: None/performs an action
    """
    looping_time = 0
    while looping_time < len(data):
        book_to_update = data[random.randint(0, len(data) - 1)]
        if not book_to_update.get("read"):
            book_to_update["read"] = True
            book_to_update["rating"] = book_rating(book_to_update["read"])
            print("Book updated to read")
            print(data)
            return
        else:
            data.remove(book_to_update)

    print("All books have been read")


def generate_reading_list(data: list, genre=None):
    """this function suggests unread books, optionally filtered by genre"""
    # Return list of unread books as tuples (title, author)
    suggest_list = []
    if genre is not None:
        for books in data:
            if books['genre'] == genre and books["read"] is False:
                suggest_list.append((books["title"], books["author"]))
    else:
        for books in data:
            if books['read'] is False:
                suggest_list.append((books["title"], books["author"]))
    print(suggest_list)


def analyze_authors(data: list):
    """this function uses dictionary to count books per author"""
    # Return dict with author names as keys, count as values
    authors = {}
    for author in data:
        val = author["author"]
        authors[val] = authors.setdefault(val, 0) + 1
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
    print("8. Classify books by authors")
    print("0. Exit")


def main():
    display_menu()

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_books(library)
        elif choice == "4":
            display_all_books(library)
        elif choice == "5":
            view_statistics(library)
        elif choice == "6":
            mark_book_as_read(library)
        elif choice == "7":
            generate_reading_list(library)
        elif choice == "8":
            analyze_authors(library)
        elif choice == "0":
            break
        else:
            print("Invalid choice option")


# main()

# mark_book_as_read(library)
# add_book(library)
# remove_book(library)
# display_all_books(library)
# view_statistics(library)
search_books(library)
# generate_reading_list(library)
# analyze_authors(library)
