from datetime import datetime

from pydantic import BaseModel, constr, model_validator, field_validator
from typing_extensions import Self


def validate_serial_number(value: str) -> str:
    if not value.isdigit():
        raise ValueError("Book serial_number must be an 6 digit number.")

    return value


def validate_user_card_number(value: str) -> str:
    if not value.isdigit():
        raise ValueError("borrowed_by must be an 6 digit number (user library card number).")

    return value

class BookPayload(BaseModel):
    serial_number: constr(min_length=6, max_length=6)
    title: constr(min_length=1, max_length=200)
    author: constr(min_length=1, max_length=200)
    is_borrowed: bool = False
    borrowed_date: datetime | None = None
    borrowed_by: constr(min_length=6, max_length=6) | None = None

    @model_validator(mode='before')
    def validate_consistency_of_borrowed_related_data(self) -> Self:
        print(f"validate_consistency_of_borrowed_related_data: {self}")

        if self["is_borrowed"] and not (self.get("borrowed_date") and self.get("borrowed_by")):
            raise ValueError("Borrowed book must have borrowed_date and borrowed_by.")
        elif not self["is_borrowed"] and (self.get("borrowed_date") or self.get("borrowed_by")):
            raise ValueError("Book which is not borrowed must have set borrowed_date and borrowed_by as None.")


        return self

    @field_validator('serial_number')
    @classmethod
    def validate_book_serial_number(cls, value: str) -> str:
        return validate_serial_number(value)

    @field_validator('borrowed_by')
    @classmethod
    def user_card_number_validator(cls, value: str) -> str:
        print(f"user_card_number_validator: {value}")
        if value is None:
            return value

        return validate_user_card_number(value)


class BorrowBookPayload(BaseModel):
    user_card_number: constr(min_length=6, max_length=6)


    @field_validator('user_card_number', check_fields=False)
    @classmethod
    def user_card_number_validator(cls, value: str) -> str:
        print(f"validator user_card_number: {value}")
        # return validate_user_card_number(value)
        if not value.isdigit():
            raise ValueError("borrowed_by must be an 6 digit number (user library card number).")

        return value


class BookResponse(BaseModel):
    serial_number: constr(min_length=6, max_length=6)
    title: constr(min_length=1, max_length=200)
    author: constr(min_length=1, max_length=200)
    is_borrowed: bool
    borrowed_date: datetime | None = None
    borrowed_by: constr(min_length=6, max_length=6) | None = None
