from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Book
from app.services.dependencies import get_current_admin_user

# Create a new APIRouter instance
router = APIRouter()


# Get a database session
def get_db():
    """
    Returns a database session.

    Returns:
        SessionLocal: The database session.
    """
    # Create a new database session
    db = SessionLocal()
    # Yield the database session
    try:
        yield db
    # Close the database session
    finally:
        db.close()


# Create a new book
@router.post("/")
def create_book(
    title: str,
    author: str,
    db: Session = Depends(get_db),
):
    """
    Creates a new book with the given title and author.
    Parameters:
    - title (str): The title of the book.
    - author (str): The author of the book.
    - db (Session): The database session.
    Returns:
    - book: The newly created book object.
    """
    # Create a new book object
    book = Book(title=title, author=author)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a book by its ID from the database.

    Parameters:
    - book_id (int): The ID of the book to retrieve.
    - db (Session): The database session.

    Returns:
    - book: The retrieved book.

    Raises:
    - HTTPException: If the book is not found in the database.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    Deletes a book from the database based on the provided book ID.

    Parameters:
    - book_id (int): The ID of the book to delete.
    - db (Session): The database session.

    Returns:
    - dict: A message indicating that the book has been deleted.

    Raises:
    - HTTPException: If the book is not found in the database.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@router.get("/")
def read_books(db: Session = Depends(get_db)):
    """
    Retrieve all books from the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - list: A list of all books in the database.
    """
    books = db.query(Book).all()
    return books
