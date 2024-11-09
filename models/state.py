#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models
from models.engine.file_storage import FileStorage as F

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable= False)
    cities = relationship('City', backref='states')

    if models.storage_type != "db":
        @property
        def cities(self):
            """get the list of City instances of the same state"""
            for city in F.all('City').values():
                city_list = []
                if city.state_id == self.State.id:
                    city_list.append(city)

            return city_list
    if models.storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""
