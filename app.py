# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session,flash
from database_ import Admin, User
import base64
import requests
import time
from werkzeug.datastructures import ImmutableMultiDict
import selenium
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Dummy admin credentials
ADMIN_USERNAME = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin' 


@app.route("/")
def mainpage():
    return render_template('main.html')

@app.route('/home')
def home():
    # Check if the user is logged in
    if 'user_id' in session:
        # Render the home page with the "Logout" and "Profile" links
        return render_template('home.html')
    else:
        # Render the home page with the "Sign Up" and "Sign In" links
        return render_template('home.html')
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

        # print(name, email, address, mobile, pincode, password)
        # Simple form validation, you can enhance this as per your requirements
        if not name or not email or not address or not mobile or not pincode or not password:
            return jsonify({'error': 'Please fill in all fields.'}), 400

        try:
            User.register_new_user(name, email, address, mobile, pincode, password)
        except Exception as e:
            print("Error during registration:", str(e))  # Debugging message
            return jsonify({'error': 'Registration failed. Error: {}'.format(str(e))}), 500

        # Return a success message or redirect to another page after registration
        return redirect(url_for('login'))  # Redirect to the login page after successful registration

    # Handle GET requests to the /register route
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        userid_glob = User.get_user_id(username)
    except Exception as e:
        print("Error getting user id:", str(e))
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD and request.form.get('usertype') == 'admin':
        return jsonify({'redirect': url_for('admin_home')})
    elif User.check_existence_user(username) and request.form.get('usertype') == 'customer':
        if User.check_user_pwd(username, password):
            session['user_id'] = User.get_user_id(username)
            print(session['user_id'])
            return jsonify({'redirect': url_for('home')})
        return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# ================================================================== #

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
            Admin.add_product(p_name, p_type, manufacturer, stock, price, discount, picture_url)
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
        p_name = request.form.get('name')
        p_type = request.form.get('type')
        manufacturer = request.form.get('info')
        stock = request.form.get('quantity')
        price = request.form.get('price')
        Admin.update_product(p_name, p_type, manufacturer, stock, price)
        return redirect(url_for('admin_home'))  # Redirect back to admin home page after update
    elif request.method == 'GET':
        p_name=request.args.get('name')
        print("Product name to update:", p_name)
        if p_name is None:
            return redirect(url_for('admin_view_product'))
        #fill the form with the product details
        # request.form = ImmutableMultiDict([('name', p_name), ('type', ''), ('info', ''), ('quantity', ''), ('price', '')])
        #render the update product page with the product details
        return render_template('update_product.html')#, values=[p_name])
    else:
        # Render the update product page (GET request)
        return render_template('update_product.html')  # Assuming you have an update_product.html template

# ================================================================== #

@app.route('/view_products')
def view_product():
    all_products = Admin.get_all_products()
    # print(all_products)
    return render_template('view_products.html', values=all_products, val_len=len(all_products))

# ================================================================== #

@app.route('/order_details')
def order_details():
    # Only allow admin access to this route
    if 'user_id' in session:
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('login'))

# ================================================================== #

@app.route('/cart_details')
def cart_details():
    # Render the cart_details.html template
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        user_id = session['user_id']
        cart_of_user = User.get_user_cart_items(user_id)
        cart_items_final=[]
        for i in cart_of_user:
            i=list(i)
            i[2]=float(i[2])
            cart_items_final.append(i)
    return render_template('cart_details.html', values=cart_items_final)

# ================================================================== #

@app.route('/get_cart_items', methods=['GET'])
def get_cart_items():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    cart_items = User.get_user_cart_items(user_id)

    print(cart_items)
    return jsonify(cart_items)

# ================================================================== #

@app.route('/stock')
def stock():
    return render_template('stock.html')

# ================================================================== #

@app.route('/shipped')
def shipped_page():
    shipped = Admin.get_shipped_products()
    return render_template('shipped.html', values=shipped, val_len=len(shipped))

