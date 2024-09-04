from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Book

# Create a new APIRouter instance
router = APIRouter()


def get_db():
    """
    Returns a database session.

    Returns:
        SessionLocal: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_book(title: str, author: str, db: Session = Depends(get_db)):
    """
    Creates a new book with the given title and author.
    Parameters:
    - title (str): The title of the book.
    - author (str): The author of the book.
    - db (Session): The database session.
    Returns:
    - book: The newly created book object.
    """
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
