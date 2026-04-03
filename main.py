import json
from utils import *


def load_data():
    try:
        with open('data.json', mode='r', encoding='utf-8') as library_data:
            return json.load(library_data)
    except Exception as e:
        print(f"Error message: {e}")
        return []


def main():
    library = load_data()
    if not library:
        return

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            book_search(library)
        elif choice == "4":
            display_all_books(library)
        elif choice == "5":
            view_statistics(library)
        elif choice == "6":
            update_reading_status(library)
        elif choice == "7":
            generate_reading_list(library)
        elif choice == "8":
            books_per_author(library)
        elif choice == "9":
            get_top_rated_books(library)
        elif choice == "10":
            borrow_book(library)
        elif choice == "11":
            return_borrowed_book()
        elif choice == "0":
            break
        else:
            print("Invalid choice option")
        print()


main()
