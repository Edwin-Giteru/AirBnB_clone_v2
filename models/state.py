#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable= False)
    cities = relationship("City", back_populates="states",cascade="all, delete-orphan")
    
    @property
    def cities(self):
        """Returns list of City instances with state_id == current State.id
        """

        from models import storage
        all_cities = storage.all(City).values()
        return [city for city in all_cities if city.state_id ==self.id]
