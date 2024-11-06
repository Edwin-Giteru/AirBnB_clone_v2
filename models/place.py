#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)



class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60),ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60),ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable= False)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []
    reviews = relationship('Review', backref='places',cascade ='all, delete, delete-orphan')
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,    
        back_populates="place_amenities")

    @property
    def reviews(self):
        from models import storage
        all_review = storage.all("Review").values()
        return [review for review in all_review if review.place_id == self.id]
    @property
    def amenities(self):
        """Returns the list of Amenity instances linked to this Place."""
        from models import storage
        return [amenity for amenity in storage.all(Amenity).values() if amenity.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, amenity):
        """Adds Amenity ID to amenity_ids if amenity is an Amenity instance."""
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
