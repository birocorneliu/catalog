import os
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, desc
from lib import exceptions

Base = declarative_base()
class DBHelper(object):
    PATH = "static/uploaded/{}_{}"
    IMAGE_PATH = "{}/{}".format(os.path.realpath('.'), PATH)

    @classmethod
    def all(cls, limit=None):
        self = cls()
        if limit is None:
            return db_session.query(self.__class__).all()
        else:
            return db_session.query(self.__class__
                    ).order_by(desc("id")).all()[:limit]

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
        if not response:
            raise exceptions.EntityNotFound(cls().__class__.__name__)
        return response[0]

    def get(self):
        response = db_session.query(self.__class__).get(self.id)
        if not response:
            raise exceptions.EntityNotFound(self.__class__.__name__)
        return response

    def create(self):
        db_session.add(self)
        db_session.commit()
        return self

    def save(self):
        return self.create()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        return True

    def to_dict(self):
        attributes = [attr for attr in self.__dict__.keys() if attr[0] != "_"]
        return {key: getattr(self, key) for key in attributes}

    def add_picture(self, request):
        file_obj = request.files.get("pic")
        if file_obj:
            if not self.id:
                self = self.save()
            path = self.IMAGE_PATH.format(self.id, file_obj.filename)
            file_obj.save(path)
            self.picture = self.PATH.format(self.id, file_obj.filename)
            self.save()



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

    def to_full_dict(self):
        attributes = [attr for attr in self.__dict__.keys() if attr[0] != "_"]
        response = {key: getattr(self, key) for key in attributes}
        response["category"] = self.category.to_dict()
        return response

engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

