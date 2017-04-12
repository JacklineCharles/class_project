import sys 

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
Base = declarative_base()

class User(Base):


    __tablename__ = 'user'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(80), nullable = False)
    username = Column(String(80), nullable = False)
    email = Column(String(100), nullable = True)
    password = Column(String)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.hashed_password(password)

    def hashed_password(self, new_password):
        """
        Hashes the new entered password
        """
        self.password = generate_password_hash(new_password)

    
    def generate_token(self, expiration = 1200):
        """
        generates token
        """
        serialize = Serialize(app.config['SECRET_KEY'], expire_time = expiration)
        return serialize.dumps({'id': self.id})

class Ideas(Base):

    __tablename__ = 'idea'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    upvotes = Column(Integer, default = 0)
    downvotes = Column(Integer, default = 0)

class Comments(Base):

    __tablename__ = 'comments'

    id = Column(Integer, primary_key = True, autoincrement = True)
    comment = Column(String(250), nullable = True)
    idea_id = Column(Integer, ForeignKey('idea.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
        
#end of file code
engine = create_engine('sqlite:///userideas.db')
Base.metadata.create_all(engine)