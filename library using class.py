
class Book:
    def __init__(self,title,author):
        self.title=title
        self.author=author
        self.is_borrowed=False
    def show_info(self):
        status="Borrowed" if self.is_borrowed else "Available"
        print(f"Title: {self.title}, Author: {self.author}, Status: {status}")
class Library:
    def __init__(self,name):
        self.name=name
        self.books=[]
    def add_book(self,title,author):
        book=Book(title,author)
        self.books.append(book)
        print(f"Added: {title} by {author}")
    def show_all_books(self):
        print(f"\n---{self.name} Catalog---")
            print("No books available.")
            return
        for book in self.books:
            book.show_info()
    def find_book(self,title):
        for book in self.books:
            if book.title.lower()==title.lower():
                return book
        return None
    def borrow_book(self,title):
        book=self.find_book(title)
        if not book:
            print(f"Book '{title}' not found in the library.")
        elif book.is_borrowed:
            print(f"Book '{title}' is already borrowed.")
        else:
            book.is_borrowed=True
            print(f"You have borrowed '{title}'.")
    def return_book(self,title):
        book=self.find_book(title)
        if not book:
            print(f"Book '{title}' not found in the library.")
        elif not book.is_borrowed:
            print(f"Book '{title}' was not borrowed.")
        else:
            book.is_borrowed=False
            print(f"You have returned '{title}'.")
        
        
#MAIN PROGRAM
def main():
    my_library=Library("AK Library")
    while True:
        print("\n---AK Library Menu---")
        print("1. Show all Books")
        print("2. Add a new Book")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Exit")
        choice=input("Enter your choice (1-5): ")
        
        if choice=="1":
            my_library.show_all_books()
        elif choice=="2":
            title=input("Enter book title: ")
            author=input("Enter book author: ")
            my_library.add_book(title,author)
        elif choice=="3":
            my_library.show_all_books()
        elif choice=="3":
            title=input("Enter book title to borrow: ")
            my_library.borrow_book(title)
        elif choice=="4":
            title=input("Enter book title to return: ")
            my_library.return_book(title)
        elif choice=="5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    main()  