# database.py
import mysql.connector as MySQL
import random

# mysql = MySQL.connect(
#     host="localhost",
#     user="root",
#     password="Janu@140",
#     database="shopping"
# )
mysql = MySQL.connect(
  host="localhost",
  user="YourFurnitureStore",
  password="yourfurniturestore",
  database="furniture2" 
)

"""
CREATE TABLE cart (
    user_id INT NOT NULL,
    p_id INT NOT NULL,
    quantity INT,
    PRIMARY KEY (user_id, p_id)
);
CREATE TABLE login (
    user_id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, email)
);
CREATE TABLE product (
    p_id INT NOT NULL AUTO_INCREMENT,
    p_name VARCHAR(255) NOT NULL,
    p_type VARCHAR(100),
    manufacturer VARCHAR(255),
    stock VARCHAR(1000),
    price VARCHAR(1000),
    discount VARCHAR(1000),
    url varchar(200),
    PRIMARY KEY (p_id)
);
CREATE TABLE orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    p_id INT,
    quantity INT,
    status VARCHAR(50),
    address VARCHAR(255),
    amount DECIMAL(10,2),
    PRIMARY KEY (order_id),
    FOREIGN KEY (user_id) REFERENCES login(user_id),
    FOREIGN KEY (p_id) REFERENCES product(p_id)
);
CREATE TABLE payment (
    order_id INT NOT NULL,
    payment_status VARCHAR(50),
    transaction_details VARCHAR(255),
    PRIMARY KEY (order_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE registration (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    pin_code VARCHAR(10) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE user (
    user_id INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    contact VARCHAR(20),
    PRIMARY KEY (user_id, email)
);
"""
def calculate_total_amount(cart_items):
        total_amount = 0
        for item in cart_items:
            total_amount += float(item[2]) * item[3]
        return total_amount
    
print(mysql)

