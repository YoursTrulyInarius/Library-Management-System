import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1100x600")
        
        try:
            self.db = Database()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not initialize database: {e}")
            self.root.destroy()
            return

        # Variables
        self.id_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.publisher_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # UI Components
        self.setup_ui()
        self.display_all()

    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Library Management System", font=("Arial", 24, "bold"), pady=20)
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Main Body
        main_frame = tk.Frame(self.root, padx=20)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left Frame: Form
        form_frame = tk.LabelFrame(main_frame, text="Book Details", font=("Arial", 12, "bold"), padx=10, pady=10)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Field Layout
        tk.Label(form_frame, text="Book Title:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.title_var, font=("Arial", 10), width=35).grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Author:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.author_var, font=("Arial", 10), width=35).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Publisher:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.publisher_var, font=("Arial", 10), width=35).grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Year:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.year_var, font=("Arial", 10), width=35).grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Category:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        categories = ["History", "Fiction", "Science", "Biography", "Art", "Technology", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=("Arial", 10), width=33, state="readonly")
        self.category_combo.grid(row=4, column=1, pady=5)
        self.category_combo.set("Other")

        tk.Label(form_frame, text="Quantity:", font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.quantity_var, font=("Arial", 10), width=35).grid(row=5, column=1, pady=5)

        # Right Frame: Table
        table_frame = tk.Frame(main_frame)
        table_frame.grid(row=0, column=1, sticky="nsew")

        # Search Bar
        search_frame = tk.Frame(table_frame)
        search_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 10)).pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Search", command=self.search_books, width=10).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Clear", command=self.display_all, width=10).pack(side=tk.LEFT, padx=5)

        # Treeview (Displaying Title, Author, Publisher, Year, Category, Quantity)
        # ID is included in columns but we won't show it to the user.
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Title", "Author", "Publisher", "Year", "Category", "Quantity"), show="headings")
        
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Publisher", text="Publisher")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity", text="Quantity")
        
        # Hide ID column
        self.tree.heading("ID", text="")
        self.tree.column("ID", width=0, stretch=tk.NO)
        
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        self.tree.column("Publisher", width=150)
        self.tree.column("Year", width=80)
        self.tree.column("Category", width=100)
        self.tree.column("Quantity", width=80)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.get_selected_row)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Button Frame
        button_frame = tk.Frame(self.root, pady=20)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        btn_config = [
            ("Add Record", self.add_book, "green"),
            ("Update Record", self.update_book, "orange"),
            ("Delete Record", self.delete_book, "red"),
            ("Clear Fields", self.clear_fields, "blue"),
            ("Exit", self.root.quit, "black")
        ]

        for text, cmd, color in btn_config:
            tk.Button(button_frame, text=text, command=cmd, font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=10, expand=True)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def display_all(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.db.fetch_records():
            self.tree.insert("", tk.END, values=row)
        self.search_var.set("")

    def add_book(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        publisher = self.publisher_var.get().strip()
        year = self.year_var.get().strip()
        category = self.category_var.get()
        quantity = self.quantity_var.get().strip()

        if not all([title, author, publisher, year, category, quantity]):
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        if not quantity.isdigit():
            messagebox.showerror("Input Error", "Quantity must be a number!")
            return

        try:
            # Check for similarities
            similar_results = self.db.get_similar_books(title, author)
            
            if similar_results:
                top_match, high_ratio = similar_results[0]
                
                # Hard Block for very high similarity (typos/duplicates)
                if high_ratio >= 0.9:
                    messagebox.showerror("Duplicate Blocked", 
                                        f"Access Denied: A very similar book already exists by this author:\n\n"
                                        f"Existing: '{top_match}'\n"
                                        f"Incoming: '{title}'\n\n"
                                        f"Please correct the title if it's a typo.")
                    return
                
                # Warning for moderate similarity (sequels/series)
                elif high_ratio >= 0.7:
                    similar_list = "\n- ".join([t for t, r in similar_results])
                    msg = (f"Similar books by this author already exist:\n- {similar_list}\n\n"
                           f"Are you sure this is a different book and NOT a duplicate?")
                    if not messagebox.askyesno("Potential Duplicate", msg):
                        return

            self.db.add_book(title, author, publisher, year, category, int(quantity))
            messagebox.showinfo("Success", "Record added successfully!")
            self.clear_fields()
            self.display_all()
        except Exception as e:
            messagebox.showerror("Database Error", f"An unexpected error occurred: {e}")

    def get_selected_row(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        data = self.tree.item(selected_item)["values"]
        if data:
            self.id_var.set(data[0])
            self.title_var.set(data[1])
            self.author_var.set(data[2])
            self.publisher_var.set(data[3])
            self.year_var.set(data[4])
            self.category_var.set(data[5])
            self.quantity_var.set(data[6])

    def update_book(self):
        book_id = self.id_var.get()
        if not book_id:
            messagebox.showwarning("Selection Required", "Please select a record to update!")
            return
        
        try:
            title, author = self.title_var.get().strip(), self.author_var.get().strip()
            quantity = self.quantity_var.get().strip()

            if not quantity.isdigit():
                messagebox.showerror("Input Error", "Quantity must be a number!")
                return
            
            # Similar check for update
            similar_results = self.db.get_similar_books(title, author)
            # Filter out the current record's title from similarity check
            # Note: Since we are updating, it's okay if the top match is the CURRENT record title.
            # But we need to check if there's ANOTHER record that is too similar.
            
            # Better check: Filter by ID (which we don't easily have here without fetching all)
            # For simplicity, we filter out EXACT matches with the current title if they exist.
            other_similars = [(t, r) for t, r in similar_results if r < 1.0 or t != title]
            
            if other_similars:
                top_match, high_ratio = other_similars[0]
                if high_ratio >= 0.9:
                    messagebox.showerror("Update Blocked", 
                                        f"Cannot update: The new title is too similar to another record:\n\n"
                                        f"Existing: '{top_match}'\n"
                                        f"Please use a unique title.")
                    return
                elif high_ratio >= 0.7:
                    similar_list = "\n- ".join([t for t, r in other_similars])
                    if not messagebox.askyesno("Potential Duplicate", 
                                              f"The new title is similar to:\n- {similar_list}\n\nProceed anyway?"):
                        return

            self.db.update_book(book_id, title, self.author_var.get(), 
                               self.publisher_var.get(), self.year_var.get(), self.category_var.get(), int(quantity))
            messagebox.showinfo("Success", "Record updated successfully!")
            self.clear_fields()
            self.display_all()
        except ValueError as ve:
            messagebox.showwarning("Duplicate Record", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"An unexpected error occurred: {e}")

    def delete_book(self):
        book_id = self.id_var.get()
        if not book_id:
            messagebox.showwarning("Selection Required", "Please select a record to delete!")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            try:
                self.db.delete_book(book_id)
                messagebox.showinfo("Success", "Record deleted!")
                self.clear_fields()
                self.display_all()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not delete record: {e}")

    def search_books(self):
        query = self.search_var.get().strip()
        if not query:
            self.display_all()
            return
        
        self.tree.delete(*self.tree.get_children())
        results = self.db.search_books(query)
        if not results:
            messagebox.showinfo("Search Results", "No matching records found.")
            self.display_all()
        else:
            for row in results:
                self.tree.insert("", tk.END, values=row)

    def clear_fields(self):
        self.id_var.set("")
        self.title_var.set("")
        self.author_var.set("")
        self.publisher_var.set("")
        self.year_var.set("")
        self.category_var.set("Other")
        self.quantity_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()
