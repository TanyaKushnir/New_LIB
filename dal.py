from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book, Customer, Loan, Base
from datetime import datetime
from sqlalchemy.orm import joinedload


class LibraryDAL:
    def __init__(self):
        self.engine = create_engine('sqlite:///library.db')
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_book(self, book):
        session = self.Session()
        session.add(book)
        session.commit()
        session.close()

    def add_customer(self, customer):
        session = self.Session()
        session.add(customer)
        session.commit()
        session.close()

    def loan_book(self, loan):
        session = self.Session()
        session.add(loan)
        session.commit()
        session.close()

    def return_book(self, cust_id, book_id):
        session = self.Session()
        loan = session.query(Loan).filter_by(cust_id=cust_id, book_id=book_id, return_date=None).first()
        if loan:
            loan.return_date = datetime.now()
            session.commit()
            print(f"Book returned successfully by customer {loan.customer.name} ({loan.customer.id}).")
        else:
            print("No active loan found for the specified customer and book.")
        session.close()

    def get_all_books(self):
        session = self.Session()
        all_books = session.query(Book).all()
        session.close()
        return all_books

    def get_all_customers(self):
        session = self.Session()
        all_customers = session.query(Customer).all()
        session.close()
        return all_customers

    def get_all_loans(self):
        session = self.Session()
        try:
            all_loans = (
                session.query(Loan)
                .options(joinedload(Loan.customer), joinedload(Loan.book))
                .all()
            )
            return all_loans
        except Exception as e:
            print(f"Error in get_all_loans: {e}")
            return None
        finally:
            session.close()

    def get_late_loans(self):
        session = self.Session()
        late_loans = session.query(Loan).filter(Loan.return_date == None, Loan.loan_date < datetime.now()).all()
        session.close()
        return late_loans

    def find_books_by_name(self, book_name):
        session = self.Session()
        found_books = session.query(Book).filter(Book.name.ilike(f"%{book_name}%")).all()
        session.close()
        return found_books

    def find_customers_by_name(self, customer_name):
        session = self.Session()
        found_customers = session.query(Customer).filter(Customer.name.ilike(f"%{customer_name}%")).all()
        session.close()
        return found_customers

    def remove_book(self, book_id):
        session = self.Session()
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
            print(f"Book '{book.name}' (ID: {book.id}) removed successfully.")
        else:
            print(f"No book found with ID: {book_id}.")
        session.close()

    def remove_customer(self, customer_id):
        session = self.Session()
        customer = session.query(Customer).filter_by(id=customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
            print(f"Customer '{customer.name}' (ID: {customer.id}) removed successfully.")
        else:
            print(f"No customer found with ID: {customer_id}.")
        session.close()
