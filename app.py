from models import Base, session, Product, engine

import datetime
import csv
import time

####main menu
def menu():
    while True:
        print('''
              \nStore Inventory
              \rv) View Details of Product
              \ra) Add New Product
              \rb) Backup the Database
              \re) Exit program''')
              
        choice = input('What would you like to do? ')
        if choice in ['a', 'b', 'v', 'e']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rEither a, b, c, or e.
                  \rpress enter to try again.''')
            
#### Convert date to a date time            
def clean_date(date):
    try:
        date_split= date.split('/')
        month = int(date_split[0])
        day = int(date_split[1])
        year = int(date_split[2])
        datetime_val = datetime.datetime(year, month, day)
    except ValueError:
        input('''
              \n****** DATE ERROR ******
              \rThe date format should include a valid Month Day Year from the past.
              \rEx: 11/12/2022
              \r Press enter to try again.
              \r**************************''')
    else:
        return datetime_val
    
#### Clean price to be in cents
def clean_price(price):
    new_price = ""
    try:
        for character in price:
            if character == "$":
                continue
            else:
                new_price += character
        new_price = 100 * (float(new_price))
    except ValueError:
        input('''
              \n****** CURRENCY ERROR ******
              \rThe format should be a dollar amount
              \rEx: $7.11
              \r Press enter to try again.
              \r**************************''')
    else:
        return int(new_price)

#### Add csv data to database,
#### only add entries that have not been added yet
def add_csv():
    with open('inventory.csv', newline='') as csvfile:
####    Skip first line containing field headers
        next(csvfile, None)
####    Add remaining products from 2nd row    
        data = csv.reader(csvfile)
        for row in data:
            inventory_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if inventory_in_db == None:
                product_name = row[0]
                product_price = (str(row[1]))
                product_price = clean_price(product_price)
                product_quantity = row[2]
                date_updated = (str(row[3]))
                date_updated = clean_date(date_updated)
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
                session.add(new_product)
        session.commit()

#### Create backup of database in csv format      
def backup_csv():
    backup_data = []
    for product in session.query(Product):
        current_product = []
        current_product.append(product.product_name)
        current_product.append(product.product_price)
        current_product.append(product.product_quantity)
        current_product.append(product.date_updated)
        backup_data.append(current_product)
    with open('backup.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["Product Name | Price | Quantity | Date Updated"])
        for row in backup_data:
            writer.writerow(row)
    input("""
          *****************************************
          ******        BACKUP MADE!         ******
          *        Press enter to continue.       *
          *****************************************""")

#### confirm the user selects an id
def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
              \n****** ID ERROR ******
              \rThe ID should be NUMBER
              \r Press enter to try again.
              \r**************************''')
        return
    else:
        if product_id in options:
          return product_id
        else:
            input("""
            |******* AVAILABLE ID OPTIONS******|
            |----------------------------------|    
            |Options: {options}                | 
            |__________________________________|
            |**********************************|""")

def clean_quantity(quantity):
    try:
        return_quantity = int(quantity)
    except ValueError:
        input('''
            \n****** QUANTITY ERROR ******
            \rPlease enter a number ex(1, 2, 41, 20)
            \r Press enter to try again.
            \r**************************''')
    else:
        return return_quantity
#### Run main application
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "a":
            product_name = input("Product Name: ")
            price_error = True
            while price_error:
                price = input("Price (Ex: $2.99): ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                quantity = input("Quantity: ")
                quantity = clean_quantity(quantity)
                if type(quantity) == int:
                    quantity_error = False
            date_error = True
            while date_error:
                date = input("Date Updated (Ex: 11/1/2023): ")
                date = clean_date(date)
                if type(date) == datetime.datetime:
                    date_error = False
            new_product = Product(product_name=product_name, product_price=price, product_quantity=quantity, date_updated=date)
            session.add(new_product)
            session.commit()
            print("""
                     |********************************|
                     |        Product Added!          |
                     |********************************|""")
            time.sleep(1.5)
        elif choice == "b":
            backup_csv()
        elif choice == "v":
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                 id_choice = input(f"""
                    **************************************
                    **************************************
                    * ID Options: {id_options}           *
                    * Product id:   """)
                  
                 id_choice = clean_id(id_choice, id_options)
                 if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id==id_choice).first()
            print(f"""
             ************************************************ 
             *          {the_product.product_name}          * 
             ************************************************     
             *     Price: ${the_product.product_price / 100}*
             *     Quantity: {the_product.product_quantity} *
             *     Date Updated: {the_product.date_updated} *
             ************************************************
             ************************************************""")
            time.sleep(3.5)
        elif choice == "e":
            print("""
     *******************************
     *******************************
     *           Goodbye!          * 
     *******************************
     *******************************""")
            time.sleep(1.5)
            app_running = False
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
            



            
        

      
        