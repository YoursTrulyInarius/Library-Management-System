import sqlite3
import logging

# Set up basic logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    def __init__(self, db_file="library.db"):
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            raise

    def create_table(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publisher TEXT NOT NULL,
                    year TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'Other'
                )
            """)
            # Check if category column exists (for migration)
            self.cur.execute("PRAGMA table_info(books)")
            columns = [column[1] for column in self.cur.fetchall()]
            if 'category' not in columns:
                self.cur.execute("ALTER TABLE books ADD COLUMN category TEXT NOT NULL DEFAULT 'Other'")
            
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating/updating table: {e}")
            self.conn.rollback()

    def check_duplicate(self, title, author):
        try:
            self.cur.execute("SELECT * FROM books WHERE title=? AND author=?", (title, author))
            return self.cur.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Error checking duplicates: {e}")
            return False

    def add_book(self, title, author, publisher, year, category):
        if self.check_duplicate(title, author):
            raise ValueError(f"A book with title '{title}' by '{author}' already exists.")
        
        try:
            self.cur.execute("INSERT INTO books (title, author, publisher, year, category) VALUES (?, ?, ?, ?, ?)",
                             (title, author, publisher, year, category))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error adding book: {e}")
            self.conn.rollback()
            raise

    def fetch_records(self):
        try:
            self.cur.execute("SELECT * FROM books")
            return self.cur.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching records: {e}")
            return []

    def delete_book(self, book_id):
        try:
            self.cur.execute("DELETE FROM books WHERE id=?", (book_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error deleting book: {e}")
            self.conn.rollback()
            raise

    def update_book(self, book_id, title, author, publisher, year, category):
        try:
            # Check if another book with same title/author exists (excluding this ID)
            self.cur.execute("SELECT * FROM books WHERE title=? AND author=? AND id!=?", (title, author, book_id))
            if self.cur.fetchone():
                raise ValueError(f"Another book with title '{title}' by '{author}' already exists.")

            self.cur.execute("""
                UPDATE books SET title=?, author=?, publisher=?, year=?, category=? WHERE id=?
            """, (title, author, publisher, year, category, book_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error updating book: {e}")
            self.conn.rollback()
            raise

    def search_books(self, query):
        try:
            self.cur.execute("""
                SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
            """, (f'%{query}%', f'%{query}%', f'%{query}%'))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error searching books: {e}")
            return []

    def get_similar_books(self, title, author):
        """Finds books with similar titles by the same author and returns (title, ratio)."""
        try:
            from difflib import SequenceMatcher
            
            self.cur.execute("SELECT title FROM books WHERE author=?", (author,))
            existing_titles = [row[0] for row in self.cur.fetchall()]
            
            similar = []
            for existing in existing_titles:
                # Normalize for comparison
                t1 = title.lower().strip()
                t2 = existing.lower().strip()
                
                # Direct match
                if t1 == t2:
                    similar.append((existing, 1.0))
                    continue
                
                # Fuzzy ratio check
                ratio = SequenceMatcher(None, t1, t2).ratio()
                
                # Substring check bonus
                if t1 in t2 or t2 in t1:
                    # Give substring matches a high score but not necessarily 1.0
                    ratio = max(ratio, 0.85)
                
                if ratio > 0.7:
                    similar.append((existing, ratio))
            
            # Sort by highest ratio first
            similar.sort(key=lambda x: x[1], reverse=True)
            return similar
        except Exception as e:
            logging.error(f"Error finding similar books: {e}")
            return []

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
