from models import Book, Customer, Loan
from dal import LibraryDAL
from datetime import datetime


def main_menu():
    print("1. Add a new customer")
    print("2. Add a new book")
    print("3. Loan a book")
    print("4. Return a book")
    print("5. Display all books")
    print("6. Display all customers")
    print("7. Display all loans")
    print("8. Display late loans")
    print("9. Find book by name")
    print("10. Find customer by name")
    print("11. Remove book")
    print("12. Remove customer")
    print("0. Exit")


def main():
    dal = LibraryDAL()
    dal.create_tables()

    while True:
        main_menu()

        choice = input("Enter your choice: ").strip()

        print(f"DEBUG: Choice entered: '{choice}'")

        if choice == '1':
            name = input("Enter customer name: ")
            city = input("Enter customer city: ")
            age = int(input("Enter customer age: "))
            customer = Customer(name=name, city=city, age=age)
            dal.add_customer(customer)

        elif choice == '2':
            name = input("Enter book name: ")
            author = input("Enter book author: ")
            year_published = int(input("Enter year published: "))
            book_type = int(input("Enter book type (1/2/3): "))
            book = Book(name=name, author=author, year_published=year_published, book_type=book_type)
            dal.add_book(book)

        elif choice == '3':
            cust_id = int(input("Enter customer ID: "))
            book_id = int(input("Enter book ID: "))
            loan_date_str = input("Enter loan date (YYYY-MM-DD): ")
            return_date_str = input("Enter return date (YYYY-MM-DD): ")
            # Convert date strings to datetime objects
            loan_date = datetime.strptime(loan_date_str, '%Y-%m-%d')
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d') if return_date_str else None
            loan = Loan(cust_id=cust_id, book_id=book_id, loan_date=loan_date, return_date=return_date)
            dal.loan_book(loan)

        elif choice == '4':
            cust_id = int(input("Enter customer ID: "))
            book_id = int(input("Enter book ID: "))
            dal.return_book(cust_id, book_id)

        elif choice == '5':
            all_books = dal.get_all_books()
            print("All Books:")
            for book in all_books:
                print(f"{book.id}: {book.name} by {book.author}, Type: {book.book_type}")

        elif choice == '6':
            all_customers = dal.get_all_customers()
            print("All Customers:")
            for customer in all_customers:
                print(f"{customer.id}: {customer.name}, City: {customer.city}, Age: {customer.age}")

        elif choice == '7':
            all_loans = dal.get_all_loans()
            print("All Loans:")

            for loan in all_loans:
                customer_name = loan.customer.name if loan.customer else "Unknown Customer"
                book_title = loan.book.name if loan.book else "Unknown Book"
                print(f"Customer {customer_name} ({loan.cust_id}) borrowed {book_title} ({loan.book_id})")

        elif choice == '8':
            late_loans = dal.get_late_loans()
            print("Late Loans:")
            for loan in late_loans:
                print(
                    f"Customer {loan.customer.name} ({loan.customer.id}) has a late loan for {loan.book.name} ({loan.book.id})")

        elif choice == '9':
            book_name = input("Enter book name: ")
            found_books = dal.find_books_by_name(book_name)
            print(f"Books with name '{book_name}':")
            for book in found_books:
                print(f"{book.id}: {book.name} by {book.author}, Type: {book.book_type}")

        elif choice == '10':
            customer_name = input("Enter customer name: ")
            found_customers = dal.find_customers_by_name(customer_name)
            print(f"Customers with name '{customer_name}':")
            for customer in found_customers:
                print(f"{customer.id}: {customer.name}, City: {customer.city}, Age: {customer.age}")

        elif choice == '11':
            book_id = int(input("Enter book ID to remove: "))
            dal.remove_book(book_id)

        elif choice == '12':
            customer_id = int(input("Enter customer ID to remove: "))
            dal.remove_customer(customer_id)

        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
