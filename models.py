from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
     __tablename__ = "products"

     product_id = Column("product_id", Integer, primary_key=True)
     product_name = Column("product_name", String)
     product_quantity = Column("product_quantity", Integer)
     product_price = Column("product_price", Integer)
     date_updated = Column("date_updated", Date)

     def __repr__(self):
         return f'{product_id}, {self.product_name}, {self.product_quantity}, {self.product_price}, {self.date_updated}'