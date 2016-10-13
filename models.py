"""from sqlalchemy import Column, Integer, String, Float"""
from sqlalchemy.orm import relationship
from sqlalchemy import *
from database import Base

class User (Base):
    __tablename_ = 'user'

    user_id = Column(Integer, primary_key=true)
    user_email = Column(String(200))
    user_password = Column(String(200))
    user_products = relationship('Product')

    def __init__(self,user_email= None, user_password= None):
        self.user_email = user_email,
        self.user_password = user_password

    def __repr__(self):
        return "{\"user_id\" : \"%s\" , \"user_email\" : \"%s\"}" %(
        self.user_id,
        self.user_email)



class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(200))
    product_price = Column(Float)
    product_qty = Column (Integer)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='cascade'))

    def __init__(self, product_name=None, product_price=None, product_qty = None, user_id = None):
        self.product_name = product_name
        self.product_price = product_price
        self.product_qty = product_qty
        self.user_id = user_id


    def __repr__(self):
        return "{\"product_id\" : \"%s\", \"product_name\" : \"%s\", \"product_price\" : \"%s\", \"product_qty\" : \"%s\" , \"user_id\" : \"%s\"}" % (
        self.product_id,
        self.product_name,
        self.product_price,
        self.product_qty,
        self.user_id)







