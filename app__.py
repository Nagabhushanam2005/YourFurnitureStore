from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Admin, User
import base64
import requests

app = Flask(__name__)
# maintain current user id 
try:
    file=open("user_id.txt","r")
except:
    file=open("user_id.txt","w")
    file.write("-1")
    file=open("user_id.txt","r")
user_id_glob=int(file.read())
print(user_id_glob)
# Dummy admin credentials
ADMIN_USERNAME = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin'

# Dummy customer credentials
CUSTOMER_USERNAME = 'customer@gmail.com'
CUSTOMER_PASSWORD = 'customer'

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        mobile = request.form.get('mobile')
        pincode = request.form.get('pincode')
        password = request.form.get('password')

        # Simple form validation, you can enhance this as per your requirements
        if not name or not email or not address or not mobile or not pincode or not password:
            return jsonify({'error': 'Please fill in all fields.'}), 400

        try:
            User.register_new_user(name, email, address, mobile, pincode, password)
        except Exception as e:
            print("Error during registration:", str(e))  # Debugging message
            return jsonify({'error': 'Registration failed. Error: {}'.format(str(e))}), 500

        # Return a success message or redirect to another page after registration
        return jsonify({'message': 'Registration successful.'}), 200

    # Handle GET requests to the /register route
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        userid_glob=User.get_user_id(username)
    except Exception as e:
        print("Error getting user id:", str(e))
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD and request.form.get('usertype')=='admin':
        return jsonify({'redirect': url_for('admin_home')})
    elif User.check_existence_user(username) and request.form.get('usertype')=='customer':
        if User.check_user_pwd(username,password):
            user_id_glob=User.get_user_id(username)
            file=open("user_id.txt","w")
            file.write(str(user_id_glob))
            print(user_id_glob)
            return jsonify({'redirect': url_for('home')})
        return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# ================================================================== #
    


@app.route('/')
def home():
    # Render the home page template for customers
    return render_template('home.html')

# ================================================================== #
    


@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

# ================================================================== #
    


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        p_name = request.form.get('p_name')
        p_type = request.form.get('p_type')
        manufacturer = request.form.get('manufacturer')
        stock = request.form.get('stock')
        price = request.form.get('price')
        discount = request.form.get('discount')
        picture_url = request.form.get('picture_url')

        try:
            # Fetch image from URL and convert to base64
            picture_response = requests.get(picture_url)
            if picture_response.status_code != 200:
                return jsonify({'error': 'Failed to fetch image from URL.'}), 500

            picture_base64 = base64.b64encode(picture_response.content).decode('utf-8')

            Admin.add_product(p_name, p_type, manufacturer, stock, price, discount, picture_base64)
            return jsonify({'message': 'Product added successfully.'}), 200
        except Exception as e:
            print("Error adding product:", str(e))  # Debugging message
            return jsonify({'error': 'Error adding product. {}'.format(str(e))}), 500

    return render_template('add_product.html')

# ================================================================== #
    

@app.route('/update_product', methods=['GET', 'POST'])  
def update_product():
    # Handle POST request to update products (form submission)
    if request.method == 'POST':
        # Perform update action here
        # Assuming you have a form with fields for product name, type, manufacturer, stock, price
        p_name = request.form.get('prodName')
        p_type = request.form.get('productType')
        manufacturer = request.form.get('prodDescription')
        stock = request.form.get('prodQuantity')
        price = request.form.get('prodPrice')
        Admin.update_product(p_name, p_type, manufacturer, stock, price)
        return redirect(url_for('admin_home'))  # Redirect back to admin home page after update
    else:
        # Render the update product page (GET request)
        return render_template('update_product.html')  # Assuming you have an update_product.html template


# ================================================================== #
    

@app.route('/view_products') 
def view_product():
    all_products=Admin.get_all_products()
    # print(all_products)
    return render_template('view_products.html', values=all_products,val_len=len(all_products))


# ================================================================== #
    

@app.route('/order_details') 
def order_details():
    # Only allow admin access to this route
    return redirect(url_for('admin_home'))

# ================================================================== #
    



@app.route('/cart_details')
def cart_details():
    # Render the cart_details.html template
    if user_id_glob==-1:
        return render_template('login.html')
    else:
        cart_of_user=User.get_user_cart_items(user_id_glob)
    return render_template('cart_details.html',values=cart_of_user)


# ================================================================== #
    

@app.route('/profile')
def profile():
    # Render the profile page template
    return render_template('profile.html')


# ================================================================== #
    

@app.route('/stock') 
def stock():
    return render_template('stock.html')

# ================================================================== #
    

@app.route('/shipped') 
def shipped_page():
    shipped=Admin.get_shipped_products()

    return render_template('shipped.html',values=shipped,val_len=len(shipped))

# ================================================================== #
    

@app.route('/unshipped')  
def unshipped_page():
    return render_template('unshipped.html')

# ================================================================== #
    

@app.route('/returned_products')  
def returned_products_page():
    return render_template('returned_products.html')

# ================================================================== #
    
@app.route("/remove_products")
def rem_prod():
    if request.method=='POST':
        p_id=request.form.get('productId')
        Admin.remove_product(p_id)
    return render_template('remove_products.html')


@app.route('/check_out',methods=['POST'])
def check_out():
    if user_id_glob == -1:
        # If no user is logged in, redirect to the login page
        return redirect(url_for('login'))

    if request.method == 'POST':
        
        p_id = request.form.get('product_id')

        
        User.add_to_cart(user_id_glob, p_id)

       
        return redirect(url_for('cart_details'))
    # return render_template('products.html')
    # Handle GET request (if needed)
    return render_template('view_products.html')
    

if __name__ == '__main__':
    app.run(debug=True)
