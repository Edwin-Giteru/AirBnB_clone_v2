#!/usr/bin/python3

import os
from models.base_model import Base, BaseModel
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_user = os.getenv('HBNB_MYSQL_USER')
db_pwd = os.getenv('HBNB_MYSQL_PWD')
db_host = os.getenv('HBNB_MYSQL_HOST','localhost')
db_name = os.getenv('HBNB_MYSQL_DB')

class DBstorage:

    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(db_user, db_pwd, db_host, db_name), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

        SessionLocal = sessionmaker(autocommmit=False, autoflush=False, bind=self.__engine)
        self.__session = SessionLocal()

    def all(self,cls=None):
        ''' Query all objects depending on the class name'''

        objects_dict = {}

        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
        else:
            classes = [cls]

        for a_class in classes:
            instances = self.__session.query(a_class).all()

            for obj in instances:
                key ='{}.{}'.format(a_class.__name__, obj.id)
                objects_dict[key] = obj

            return objects_dict

    def new(self, obj):

        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
    def reload(self):

        """create tables in the database"""
        Base.metadata.create_all(self.__engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

        self.__session = SessionLocal()
    def close(self):
        self.__session.remove()
