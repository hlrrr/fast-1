
from sqlalchemy     import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.sql.sqltypes        import TIMESTAMP
from sqlalchemy.sql.expression      import text
from sqlalchemy.orm     import relationship, Session

from .database      import Base, get_db


class Common():
    id = Column(Integer, primary_key=True, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=True, onupdate=text('now()'))
    

class Post(Common, Base):
    __tablename__ = 'posts'
    # __allow_unmapped__ = True
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='NO ACTION'), nullable=False )
    owner = relationship('User')


class User(Common, Base):
    __tablename__ = 'users'
    email = Column(String(length=255), nullable=True, unique=True)
    password = Column(String(length=255), nullable=False)
    # status = Column(Enum("active", "deleted", "blocked"), default="active")
    # name = Column(String(length=255), nullable=True)
    # phone_number = Column(String(length=20), nullable=True, unique=True)
    # profile_img = Column(String(length=1000), nullable=True)
    # sns_type = Column(Enum("FB", "G", "K"), nullable=True)
    # marketing_agree = Column(Boolean, nullable=True, default=True)
    # keys = relationship("ApiKeys", back_populates="users")


class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='NO ACTION'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='NO ACTION'), primary_key=True)


# class UserSNS(Common, Base):
#     __tablename__ = 'users_with_sns'
#     email = Column(String(length=255), nullable=True, unique=True)
#     password = Column(String(length=255), nullable=False)
#     status = Column(Enum("active", "deleted", "blocked"), default="active")
#     name = Column(String(length=255), nullable=True)
#     phone_number = Column(String(length=20), nullable=True, unique=True)
#     profile_img = Column(String(length=1000), nullable=True)
#     sns_type = Column(Enum("FB", "GG", "KK"), nullable=True)
#     marketing_agree = Column(Boolean, nullable=True, default=True)
#     # keys = relationship("ApiKeys", back_populates="users")