# ================================================================== #


@app.route('/unshipped')
def unshipped():
    unshipped = Admin.get_unshipped_products()
    # print(unshipped)
    return render_template('unshipped.html', values=unshipped, val_len=len(unshipped))
@app.route("/shipping",methods=['GET'])
def update_to_ship():
    if request.method=='GET':
        lst=list(eval(request.args.get('val')))
        print(lst)
        Admin.update_shipping(lst)
        return redirect(url_for('unshipped'))
    
# ================================================================== #

@app.route('/returned_products')
def returned_products_page():
    returned_products = Admin.get_returned_products()
    return render_template('returned_products.html', values=returned_products, val_len=len(returned_products))

# ================================================================== #

@app.route("/remove_products", methods=['GET', 'POST'])
def rem_prod():
    if request.method == 'POST':
        p_id = request.form.get('prodid')
        print("To remove:",p_id)
        Admin.remove_product(p_id)
    if request.method == 'GET':
        product_id = request.args.get('id')
        if product_id is None:
            return render_template('remove_products.html')
        print("Product ID to remove:", product_id)
        try:
            Admin.remove_product(product_id)
            # #display message that producrt is removed
            # flash("Product removed successfully")
            # return redirect(url_for('admin_view_product'))
            return redirect(url_for('admin_view_product', message=f'Product removed successfully:{product_id}'))
        except Exception as e:
            print("Error removing product:", str(e))
            return jsonify({'error': 'Error removing product. {}'.format(str(e))}), 500
    return render_template('remove_products.html')



# ================================================================== #


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart_via_page():
    product_id = request.json['product_id']
    print(product_id)
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']

    try:
        # Assuming User.add_to_cart method handles the addition to the cart
        User.add_to_cart(user_id, product_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ================================================================== #


@app.route('/check_out')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        # if request.method == 'POST':
            # Retrieve cart items and user details
        user_id = session['user_id']
        cart_items = User.get_user_cart_items(user_id)
        user_details = User.get_user_details(user_id)

        # Process the order and payment
        order_id = Admin.process_order(user_id, cart_items, user_details)
        print(order_id)
        session['order_id']=order_id
        print(session['order_id'])
        # # # Clear the cart after successful order
        if order_id!=None:
            User.clear_cart(user_id)
        else:
            return jsonify({"Error": "Checkout failed, Try again:"}),500

        return render_template('select_payment.html')
    except:
        # Handle GET request (if needed)
        return jsonify({"Error": "Checkout failed, Try again:"}),500

# ================================================================== #

@app.route('/logout')  # Changed the route path to '/user_logout'
def logout():  # Renamed the function to 'user_logout'
    session.pop('user_id', None)
    return redirect(url_for('home'))

# ================================================================== #

@app.route('/admin_logout')  # Route path for admin logout
def admin_logout():  # Function for admin logout
    session.pop('admin_id', None)  # Assuming 'admin_id' is the key for admin session
    # Redirect to home or wherever you want to redirect after admin logout
    return redirect(url_for('login'))

# ================================================================== #

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    if 'user_id' in session:
        user_id = session['user_id']
        user_details = User.get_user_details(user_id)
        if user_details:
            user_data = {
                'name': user_details[0],
                'email': user_details[1],
                'address': user_details[2],
                'mobile': user_details[3],
                'pinCode': user_details[4]
            }
            return jsonify(user_data)
    return jsonify({'error': 'User not logged in'}), 401

# ================================================================== #

@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        user_details = User.get_user_details(user_id)
        print(user_details)
        return render_template('profile.html', values=user_details)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))

# ================================================================== #
@app.route('/admin_view_product')
def admin_view_product():
    all_products = Admin.admin_all_prod()
    # print(all_products)
    final_prods=[]
    for i in all_products:
        i=list(i)
        i[2]=float(i[2])
        # i[3]='https://www.decorsouth.com/thumbs/150x125/images/framed-chair-batik-pearl-black-1.jpg'
        final_prods.append(i)
    print(final_prods)
    return render_template('admin_view_product.html', values=final_prods)


