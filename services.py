import random
from operator import itemgetter

library = [
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy", "read": True, "rating": 5},
    {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian", "read": False, "rating": None},
    {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Science Fiction", "read": True, "rating": 4},
    {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Science Fiction", "read": True, "rating": 4}
]


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
    data.append(book)
    print(f"Book Added!!! Title: {title}")
    print(data)


def remove_book(data: list):
    """this function removes a book from the libreary by the book's title"""
    book_r = input("Enter the title of the book: ")
    for book in data:
        if book["title"] == book_r:
            data.remove(book)
            print("Book deleted")
            return
    print("Book not found")


def display_all_books(data: list):
    """ this function displays all books in our library"""
    for book in data:
        print(f"Book: {book['title']} | Author: {book['author']}")


def view_statistics(data: list):
    """ this function shows the different statistics about books in our library"""
    total_books = len(data)
    total_read_books = 0
    total_unread_books = 0
    average_rating_of_read_books = 0
    most_common_genre_dict = {}
    most_common_genre = ""
    common_genre = 0

    print(data)
    new_data = sorted(data, key=itemgetter("year"))
    print(new_data)
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





# add_book(library)
# remove_book(library)
# display_all_books(library)
view_statistics(library)