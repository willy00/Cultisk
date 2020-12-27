from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entry"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    favorite = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'entry',
        'polymorphic_on': type
    }

    def __init__(self, type):
        self.type = type


class Password(Entry):
    __tablename__ = 'password'

    id = Column(Integer, ForeignKey('entry.id'), primary_key=True)
    username = Column(String)
    password = Column(String)
    totp_secret = Column(String, nullable=True, default=None)

    __mapper_args__ = {
        'polymorphic_identity': 'password',
    }

    def __init__(self, username, password, totp_secret=None):
        super(Password, self).__init__("password")
        self.username = username
        self.password = password
        self.totp_secret = totp_secret


class Note(Entry):
    __tablename__ = 'note'

    id = Column(Integer, ForeignKey('entry.id'), primary_key=True)
    content = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'note',
    }

    def __init__(self, content):
        super(Note, self).__init__("note")
        self.content = content