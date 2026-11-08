from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from apps.Connection_Through_ORM.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post2(Base):
    __tablename__ = "post2"

    id = Column(Integer, primary_key=True, nullable=False)
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    published= Column(Boolean, server_default='TRUE', nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password= Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))