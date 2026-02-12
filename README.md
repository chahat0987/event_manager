The Event Management System is a web-based application developed using Flask (Python) and SQLite database.

This system allows:

👨‍💼 Vendors to add and manage products/services

👤 Users to browse vendors, add products to cart, and make payments

💳 Checkout and Payment simulation

📦 Order confirmation popup after successful payment

The project follows the required flowchart structure provided in the assignment.

🛠 Technologies Used

Python 3

Flask

Flask-SQLAlchemy

SQLite

HTML5

CSS3

Jinja2 Templates

Project Structure
event_management_system/
│
├── app.py
├── models.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── vendor/
│   │     └── vendor_dashboard.html
│   ├── user/
│   │     ├── user_dashboard.html
│   │     ├── cart.html
│   │     ├── checkout.html
│   │     └── success.html
│
├── static/
│   ├── css/
│   │     └── style.css
│   └── images/
│
└── database.db
🔁 Application Flow
START
   ↓
INDEX
   ↓
LOGIN
   ↓
VENDOR / USER

Vendor Module

Add Product (with image upload)

View Products

Delete Products

User Module

View Dashboard

Add to Cart

View Cart

Checkout

Payment Success Popup

🔐 Authentication

Role-based login system

Session management

Password is securely hashed

Separate access for Vendor and User

🛒 Shopping Cart Features

View cart items

Calculate total amount

Remove item

Delete all items

Proceed to checkout

💳 Checkout Features

Name

Email

Phone Number

Address

City

State

Pin Code

Payment Method (Cash / UPI)

After successful order:

Thank You popup appears

Total amount displayed

Continue Shopping option

🧠 Database Models
User

id

name

email

password

role

Product

id

vendor_id

name

price

image

Order

id

user_id

product_id

total_amount

status (pending / paid)

▶️ How To Run The Project
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run Application
python app.py

3️⃣ Open Browser
http://127.0.0.1:5000

✅ Assignment Requirements Covered

✔ Role-based login
✔ Session management
✔ Form validations
✔ Image upload
✔ Cart system
✔ Payment simulation
✔ Success popup
✔ Proper folder structure

👨‍💻 Developed By

Chahat Jain
B.Tech Assignment Project
