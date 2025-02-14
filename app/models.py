from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from .database import Base

# Post model
class Post(Base):
    
    # table name to be used in the postgres database
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    