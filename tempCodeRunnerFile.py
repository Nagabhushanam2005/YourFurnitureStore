@app.route("/check_out",methods=['POST'])
def check_out():
    if user_id_glob == -1:
        # If no user is logged in, redirect to the login page
        return redirect(url_for('index'))

    if request.method == 'POST':
        
        p_id = request.form.get('product_id')

        
        User.add_to_cart(user_id_glob, p_id)

       
        return redirect(url_for('products'))

    # Handle GET request (if needed)
    return render_template('products.html')