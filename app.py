from datetime import datetime
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from venmo_api import Client
from werkzeug.utils import secure_filename

import json
import os
import requests 

app = Flask(__name__)
UPLOAD_FOLDER = 'assets/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
item_list = []

db = SQLAlchemy(app)

# build login required module
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.Text, nullable=False)
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Expense: " + self.title +" "+ str(self.id)

class Debts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    debt_type = db.Column(db.String(10),nullable=False)
    payee = db.Column(db.String(100),nullable=False)
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return "Debt: " + self.title +" "+ str(self.id)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return "Friend: " + self.username +" "+ self.user_id

def get_user_id(username):
    users = venmo.user.search_for_users(query=username)
    for user in users:
        return(user.id)   

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

@app.route('/login',methods = ['GET','POST'])
def index():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        try:
            access_token = Client.get_access_token(username= username, password = password)
            global venmo
            venmo = Client(access_token=access_token)

            # new_user = User(username,user_id,access_token)
            return redirect('/expenses')
        except:
            error = "Invalid Credentials. Please Try Again"
        
        return render_template("login.html",error=error)
    else:
        return render_template("login.html",error=error)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/expenses',methods = ['GET','POST'])
def expenses():
    if request.method == "POST":
        expense_title = request.form['title']
        expense_amount = request.form['amount']
        expense_category = request.form['category']
        new_expense = Expenses(title=expense_title,amount=expense_amount,category=expense_category)
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/expenses')
    else:
        current_expenses = Expenses.query.order_by(Expenses.date_created).all()
        return render_template('expenses.html',expenses = current_expenses)

@app.route('/expenses/delete/<int:id>')
def delete_expense(id):
    expense = Expenses.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/debts',methods = ['GET','POST'])
def debts():
    if request.method == "POST":
        debt_title = request.form['title']
        debt_amount = request.form['amount']
        debt_type = request.form['debt_type']
        payee = request.form['payee']
        new_debt = Debts(title=debt_title,amount=debt_amount,debt_type=debt_type,payee=payee)
        db.session.add(new_debt)
        db.session.commit()
        return redirect('/debts')
    else:
        current_debts = Debts.query.order_by(Debts.date_created).all()
        friends = Friends.query.all()
        return render_template("debts.html",friends = friends,debts=current_debts)

@app.route('/debts/delete/<int:id>')
def delete_debt(id):
    debt = Debts.query.get_or_404(id)
    db.session.delete(debt)
    db.session.commit()
    return redirect('/debts')

@app.route('/friends',methods = ['GET','POST'])
def friends():
    if request.method == "POST":
        friends = venmo.user.get_user_friends_list(venmo.my_profile().id)
        for friend in friends:
            friend_username = friend.username 
            friend_id = friend.id
            new_friend = Friends(username=friend_username,user_id=friend_id)
            db.session.add(new_friend)
            db.session.commit()
        return redirect('/friends')
    
    else:
        friends = Friends.query.all()
        return render_template("friends.html",friends = friends)

@app.route('/Requestnow/<int:id>',methods = ['POST'])
def requestnow(id):
    request = Debts.query.get_or_404(id)
    request_description = request.title
    request_amount = request.amount
    request_person = get_user_id(request.payee)
    print(request_amount,request_description,request_person)
    venmo.payment.request_money(request_amount,request_description,request_person)
    return redirect('/debts')

@app.route('/Paynow/<int:id>',methods = ['POST'])
def paynow(id):
    payment = Debts.query.get_or_404(id)
    payment_description = payment.title
    payment_amount = payment.amount
    payment_person = get_user_id(payment.payee)
    # print(request_amount,request_description,request_person)
    venmo.payment.send_money(payment_amount,payment_description,payment_person)
    return redirect('/debts')

@app.route('/calendar')
def calendar():
    return "This is Calendar Page"

@app.route('/scan', methods =['GET','POST'])
def scan_reciept():
    # if "file" not in request.files:
    #     flash("No image selected")
    #     return redirect('/scan')
    global item_list
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
            imageFile = "assets/{}".format(filename) # // Modify it to use your own file
            r = requests.post(receiptOcrEndpoint, data = { \
              'client_id': 'TEST',        # Use 'TEST' for testing purpose \
              'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
              'ref_no': 'ocr_python_124', # optional caller provided ref code \
              }, \
            files = {"file": open(imageFile, "rb")})
            result = (r.text)
            data = json.loads(result)
            item_list =[]
            for receipt in (data['receipts']):
                items = (receipt['items'])
                for item in items:
                    item_list.append(item)
            
            print(item_list)
                       
            return redirect('/scan')
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

    else:
        if(len(item_list)==0):
            item_list=[]
        return render_template("scan.html",scanned_items = item_list)

    
if __name__ == "__main__":
    app.run(debug=True)
