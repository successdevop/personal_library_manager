import json
from utils import *


def load_data():
    try:
        with open('data.json', mode='r', encoding='utf-8') as library_data:
            return json.load(library_data)
    except Exception as e:
        print(f"Error message: {e}")
        return []


library = load_data()

# add_book(library)
# display_all_books(library)
# update_reading_status(library)
# books_per_author(library)