# ================================================================== #
@app.route('/payment_credit')
def view_pay_credit():
    return render_template("payment_credit.html")


@app.route('/payment_credit',methods=['POST'])
def pay_credit():
    # try:
    if request.method == 'POST':
        card_num = request.form.get('cardnumber')
        card_name = request.form.get('cardholder')
        # cvv = request.form.get('cvv')0
        expiry = request.form.get('expyear')
        print(card_num, card_name, expiry)
        User.add_payment(transaction_details="Credit card txn "+str(card_num)[:5]+'xxx'+' '+card_name+' on '+time.strftime('%Y-%m-%d %H:%M:%S'),order_id=session['order_id'], payment_status='successful')

        return render_template("payment_credit.html")
    # except:
    #     return render_template("payment_credit.html")

# ================================================================== #
@app.route('/payment')
def payment():
    return render_template('select_payment.html')
@app.route('/payment_debit')
def view_pay_debit():
    return render_template("payment_debit.html")

@app.route('/payment_debit',methods=['POST'])
def pay_debit():
    if request.method == 'POST':
        card_num = request.form.get('cardnumber')
        card_name = request.form.get('cardholder')
        expiry = request.form.get('expyear')
        print(card_num, card_name, expiry)
        User.add_payment(transaction_details="Debit card txn "+str(card_num)[:5]+'xxx'+' '+card_name+' on '+time.strftime('%Y-%m-%d %H:%M:%S'),order_id=session['order_id'], payment_status='successful')

        return render_template("payment_debit.html")
    
# ================================================================== #
@app.route('/check_out_selected_item', methods=['GET','POST'])
def checkout_selected_item():
    if  request.method=='POST':
        if 'user_id' not in session:
            return redirect(url_for('login'))
        try:
            user_id = session['user_id']
            # Retrieve selected product details from the form submission
            p_id = request.form.get('product_id')
            # You can also retrieve other details of the product if needed
            p_name = request.form.get('product_name')
            p_price = request.form.get('product_price')
            user_details=User.get_user_details(user_id)
            print(p_id, p_name, p_price, user_details)
            # Process the order for the selected item
            order_id = Admin.process_order_1(user_id, [(p_id, p_name, p_price, 1)],user_details)

            if order_id:
                # Clear the cart after successful order
                User.clear_cart(user_id)
                # Set the order ID in the session for future reference
                session['order_id'] = order_id
                return redirect(url_for('payment'))
            else:
                return jsonify({"Error": "Checkout failed, try again."}), 500
        except Exception as e:
            print("Error during checkout:", str(e))
            return jsonify({"Error": "Checkout failed, try again."}), 500
    if request.method=='GET':
        p_id=request.args.get('productID')
        print(p_id)
        p_info=User.get_prod_info(p_id)
        p_info.append(1)
        user_id = session['user_id']
        user_details=User.get_user_details(user_id)
        order_id=Admin.process_order_1(user_id,p_info,user_details)
        if order_id:
                # Set the order ID in the session for future reference
                session['order_id'] = order_id
                return redirect(url_for('payment'))
                return render_template('select_payment.html')
        else:
            return jsonify({"Error": "Checkout failed, try again."}), 500
# ================================================================== #
@app.route('/payment_upi')
def view_pay_upi():
    return render_template("payment_upi.html")

@app.route('/payment_upi',methods=['POST'])
def pay_upi():
    if request.method == 'POST':
        upi_id = request.form.get('upiId')
        print(upi_id)
        User.add_payment(transaction_details="UPI txn "+str(upi_id)[:2]+'xxx'+' on '+time.strftime('%Y-%m-%d %H:%M:%S'),order_id=session['order_id'], payment_status='successful')
    return render_template("payment_upi.html")




if __name__ == '__main__':
    app.run(debug=True)