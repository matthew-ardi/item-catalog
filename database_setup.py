#!/usr/bin/env python

import sys

from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Categories(Base):
    # Representation of the table inside the database
    __tablename__ = 'categories'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

	 # serializable format
    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id
        }

class Categories_item(Base):
    # Representation of the table inside the database
    __tablename__ = 'categories_item'

    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(10000), nullable = False)
    picture = Column(LargeBinary)
    categories_item_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)


# serializable format
    @property
    def serialize(self):
        return {
            'name': self.categories.name,
            'cat_id' : self.categories.id,
            'Items':{
                'id': self.id,
                'title': self.title,
                'description': self.description
            }
        }

    @property
    def serialize_items(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }


########### insert at the end of file ##########
engine = create_engine('sqlite:///catalog_items.db')

Base.metadata.create_all(engine)
