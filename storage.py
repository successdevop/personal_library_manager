import json


def load_json_data(filename):
    """this functions loads data into our python list by reading/deserializing data from our json file/document"""
    try:
        with open(filename, mode="r", encoding="utf-8") as file_reader:
            return json.load(file_reader)
    except Exception as e:
        print(f"Error message: {e} | File is empty, starting with an empty list")
        return []


def save_json_data(data, filename):
    """this function updates our json file/document by serialising every change made in our data object"""
    with open(filename, mode="w", encoding="utf-8") as file_writer:
        json.dump(data, file_writer, indent=4)
