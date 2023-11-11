from models import Base, session, Product, engine

import datetime
import csv
import time

if __name__ == '__main__':
    Base.metadata.create_all(engine)
def menu():
    while True:
        print('''
              \nStore Inventory
              \ra) View Current Inventory
              \rb) Backup database to a file
              \rc) Search for book''')
              
        choice = input('What would you like to do? ')
        if choice in ['a', 'b', 'c']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rEither a, b, or c.
                  \rpress enter to try again.''')
def clean_date(date):
    date_split= date.split('/')
    month = int(date_split[0])
    print(month)
    day = int(date_split[1])
    year = int(date_split[2])

    datetime_val = datetime.datetime(year, month, day)
    return datetime_val
    

def add_csv():
    with open('inventory.csv', newline='') as csvfile:
        next(csvfile, None)
        data = csv.reader(csvfile)
        for row in data:
            inventory_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if inventory_in_db == None:
                product_name = row[0]
                product_price = row[1]
                product_quantity = row[2]
                date_updated = (str(row[3]))
                date_updated = clean_date(date_updated)
                print(date_updated)
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
                session.add(new_product)
        session.commit()
                
