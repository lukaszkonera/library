from sqlalchemy import Boolean, Column, String, DateTime
from database.database import Base

class Book(Base):
    __tablename__ = "books"

    serial_number = Column(String(6), primary_key=True, index=True, unique=True)
    title = Column(String, index=True)
    author = Column(String)
    is_borrowed = Column(Boolean, default=False)
    borrowed_date = Column(DateTime, nullable=True)
    borrowed_by = Column(String(6), index=True)