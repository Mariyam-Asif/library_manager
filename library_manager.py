import os

# Store library data
LIBRARY_FILE = "library.txt"

# Load library data from file
def load_library():
    library = []
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, "r") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        title, author, year, genre, read_status = parts
                        library.append({
                            "title": title,
                            "author": author,
                            "year": int(year),
                            "genre": genre,
                            "read": read_status == "yes"
                        })
        except IOError:
            print("⚠️ Warning: Library file is corrupted. Starting with an empty library.")
    return library

# Save library data to a file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        for book in library:
            file.write(f"{book['title']}|{book['author']}|{book['year']}|{book['genre']}|{'yes' if book['read'] else 'no'}\n")

# Load existing library data
library = load_library()

# Add a new book
def add_book():
    title = input("Enter the book title: ").strip()

    if any(book["title"].lower() == title.lower() for book in library):
        print("⚠️ This book already exists in your library.")
        return
    
    author = input("Enter the author: ").strip()
    year = input("Enter the publication year: ").strip()
    genre = input("Enter the genre: ").strip()

    if not title or not author or not year.lstrip('-').isdigit():
        print("⚠️ Invalid input. Title, author, and year are required.")
        return

    while True:
        read_status = input("Have you read this book? (yes/no: )").strip().lower()
        if read_status in ["yes", "no"]:
            break
        print("⚠️ Invalid input. Please enter 'yes' or 'no'.")

    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read_status == "yes"
    }
    
    library.append(book)
    save_library(library)
    print("✅ Book added successfully!")

# Edit a book
def edit_book():
    title = input("Enter the title of the book to edit: ").strip()

    for book in library:
        if book["title"].lower() == title.lower():
            print("Editing book: ", book)

            new_title = input("Enter new title (press Enter to keep unchanged): ").strip() or book["title"]
            new_author = input("Enter new author (press Enter to keep unchanged): ").strip() or book["author"]
            new_year = input("Enter new year (press Enter to keep unchanged): ").strip() or str(book["year"])
            new_genre = input("Enter new genre (press Enter to keep unchanged): ").strip() or book["genre"]
            new_read_status = input("Have you read this book? (yes/no, press Enter to keep unchanged): ").strip().lower()

            if new_year.isdigit():
                book["year"] = int(new_year)
            book["title"], book["author"], book["genre"] = new_title, new_author, new_genre
            if new_read_status in ["yes", "no"]:
                book["read"] = new_read_status == "yes"
            
            save_library(library)
            print("✅ Book updated successfully!")
            return
        
    print("⚠️ Book not found.")

# Remove a book
def remove_book():
    title = input("Enter the title of the book to remove: ").strip()
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            print("✅ Book removed successfully!")
            return
    print("⚠️ Book not found.")
    
# Search for a book
def search_book():
    print("Search by:\n1. Title\n2. Author")
    choice = input("Search for a book: ").strip()
    
    if choice not in ["1", "2"]:
        print("⚠️ Invalid choice. Please enter 1 for Title or 2 for Author.")
        return
    keyword = input("Enter the title/author to search: ").strip().lower()
    if choice == "1":
        matches = [book for book in library if book["title"].lower() == keyword]
    else:
        matches = [book for book in library if book["author"].lower() == keyword]

    if matches:
        print("\n📚 Matching Books:")
        for idx, book in enumerate(matches, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        print("⚠️ No matching books found.")

# Display all books
def display_books():
    if not library:
        print("⚠️ Your library is empty.")
        return
    print("\n📚 Your Library:")
    for idx, book in enumerate(library, 1):
        read_status = "Read" if book["read"] else "Unread"
        print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

# Display statistics
def display_statistics():
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    print(f"\n📊 Library Statistics:")
    print(f"📚 Total books: {total_books}")
    print(f"📖 Books read: {read_books}")
    print(f"✅ Percentage read: {percentage_read:.2f}%")

# Main menu
def main_menu():
    while True:
        print("\n📖 Welcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Edit a book")
        print("3. Remove a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Display statistics")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            edit_book()
        elif choice == "3":
            remove_book()
        elif choice == "4":
            search_book()
        elif choice == "5":
            display_books()
        elif choice == "6":
            display_statistics()
        elif choice == "7":
            save_library(library)
            print("📁 Library saved to file. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please enter a number between 1 and 7.")

# Running the program
if __name__ == "__main__":
    main_menu()