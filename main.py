from core import *
from storage import load_json_data
from config import DATA_FILE, USERS_FILE


def main():
    library = load_json_data(DATA_FILE)
    if not library:
        print("No book in the Library")
        return

    users = load_json_data(USERS_FILE)

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
            borrow_book(library, users)
        elif choice == "11":
            return_borrowed_book(library, users)
        elif choice == "12":
            book_overdue_system_check(library)
        elif choice == "13":
            pagination(library, 1, 3)
        elif choice == "14":
            print(sort_books(library, "rating"))
        elif choice == "0":
            break
        else:
            print("Invalid choice option")
        print()


main()
