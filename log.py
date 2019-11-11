from flask import Flask, redirect, url_for, request, render_template , session, escape, request
from flask.helpers import send_from_directory 
from database.db import db_interface
app = Flask(__name__) 
app.secret_key = "any random string"
psql = None
@app.route('/')
def index():
   if 'username' in session:
      data = {}
      data['username'] = session['username']
      data['profile'] = "Being Human"
      data['skills'] = "Nothing"
      
      return render_template("Fac_port.html",data=data)
   return redirect(url_for('login'))
@app.route('/success/<name><pwd>') 
def success( name  , pwd ): 
   return  name +"    "+pwd

@app.route('/logout')
def logout():
   session.pop('username',None)
   return redirect(url_for('home'))
@app.route('/home')
def home():
   return render_template('home.html')
@app.route('/login',methods = ['POST', 'GET']) 
def login(): 
   if request.method == 'POST': 
      user = request.form['email'] 
      goif = psql.check_employee([request.form['email'],request.form['password']])
      pwd = request.form['password']
      print (goif)
      if goif[0] == True :
         session['username'] = user
      print(user, pwd)
      return redirect(url_for('index')) 
   else: 
      return render_template("login.html")

@app.route('/register' , methods = ['POST','GET'])
def register():
    if request.method == 'POST':      
      user = request.form['email']
      pwd1 = request.form['password']
      print(user,pwd1)
      psql.insert_employee([request.form['Name'],request.form['password'],request.form['Departement'],request.form['Gender'],request.form['email']])
      return redirect(url_for('success' , name = user , pwd = pwd1))  
    else :
      return render_template("register.html")   

  
if __name__ == '__main__': 
   psql = db_interface()
   app.run(debug = True) 
