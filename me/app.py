
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Janu@140"
app.config['MYSQL_DB'] = "furniture"

mysql = MySQL(app)

@app.route('/')
def web():
    return render_template('index.html')
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pswd = request.form['password']
        name = request.form['fullname']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['zip']
        con = request.form['country']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registration (username,email,password_hash,full_name,address,city,state,pincode,country,phone_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (username, email, pswd, name, address, city, state, pincode, con, phone))
        mysql.connection.commit()
        cur.close()

        return "registered successfully"

    return render_template('register.html')



if __name__ == "__main__":
    app.run(debug=True)

