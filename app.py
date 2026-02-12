
from flask import Flask, render_template, request, redirect, session
from models import db, User, Product, Order
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/images'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template("signup.html")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(f"/{user.role}")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------- Vendor ----------
# ---------------- VENDOR DASHBOARD ---------------- #

@app.route('/vendor')
def vendor_dashboard():
    if session.get("role") != "vendor":
        return redirect('/')
    return render_template("vendor/vendor_dashboard.html")


@app.route('/vendor/your-item')
def vendor_your_item():
    if session.get("role") != "vendor":
        return redirect('/')
    products = Product.query.filter_by(vendor_id=session["user_id"]).all()
    return render_template("vendor/your_item.html", products=products)


@app.route('/vendor/add-new-item', methods=["GET","POST"])
def vendor_add_new_item():
    if session.get("role") != "vendor":
        return redirect('/')

    if request.method == "POST":
        product = Product(
            vendor_id=session["user_id"],
            name=request.form["name"],
            price=request.form["price"],
            status=request.form["status"]
        )
        db.session.add(product)
        db.session.commit()
        return redirect('/vendor/your-item')

    return render_template("vendor/add_new_item.html")


@app.route('/vendor/delete/<int:id>')
def vendor_delete(id):
    if session.get("role") != "vendor":
        return redirect('/')
    Product.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/vendor/your-item')


@app.route('/vendor/transaction')
def vendor_transaction():
    if session.get("role") != "vendor":
        return redirect('/')
    orders = Order.query.all()
    return render_template("vendor/transaction.html", orders=orders)
@app.route('/vendor-list')
def vendor_list():
    if session.get("role") != "user":
        return redirect('/')

    vendors = User.query.filter_by(role="vendor").all()
    return render_template("user/vendor_list.html", vendors=vendors)



# ---------- User ----------
@app.route('/user')
def user_dashboard():
    if session.get("role") != "user":
        return redirect('/')

    vendors = User.query.filter_by(role="vendor").all()
    return render_template("user/user_dashboard.html", vendors=vendors)


@app.route('/cart')
def cart():
    if session.get("role") != "user":
        return redirect('/')

    orders = Order.query.filter_by(user_id=session["user_id"], status="pending").all()

    grand_total = 0
    for order in orders:
        grand_total += order.total_amount

    return render_template("user/cart.html", orders=orders, grand_total=grand_total)


@app.route('/payment', methods=["GET","POST"])
def payment():

    if session.get("role") != "user":
        return redirect('/')

    if request.method == "POST":

        # Store details in session for success popup
        session["checkout_data"] = {
            "name": request.form["name"],
            "email": request.form["email"],
            "number": request.form["number"],
            "payment_method": request.form["payment_method"],
            "address": request.form["address"],
            "city": request.form["city"],
            "state": request.form["state"],
            "pincode": request.form["pincode"]
        }

        # Mark orders as paid
        Order.query.filter_by(user_id=session["user_id"], status="pending").update({"status":"paid"})
        db.session.commit()

        return redirect('/success')

    return render_template("user/checkout.html")



@app.route('/success')
def success():

    data = session.get("checkout_data")

    orders = Order.query.filter_by(user_id=session["user_id"], status="paid").all()
    total = sum(o.total_amount for o in orders)

    return render_template("user/success.html", data=data, total=total)

@app.route('/remove-order/<int:id>')
def remove_order(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/cart')


@app.route('/delete-all')
def delete_all():
    Order.query.filter_by(user_id=session["user_id"], status="pending").delete()
    db.session.commit()
    return redirect('/cart')

if __name__ == "__main__":
    app.run(debug=True)
