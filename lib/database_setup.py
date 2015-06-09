from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String

Base = declarative_base()
class DBHelper(object):

    @classmethod
    def all(cls):
        return db_session.query(cls().__class__).all()

    @classmethod
    def find(cls, **kwargs):
        self = cls()
        query = db_session.query(self.__class__)
        for key, value in kwargs.iteritems():
            query = query.filter_by(**{key: value})
        return query.all()

    @classmethod
    def findone(cls, **kwargs):
        response = cls.find(**kwargs)
        return response[0] if response else None

    def get(self):
        return db_session.query(self.__class__).get(self.id)

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        return True

    def to_dict(self):
        attributes = [attr for attr in self.__dict__.keys() if attr[0] != "_"]
        return {key: getattr(self, key) for key in attributes}


class User(Base, DBHelper):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True)
    picture = Column(String(250))


class Category(Base, DBHelper):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey("user.id"))


class Item(Base, DBHelper):
    __tablename__ = "item"

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(250))
    picture = Column(String(250))
    category_id = Column(Integer, ForeignKey("category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    category = relationship(Category)


engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

