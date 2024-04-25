
import mysql.connector as MySQL
# GRANT ALL PRIVILEGES ON *.* TO 'YourFurnitureStore'@'localhost' WITH GRANT OPTION;


# mysql = MySQL.connect(
#   host="localhost",
#   user="root",
#   password="Janu@140",
#   database="shopping"
# )
mysql = MySQL.connect(
  host="localhost",
  user="YourFurnitureStore",
  password="yourfurniturestore",
  database="furniture"
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
CREATE TABLE product (
    p_id INT NOT NULL AUTO_INCREMENT,
    p_name VARCHAR(255) NOT NULL,
    p_type VARCHAR(100),
    manufacturer VARCHAR(255),
    stock VARCHAR(1000),
    price VARCHAR(1000),
    discount VARCHAR(1000),
    PRIMARY KEY (p_id)
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


print(mysql)

class User():
    def __init__(self) -> None:
        pass
    def check_existence_user(username):
        cur = mysql.cursor()
        cur.execute("select count(*) from login where email=%s",(username,))
        res=cur.fetchone()
        print(res)
        print(type(res))
        cur.close()
        if res==[(0,)]:
            print("user DNE")  # Debugging message
            return False
        return True
    def check_user_pwd(username,password):
        cur = mysql.cursor()
        cur.execute("select count(*) from login where email=%s and pwd=%s",
                    (username,password))
        res=cur.fetchall()
        print(res)
        print(type(res))

        cur.close()
        if res==[(0,)]:
            print("user cred status:false")  # Debugging message
            return False
        return True

    def register_new_user(name, email, address, mobile, pincode, password):
        cur = mysql.cursor()
        cur.execute("INSERT INTO registration (name, email, address, mobile, pin_code, password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, email, address, mobile, pincode, password))
        # mysql.connection.commit()
        cur.close()
        print("Registration successful:", name, email)  # Debugging message

    def get_user_cart_items(userid):
        cur = mysql.cursor()
        cur.execute("select c.p_id, p.p_name,p.price,c.quantity from cart c join product p on c.p_id=p.p_id where user_id=%s",(userid,))
        res=cur.fetchall()
        cur.close()
        print("Retrival of cart successful:", userid)  # Debugging message  
        return res
    def get_user_id(username):
        cur = mysql.cursor()
        cur.execute("select user_id from login where email=%s",(username,))
        res=cur.fetchall()
        cur.close()
        print("Retrival of user_id successful:", username)
        return res[0][0]
    def add_to_cart(user_id, p_id):
        cur = mysql.cursor()
        cur.execute("INSERT INTO cart (user_id, p_id, quantity) VALUES (%s, %s, %s)",
                    (user_id, p_id, 1))  # Assuming quantity is set to 1 by default
        mysql.commit()
        cur.close()
        print("Product added to cart successfully:", p_id)  # Debugging message

class Admin():
    def __init__(self) -> None:
        pass
    def add_product(p_name, p_type, manufacturer, stock, price, discount, picture_base64):

        cur = mysql.cursor()
        sql_query = "INSERT INTO product (p_name, p_type, manufacturer, stock, price, discount, picture) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql_query, (p_name, p_type, manufacturer, stock, price, discount, picture_base64))
        cur.close()
        print("Product added successfully:", p_name)  # Debugging message

    def get_all_products():
        cur = mysql.cursor()
        cur.execute("select p_id,p_name,p_type,price,stock from product") #==========================
        res=cur.fetchall()
        cur.close()
        print("Retrival of products successful")
        return res
    
    def remove_product(p_id):
        cur = mysql.cursor()
        cur.execute("delete from product where p_id=%s",(p_id,))
        cur.close()
        print("Product removed successfully:", p_id)
        
    def update_product(p_name, p_type, manufacturer, stock, price ):
        cur = mysql.cursor()
        cur.execute("update product set p_type=%s,manufacturer=%s,stock=%s,price=%s where p_name=%s",
                    (p_type, manufacturer, stock, price,p_name))
        cur.close()
        print("Product updated successfully:", p_name)
    def get_shipped_products():
        # get transaction id, p_id,username,address,quantity,amount,status
        cur = mysql.cursor()
        cur.execute("select p.transaction_details,o.p_id,o.user_id,o.address,o.quantity,o.amount,o.status from orders o join payment p on o.order_id=p.order_id where o.status='shipped'")
        res=cur.fetchall()
        cur.close()
        print("Retrival of shipped products successful")
        return res
    
    





