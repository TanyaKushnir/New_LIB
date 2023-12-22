from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    year_published = Column(Integer)
    book_type = Column(Integer)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)


class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(DateTime)
    return_date = Column(DateTime)

    customer = relationship("Customer", back_populates="loans")
    book = relationship("Book", back_populates="loans")


# Define relationships after defining all classes
Customer.loans = relationship("Loan", back_populates="customer")
Book.loans = relationship("Loan", back_populates="book")
