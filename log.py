from flask import Flask, redirect, url_for, request, render_template , session, escape, request
from flask.helpers import send_from_directory 
from database.db import db_interface
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

my_client = pymongo.MongoClient('mongodb+srv://'+ os.environ.get('MONGO_USER', 'test') 
      +':'+ os.environ.get('MONGO_PASS', 'test') +'@mongodbms-nvis8.mongodb.net/test?retryWrites=true&w=majority')
try:
   print("MongoDB version is %s" %my_client.server_info()['version'])
   print("database is connected succesfully")
except pymongo.errors.OperationFaliure as error:
   print(error)

my_database = my_client.test 
my_collection = my_database.teach_info

#goif = []
app = Flask(__name__) 
app.secret_key = "any random string"
psql = None
   
@app.route('/setBio',methods = ['POST','GET'])
def setBio():
   if request.method == 'POST' and session.get('_id'):
      result = request.form
      my_collection.update_one({"_id":session['_id']},{"$set":{"biography":result['biography']}})
      print(result)
      return redirect(url_for('portal'))
@app.route('/Projects',methods = ['POST','GET'])
def setProjects():
   if request.method == 'POST' and session.get('_id'):
      result = request.form
      my_collection.update_one({"_id":session['_id']},{"$set":{"projects":result['projects']}})
      print(result)
      return redirect(url_for('portal'))
@app.route('/ResearchOutput',methods = ['POST','GET'])
def setResearch():
   if request.method == 'POST' and session.get('_id'):
      result = request.form
      my_collection.update_one({"_id":session['_id']},{"$set":{"research":result['research']}})
      print(result)
      return redirect(url_for('portal'))
@app.route('/Prizes',methods = ['POST','GET'])
def setPrizes():
   if request.method == 'POST' and session.get('_id'):
      result = request.form
      my_collection.update_one({"_id":session['_id']},{"$set":{"prizes":result['prizes']}})
      print(result)
      return redirect(url_for('portal'))
@app.route('/result',methods = ['POST','GET'])
def result():
   if request.method == 'POST' and session.get('_id'):
      result = request.form
      my_collection.update_one({"_id":session['_id']},{"$set":{"Biography":result['Biography'],
      "name":result['name'],"skills":result['skills'],"Research_paper":result['Research_paper'],
      "Experience":result['Experience'],"Education":result['Education']}})
      print(result)
      return redirect(url_for('portal'))
   else :
      return redirect(url_for('portal'))
@app.route('/success/<name><pwd>') 
def success( name  , pwd ): 
   return  name +"    "+pwd

@app.route('/failed/<name><pwd>') 
def failed( name  , pwd ): 
   return  "failed to login "+name +"    "+pwd

@app.route('/portal', defaults={'user_id': None})
@app.route('/portal/<user_id>',methods = ['POST','GET'])  
def portal(user_id):
   editflag = False
   if not user_id:
      editflag = True
      user_id = session.get('_id')
   if not user_id :
      return redirect(url_for('login'))
   data = my_collection.find_one({"_id": int(user_id)})
   data['editflag'] = editflag
   return render_template("Fac_port.html",data = data)



@app.route('/logout')
def logout():
   session.pop('username',None)
   session.pop('_id',None)
   return redirect(url_for('home'))
@app.route('/')
def home():
   my_LIST = list(my_collection.find())
   return render_template('home.html',my_LIST=my_LIST)


@app.route('/login',methods = ['POST', 'GET']) 
def login(): 
   if request.method == 'POST': 
      user = request.form['email'] 
      goif = psql.check_employee([request.form['email'],request.form['password']])
      pwd = request.form['password']
      print (goif)
      if goif[0] == True :
         session['username'] = user
         session['_id'] = goif[1]
         return redirect(url_for('portal'))
      else :
         return redirect(url_for('failed' , name = user , pwd = pwd)) 

      print(user, pwd)
       
   else: 
      return render_template("login.html")

@app.route('/register' , methods = ['POST','GET'])
def register():
   if request.method == 'POST':      
      user = request.form['email']
      pwd1 = request.form['password']
      print(user,pwd1)
      fid = psql.insert_employee([request.form['Name'],request.form['password'],request.form['Departement'],request.form['Gender'],request.form['email']])
      my_collection.insert_one({"_id":fid , "email":user ,"name":request.form['Name'],"departement":request.form['Departement']})
      return redirect(url_for('home'))  
   else :
      return render_template("register.html")   

  
if __name__ == '__main__': 
   psql = db_interface()
   app.run(debug = True) 