from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import UnicodeText

from potemkin.models.base import Base


class ApplicationInstance(Base):
    """An installed instance of an LTI app."""
    __tablename__ = "application_instance"
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    launch_url = Column(UnicodeText)
    consumer_key = Column(UnicodeText)
    shared_secret = Column(UnicodeText)
