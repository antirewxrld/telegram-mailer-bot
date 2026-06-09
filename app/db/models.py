from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

class EmailMessage(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)

    message_id = Column(String)
    sender = Column(String)
    subject = Column(String)