class User():
    def __init__(self) -> None:
        pass
    def add_product(p_name, p_type, manufacturer, stock, price, discount, url):

        cur = mysql.cursor()
        sql_query = "INSERT INTO product (p_name, p_type, manufacturer, stock, price, discount, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql_query, (p_name, p_type, manufacturer, stock, price, discount, url))
        mysql.commit()
        cur.close()
        print("Product added successfully:", p_name)  # Debugging message

    def check_existence_user(username):
        cur = mysql.cursor()
        cur.execute("SELECT COUNT(*) FROM login WHERE email=%s", (username,))
        res = cur.fetchone()
        print(res)
        print(type(res))
        cur.close()
        if res == (0,):
            print("User does not exist")  # Debugging message
            return False
        return True

    def check_user_pwd(username, password):
        cur = mysql.cursor()
        cur.execute("SELECT COUNT(*) FROM login WHERE email=%s AND pwd=%s",
                    (username, password))
        res = cur.fetchall()
        print(res)
        print(type(res))

        cur.close()
        if res == [(0,)]:
            print("Invalid user credentials")  # Debugging message
            return False
        return True

    def register_new_user(name, email, address, mobile, pincode, password):
        cur = mysql.cursor()
        cur.execute("INSERT INTO registration (name, email, address, mobile, pin_code, password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (str(name), str(email), str(address), str(mobile), str(pincode), str(password)))
        print("done")
        mysql.commit()
        cur.execute("insert into login (email,pwd) values (%s,%s)",(email,password))
        mysql.commit()
        cur.execute("insert into user (user_id,email,name,address,contact) values ((select user_id from login where email=%s),%s,%s,%s,%s)",(email,email,name,address,mobile))
        mysql.commit()
        cur.close()
        print("Registration successful:", name, email)  # Debugging message

    def get_user_cart_items(userid):
        cur = mysql.cursor()
        cur.execute(f"SELECT c.p_id, p.p_name, p.price, c.quantity FROM cart c JOIN product p ON c.p_id=p.p_id WHERE user_id={userid}")
        res = cur.fetchall()
        cur.close()
        print(res)
        print("Cart retrieval successful:", userid)  # Debugging message
        return res

    def get_user_id(username):
        cur = mysql.cursor()
        cur.execute("SELECT user_id FROM login WHERE email=%s", (username,))
        res = cur.fetchall()
        cur.close()
        print("User ID retrieval successful:", username)
        return res[0][0]
    
    def add_to_cart(user_id, p_id):
        cur = mysql.cursor()
        try:
            # Print debug information
            print("User ID:", user_id)
            print("Product ID:", p_id)

            # Construct and print the SQL query
            sql_query = f"INSERT INTO cart (user_id, p_id, quantity) VALUES ({user_id}, {p_id}, 1)"
            print("SQL Query:", sql_query)

            # Execute the SQL query
            abc = cur.execute(sql_query)

            # Commit the transaction
            mysql.commit()
            
            print("Rows inserted:", abc)

        except mysql.connector.Error as error:
            print("Error:", error)
            # Raise the error for further handling if needed
            raise error

        finally:
            cur.close()
            print("Product added to cart successfully:", p_id)

    def get_user_details(user_id):
        cur = mysql.cursor()
        cur.execute("SELECT name, email, address, contact FROM user WHERE user_id=%s", (user_id,))
        res = cur.fetchone()
        cur.close()
        print("User details retrieval successful:", user_id)  # Debugging message
        return res

    def clear_cart(user_id):
        cur = mysql.cursor()
        cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
        mysql.commit()
        cur.close()
        print("Cart cleared successfully:", user_id)  # Debugging message
    def add_payment(order_id, payment_status, transaction_details):
        cur = mysql.cursor()
        query=f"INSERT INTO payment VALUES ({order_id}, '{payment_status}', '{str(transaction_details)}')"
        print(query)
        cur.execute(query)
        mysql.commit()
        print()
        print("Payment added successfully:", order_id)
        cur.close()
    def get_prod_info(p_id):
        cur = mysql.cursor()
        cur.execute("select p_id,p_name,price from product where p_id= %s ",(p_id,))
        res=cur.fetchall()
        mysql.commit()
        cur.close()
        f=list(res[0])
        # f[3]=
        return f
   
# database.py (continued)

class Admin:
    def remove_product(p_id):
        cur = mysql.cursor()
        cur.execute("DELETE FROM product WHERE p_id=%s and (select count(*) from orders where p_id=%s)=0", (p_id,p_id,))
        print("Product removed successfully:", p_id)
        mysql.commit()
        cur.close()

    def update_product(p_name, p_type, manufacturer, stock, price):
        cur = mysql.cursor()
        cur.execute("UPDATE product SET p_type=%s, manufacturer=%s, stock=%s, price=%s WHERE p_name=%s",
                    (p_type, manufacturer, stock, price, p_name))
        mysql.commit()
        cur.close()
        print("Product updated successfully:", p_name)

    def get_shipped_products():
        cur = mysql.cursor()
        cur.execute("SELECT p.transaction_details, o.p_id, o.user_id, o.address, o.quantity, o.amount, o.status "
                    "FROM orders o JOIN payment p ON o.order_id=p.order_id WHERE o.status='shipped'")
        res = cur.fetchall()
        cur.close()
        print("Retrieval of shipped products successful")
        return res

    def get_unshipped_products():
        cur = mysql.cursor()
        cur.execute("SELECT p.transaction_details, o.p_id, o.user_id, o.address, o.quantity, o.amount, o.status "
                    "FROM orders o JOIN payment p ON o.order_id=p.order_id WHERE o.status='unshipped'")
        res = cur.fetchall()
        cur.close()
        print("Retrieval of unshipped products successful")
        return res
    def update_shipping(lst):
        cur = mysql.cursor()
        cur.execute(f"update orders set status ='shipped' where user_id={lst[0]} and p_id={lst[1]} and quantity={lst[2]} and status='unshipped';")
        cur.close()
        print("Updating of unshipped product was successful")

    def get_returned_products():
        cur = mysql.cursor()
        cur.execute("SELECT p.p_id, p.p_name, o.user_id, o.address, o.quantity, o.amount, o.status "
                    "FROM orders o JOIN product p ON o.p_id=p.p_id WHERE o.status='returned'")
        res = cur.fetchall()
        cur.close()
        print("Retrieval of returned products successful")
        return res
    
    def process_order(user_id, cart_items, user_details):
        cur = mysql.cursor()
        order_id = None
        print("cart_items",cart_items)
        try:
            # Insert order details
            
            order_id = cur.lastrowid

            # Insert order items
            for item in cart_items:
                print(user_id,item[0] , item[3], user_details, calculate_total_amount(cart_items), 'unshipped')
                cur.execute("INSERT INTO orders (user_id,p_id, quantity, address, amount, status) VALUES (%s, %s, %s, %s,%s,%s)",
                        (user_id,item[0] , item[3], user_details[2], calculate_total_amount(cart_items), 'unshipped'))

            # get order id
            print("added to orders")
            cur.execute("SELECT order_id FROM orders WHERE user_id=%s and p_id=%s and quantity=%s and amount=%s", (user_id,item[0] , item[3],calculate_total_amount(cart_items)))
            res=cur.fetchone()
            order_id=res[0]
            print("order_id",order_id)

            mysql.commit()
            cur.close()
            return order_id
        except Exception as e:
            mysql.rollback()
            print("Error processing order:", str(e))
    def process_order_1(user_id, cart_items, user_details):
        cur = mysql.cursor()
        order_id = None
        print("cart_items",cart_items)
        try:
            # Insert order details
            cur.execute("INSERT INTO orders (user_id,p_id, quantity, address, amount, status) VALUES (%s, %s, %s, %s,%s,%s)",
                        (user_id,cart_items[0] ,cart_items[3], user_details[2], float(cart_items[2]), 'unshipped'))

            # get order id
            mysql.commit()
            print("added to orders")
            cur.execute("SELECT order_id FROM orders WHERE user_id=%s and p_id=%s and quantity=%s and amount=%s", (user_id,cart_items[0] , cart_items[3],float(cart_items[2])))
            res=cur.fetchone()
            order_id=res[0]
            print("order_id",order_id)

            mysql.commit()
            cur.close()
            return order_id
        except Exception as e:
            mysql.rollback()
            print("Error processing order:", str(e))
    def get_order_details(order_id):
        cur = mysql.cursor()
        cur.execute("SELECT o.order_id, o.user_id, o.address, o.amount, o.status, p.payment_status, p.transaction_details "
                    "FROM orders o JOIN payment p ON o.order_id=p.order_id WHERE o.order_id=%s", (order_id,))
        res = cur.fetchone()
        cur.close()
        print("Order details retrieval successful:", order_id)
        return res

    def calculate_total_amount(cart_items):
        total_amount = 0
        for item in cart_items:
            total_amount += float(item[2]) * item[3]
        return total_amount
    def get_all_products():
        cur = mysql.cursor()
        cur.execute("select p_id,p_name,p_type,price,stock,url from product") #==========================
        res=cur.fetchall()
        cur.close()
        print("Retrival of products successful")
        return res
    def admin_all_prod():
        cur = mysql.cursor()
        cur.execute("select p_id,p_name,price,url from product")
        res=cur.fetchall()
        cur.close()
        print("Retrival of products successful")
        return res