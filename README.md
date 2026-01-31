# Library Management System

A desktop-based Library Management System developed using Python, Tkinter, and SQLite. This application allows users to efficiently manage book records with advanced duplicate prevention and a user-friendly interface.

## Developed By
**Sonjeev Cabardo**

## Features

- **Book Management**: Add, View, Update, and Delete book records.
- **Advanced Duplicate Prevention**:
    - **Hard Block**: Automatically rejects entries with >90% similarity (e.g., typos like "Horry Potter").
    - **Fuzzy Warnings**: Alerts users of potential duplicates (70-90% similarity) for series or sequels.
- **Categorization**: Organize books by types (History, Fiction, Science, Biography, etc.).
- **Search Functionality**: Quickly find books by Title, Author, or Category.
- **Data Persistence**: Records are stored locally in a SQLite database (`library.db`).
- **Proper Error Handling**: check if any parts are missing
- **Clean UI**: User-friendly desktop interface with technical IDs hidden for a professional look.

## Technologies Used

- **Python**: Core programming language.
- **Tkinter**: GUI library for the desktop interface.
- **SQLite**: Lightweight local database for storage.
- **Difflib**: For fuzzy matching and similarity calculations.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone or download the project files.
2. Ensure `database.py` and `main.py` are in the same directory.

### Running the Application

Navigate to the project directory and run the following command:

```bash
python main.py
```

## How to Use

1. **Adding a Book**: Fill in the title, author, publisher, year, and category, then click "Add Record".
2. **Updating a Book**: Select a record from the list, modify the details in the form, and click "Update Record".
3. **Deleting a Book**: Select a record from the list and click "Delete Record".
4. **Searching**: Type your query in the search bar and click "Search". Click "Clear" to see all records again.
