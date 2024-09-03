from typing import Annotated

from fastapi import FastAPI, Depends
from logging import getLogger
from app.schemas import BookResponse, BookPayload, validate_serial_number, \
    BorrowBookPayload
from database.database import Base, engine, get_db, SessionLocal
from scenarios.library import LibraryScenario
LOGGER = getLogger(__name__)

library_app = FastAPI(title="Library application")

# TODO: use lifespan https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# TODO: add 500 errors handler

@library_app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_scenario(db_session: Annotated[SessionLocal, Depends(get_db)]) -> LibraryScenario:
    return LibraryScenario(db_session=db_session)

@library_app.post("/books", tags=["Books"])
async def add_book(payload: BookPayload, scenario: Annotated[LibraryScenario, Depends(get_scenario)]) -> BookResponse:
    LOGGER.info(f"Add book with payload: {payload}.")
    return scenario.add_book(payload)

@library_app.get("/books", tags=["Books"])
async def get_books(scenario = Depends(get_scenario)) -> list[BookResponse]:
    LOGGER.info(f"Get books")
    return scenario.get_books()

@library_app.delete("/books/{serial_number}", tags=["Books"])
async def get_books(scenario = Depends(get_scenario), serial_number = Depends(validate_serial_number),) -> None:
    LOGGER.info(f"Delete book: {serial_number}.")
    return scenario.remove_book(serial_number)

@library_app.post("/books/{serial_number}/borrow", tags=["Books"])
async def borrow_book(payload: BorrowBookPayload, serial_number = Depends(validate_serial_number), scenario = Depends(get_scenario),) -> BookResponse:
    LOGGER.info(f"Borrow book, serial number: {serial_number}, user card number: {payload.user_card_number}.")
    return scenario.borrow_book(serial_number=serial_number, payload=payload)

@library_app.post("/books/{serial_number}/return", tags=["Books"])
async def return_book(serial_number = Depends(validate_serial_number), scenario = Depends(get_scenario)) -> BookResponse:
    LOGGER.info(f"Return book, serial_number: {serial_number}.")
    return scenario.return_book(serial_number)
