from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base, engine


class Posts(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    description = Column(String)


Base.metadata.create_all(bind=engine)
