from datetime import datetime
from logging import getLogger

import sqlalchemy
from fastapi import HTTPException

from app.schemas import BookResponse, BookPayload, BorrowBookPayload
from database.models.book import Book

LOGGER = getLogger(__name__)

class LibraryScenario:
    """
    LibraryScenario contains business logic for adding new book, removing book, get list of all books, borrow/return
     book.
    """
    def __init__(self, db_session):
        self.db_session = db_session

    def get_books(self) -> list[BookResponse]:
        # add pagination
        return self.db_session.query(Book).all()

    def add_book(self, payload: BookPayload) -> BookResponse:
        db_book = Book(**payload.model_dump())
        self.db_session.add(db_book)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as exc:
            raise HTTPException(status_code=409, detail=f"Book with serial_number '{payload.serial_number}' already exists.")
        self.db_session.refresh(db_book)
        print(f"db_book.serial_number: {db_book.serial_number}")
        return BookResponse(serial_number=db_book.serial_number, title=db_book.title,
                            author=db_book.author,
                            is_borrowed=db_book.is_borrowed,
                            borrowed_date=db_book.borrowed_date,
                            borrowed_by=db_book.borrowed_by
                            )

    def remove_book(self, serial_number: str) -> None:
        with self.db_session.begin():
            book_to_delete = self.db_session.query(Book).filter(Book.serial_number == serial_number).one_or_none()

            if not book_to_delete:
                raise HTTPException(status_code=404, detail="Book with serial_number does not exist.")

            # Delete the book
            self.db_session.delete(book_to_delete)

        return None

    def borrow_book(self, serial_number: str, payload: BorrowBookPayload) -> BookResponse:
        db_book_data = None
        # TODO: maybe add try/except and rollback (check if it won't work automatically with begin context manager)
        with self.db_session.begin():
            book_to_update = self.db_session.query(Book).filter(Book.serial_number == serial_number).with_for_update().first()

            if not book_to_update:
                raise HTTPException(status_code=409, detail="Book with serial_number does not exist.")
            
            if book_to_update.is_borrowed:
                raise HTTPException(status_code=409, detail="Book with serial_number is already borrowed.")

            book_to_update.is_borrowed = True
            book_to_update.borrowed_date = datetime.now()
            book_to_update.borrowed_by = payload.user_card_number
            self.db_session.add(book_to_update)

            db_book_data = {
                "serial_number": book_to_update.serial_number,
                "title": book_to_update.title,
                "author": book_to_update.author,
                "is_borrowed": book_to_update.is_borrowed,
                "borrowed_date": book_to_update.borrowed_date,
                "borrowed_by": book_to_update.borrowed_by
            }

        return BookResponse(**db_book_data)
    
    def return_book(self, serial_number: str) -> BookResponse:
        db_book_data = None
        # TODO: maybe add try/except and rollback (check if it won't work automatically with begin context manager)
        with self.db_session.begin():
            book_to_update = self.db_session.query(Book).filter(
                Book.serial_number == serial_number).with_for_update().first()

            if not book_to_update:
                raise HTTPException(status_code=409, detail="Book with serial_number does not exist.")

            if not book_to_update.is_borrowed:
                raise HTTPException(status_code=409, detail="Book with serial_number is not borrowed, so cannot be returned.")

            book_to_update.is_borrowed = False
            book_to_update.borrowed_date = None
            book_to_update.borrowed_by = None
            self.db_session.add(book_to_update)

            db_book_data = {
                "serial_number": book_to_update.serial_number,
                "title": book_to_update.title,
                "author": book_to_update.author,
                "is_borrowed": book_to_update.is_borrowed,
                "borrowed_date": book_to_update.borrowed_date,
                "borrowed_by": book_to_update.borrowed_by
            }

        return BookResponse(**db_book_data)
