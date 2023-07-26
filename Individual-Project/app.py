from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={ 
    "apiKey": "AIzaSyAC6nvd3oGJWIxUTv7_mo3uB7tA7i_tarY",
    "authDomain": "project-1fe47.firebaseapp.com",
    "projectId": "project-1fe47",
    "storageBucket": "project-1fe47.appspot.com",
    "messagingSenderId": "346344684791",
    "appId": "1:346344684791:web:b204ca31ddf98e16b9a7f2",
    "measurementId": "G-E07168PH09",
    "databaseURL":"https://project-1fe47-default-rtdb.europe-west1.firebasedatabase.app/"
}


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

#Code goes below here
@app.route('/')
def hello_world():
   return render_template("home.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            flash("You have successfully signed in!", "success")
            return redirect(url_for('hello_world'))
        except Exception as e:
            error = "Authentication failed: " + str(e)
            flash(error, "error")
    return render_template("signin.html", error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            login_session['user'] = user
            UID = login_session['user']['localId']
            user_data = {"username": username, "email": email, "password": password, "full_name": full_name}
            db.child("Users").child(UID).set(user_data)
            flash("You have successfully signed up!", "success")
            return redirect(url_for('hello_world'))
        except Exception as e:
            error = "Authentication failed: " + str(e)
            flash(error, "error")
    return render_template("signup.html", error=error)

@app.route('/rings', methods=['GET', 'POST'])
def rings():
    if request.method=='POST':
        product_data = {
            'image': request.form.get('image'),
            'price': request.form.get('price'),
            }
        try:
            UID = login_session['user']['localId']
            db.child("Users").child(UID).child('Products').push(product_data)
        except Exception as e:
            print(e)

    return render_template("rings.html")


@app.route('/necklaces', methods=['GET','POST'])
def necklaces():
    if request.method=='POST':
        product_data = {
            'image': request.form.get('image'),
            'price': request.form.get('price'),
            }
        try:
            UID = login_session['user']['localId']
            db.child("Users").child(UID).child('Products').push(product_data)
        except Exception as e:
            print(e)
    return render_template("necklaces.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin')
        )


@app.route('/cart')
def cart():
    if not login_session['user']:
        return redirect(url_for('signin'))
    uid = login_session['user']['localId']
    items = db.child("Users").child(uid).child("Products").get().val()
    return render_template("cart.html", items=items)

if __name__ == '__main__':
    app.run(debug=True)