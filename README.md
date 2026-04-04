# 📚 Smart Library Management System (CLI)

A command-line based Library Management System built with Python that allows users 
to manage books, track borrowing activities, and generate useful insights from stored data.

---

## 🚀 Features

### 📖 Book Management

* Add new books
* Remove books
* View all books
* Prevent duplicate entries

### 🔍 Search System

* Search by title, author, genre, or rating
* Case-insensitive and partial matching

### 📊 Analytics & Insights

* Total books in library
* Available vs borrowed books
* Most common genre
* Read vs unread books
* Average rating of books

### 📚 Reading Features

* Mark books as read
* Automatically assign ratings to read books
* Generate reading lists (optionally filtered by genre)

### 💸 Borrowing System

* Borrow books with timestamp tracking
* Return books with return time recorded
* Track users and their borrowed books

### 🏆 Ranking System

* View top-rated books

---

## 🧠 Technologies Used

* Python (Core Language)
* JSON (Data Storage)
* Datetime (Time Tracking)
* File Handling (Persistent Storage)

---

## 📁 Project Structure

```bash
library_project/
│
├── main.py          # Entry point of the application
├── core.py          # Core logic and helper functions
├── config.py        # Stores the file name for data and users
├── data.json        # Stores book data
├── users.json       # Stores user borrowing data
```
---

## ⚙️ How It Works

* All books are stored in `data.json`
* Borrowing information is stored in `users.json`
* The system reads from these files when it starts
* Every update (add, borrow, return, etc.) is saved automatically

---

## ▶️ How to Run the Project

1. Clone the repository:

```bash
git clone <https://github.com/successdevop/library_management_system_CLI.git>
```

2. Navigate into the project folder:

```bash
cd library_management_system_CLI
```

3. Run the program:

```bash
python main.py
```

---

## 🖥️ Menu Options

```text
1. Add a book
2. Remove a book
3. Search for books
4. Display all books
5. View statistics
6. Mark book as read
7. Generate reading list
8. Books per author
9. Get top rated books
10. Borrow book
11. Return book
12. Overdue books
13. Pagination
14. Sort books
0. Exit
```

---

## 📌 Example Book Data

```json
{
    "id": 1,
    "title": "the hobbit",
    "author": "j.r.r. tolkien",
    "year": 1937,
    "genre": "fantasy",
    "read": true,
    "rating": 5,
    "available": true,
    "borrowed_at": null,
    "returned_at": null
}
```

---

## 🔥 Future Improvements

* Error logging system
* Convert to a web application (Flask/Django)
* Replace JSON with a database (SQLite/PostgreSQL)

---

## 🎯 Learning Outcomes

This project demonstrates:

* File handling and data persistence
* Working with JSON data
* Structuring a real-world CLI application
* Use of functions, loops, and conditionals
* Basic system design and problem-solving

---

## 👨‍💻 Author

Built by **[Success.I.R (successdevop)]**

---

## 📄 License

This project is open-source and available for learning purposes.