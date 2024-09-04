from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        is_active (bool): Indicates whether the user is active or not.
        is_admin (bool): Indicates whether the user is an admin or not.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Book(Base):
    """
    Represents a book.

    Attributes:
        id (int): The unique identifier of the book.
        title (str): The title of the book.
        author (str): The author of the book.
        is_borrowed (bool): Indicates whether the book is currently borrowed or not.
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    is_borrowed = Column(Boolean, default=False)
