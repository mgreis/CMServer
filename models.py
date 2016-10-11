"""from sqlalchemy import Column, Integer, String, Float"""
from sqlalchemy.orm import relationship
from sqlalchemy import *
from database import Base




class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(200))
    product_price = Column(Float)
    product_qty = Column (Integer)

    def __init__(self, product_name=None, product_price=None, product_qty = None):
        self.product_name = product_name
        self.product_price = product_price
        self.product_qty = product_qty



    def __repr__(self):
        return "{\"product_id\" : \"%s\", \"product_name\" : \"%s\", \"product_price\" : \"%s\", \"product_qty\" : \"%s\"}" % (
        self.product_id,
        self.product_name,
        self.product_price,
        self.product_qty)







