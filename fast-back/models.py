from sqlalchemy import Column, String
from database import Base

class Login(Base):
    __tablename__ = 'requests'
    username = Column(String, primary_key=True)
