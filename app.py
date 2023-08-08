from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from datetime import datetime
import pyrebase

Config = {
  "apiKey": "AIzaSyDc4exteOwNNfnuV1RIRP33GIDpxoZgdpc",
  "authDomain": "birthday16-213d1.firebaseapp.com",
  "projectId": "birthday16-213d1",
  "storageBucket": "birthday16-213d1.appspot.com",
  "messagingSenderId": "513487413739",
  "appId": "1:513487413739:web:08f89b7350d32b968f39ae",
  "measurementId": "G-Q0Q7YKKBJB",
  "databaseURL": "https://birthday16-213d1-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='docs', static_folder='statics')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = {
        "email":request.form['email'],
        "password":request.form['password'],
        "full_name":request.form['full_name'],      
        }
        try:
            print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            login_session['user'] = auth.create_user_with_email_and_password(email, password)

            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            print("LOOOOO")
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"

    return render_template("index.html",error = "authentication failed")

@app.route('/thanks')
def thanks(): 

    return render_template("thanks.html")


@app.route('/home')
def home(): 

    return render_template("home.html")

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    error = ""
    
    if request.method == 'POST':
        UID = login_session['user']['localId']  # Assuming you're using session for user data
        print(UID)
        Q1 = request.form['Q1']
        
        # Assuming 'db' is a database connection
        # current = db.child("Users").child(UID).get().val()
        # current["wish"] = Q1  # Update the specific key
        db.child("Users").child(UID).update({"wish": Q1})
        return render_template("thanks.html")
    
    return render_template("survey.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)



# #     if request.method == 'POST':

#         try:
           
#             tweet = {"Title":request.form['Title'],
#             "Text":request.form['Text'],
#             "uid": login_session['user']['localId'],
#             "Timestamp" : dt_string
#             }
#             db.child("Tweets").push(tweet)
#             return redirect(url_for('all_tweets'))
#         except:
#             error = "Authentication failed"
   
#     return render_template("add_tweet.html")