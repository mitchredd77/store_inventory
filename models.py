from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///inventory.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
     __tablename__ = 'inventory'

     product_id = Column(Integer, primary_key=True)
     product_name = Column('Product Name', String)
     
     product_quantity = Column('Quantity', Integer)
     product_price = Column('Price', Integer)
     date_updated = Column('Last Update', Date)

     def __repr__(self):
         return f'Store Inventory: {self.product_name}, Quantity: {self.product_quantity}, Price: {self.product_price}, Last Update: {self.date_updated}'