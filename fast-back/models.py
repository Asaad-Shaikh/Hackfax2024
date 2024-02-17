from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Login(Base):
    __tablename__='login'

    masonid = Column(String, primary_key=True)
    password = Column(String)
    