from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyB7oo7flWhavDdrpE8xoL3J-j9lbfZYbHA",
  "authDomain": "indproject-8022d.firebaseapp.com",
  "databaseURL": "https://indproject-8022d-default-rtdb.firebaseio.com",
  "projectId": "indproject-8022d",
  'storageBucket': "indproject-8022d.appspot.com",
  "messagingSenderId": "483700462817",
  "appId": "1:483700462817:web:d8e1bb12073cce79d013a0",
  "measurementId": "G-44FJG413BR",
  "databaseURL":"https://indproject-8022d-default-rtdb.firebaseio.com/"
    }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=='POST':
        print('hi')
        email=request.form['email']
        password=request.form['password']
        try:
            print('hi')
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)   
            print('hi')
            return render_template("add_note.html")
        except:
            return render_template("signin.html")
    else:
        return render_template("signin.html")

    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method== 'POST':
        email=request.form['email']
        password = request.form['password']
        username = request.form['username']
        full_name = request.form['full_name']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user={"name":username,"email":email,"username":username, "full_name":full_name, 'bio': bio}
            UID = login_session['user']['localId']
            db.child("USers").child(UID).set(user)
            return render_template("add_note.html")
        except:
            print("errorrr")
            return render_template("signup.html")
    return render_template("signup.html") 



@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        text = request.form['text']
        title = request.form['title']
        UID = login_session['user']['localId']
        note={"title":title, "text":text, "UID":UID}
        db.child("notes").push(note)
        return redirect(url_for('all_notes'))
    return render_template("add_note.html")




@app.route("/all_notes", methods=['GET', 'POST'])
def all_notes():
    note = db.child("notes").get().val()
    return render_template("all_notes.html", note = note)









if __name__ == '__main__':
    app.run(debug=True)
