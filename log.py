from flask import Flask, redirect, url_for, request, render_template , session, escape, request
from flask.helpers import send_from_directory 
from database.db import db_interface
import pymongo
import os
from dotenv import load_dotenv
from datetime import date

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

##ADMIN
@app.route('/admin',methods = ['POST','GET'])
def admin():
   return render_template("Admin.html")
@app.route('/updateLeaves',methods = ['POST','GET'])
def updateLeaves():
   if request.method == "POST":
      nb_leave  = request.form['leaves']
      print(nb_leave)
      psql.setLeaves(nb_leave)
   return render_template("Admin.html")

@app.route('/clearPath')
def clearPath():
   psql.clearPath()
   return render_template("Admin.html")

@app.route('/setPath',methods = ['POST','GET'])
def setPath():
   if request.method == "POST":
      pathmember  = request.form['pathmember']
      psql.setPaths(pathmember)
   return render_template("Admin.html")

@app.route('/setCrossFaculty',methods = ['POST','GET'])
def setCrossFaculty():
   if request.method == "POST":
      designation  = request.form['designation']
      gmail = request.form['email']
      print(designation)
      print(gmail)
      if designation in ["HODCSE","HODME","HODEE"]:
         return redirect(url_for("admin_hod",email = gmail))
      else : 
         return redirect(url_for('admin_dean',email = gmail , designation = designation ,))
   return render_template("Admin.html")

@app.route('/admin_hod/<email>')
def admin_hod(email):
   fid = psql.check_employee_for_HOD([email])  #fid has fid,department
   print(fid)
   hod_log = psql.check_In_hod([fid[1]])   # it return start date and fid of privious hod of that dep.
   print(hod_log)
   if hod_log[0] != False:
      psql.insert_LOG_OF_HOD([hod_log[1],hod_log[0],date.today(),fid[1]]) #insert that fid and start and end date into log of hod table.
      psql.update_HOD_Table([date.today(),fid[0],fid[1]])
   else : 
      psql.insert_HOD_Table([date.today(),fid[0],fid[1]])  #insert new hod into hod table.
   return render_template("Admin.html")

@app.route('/admin_dean/<email>/<designation>')
def admin_dean(email , designation):
   fid = psql.check_employee_for_dean([email])  #it return faculty id related to that email
   dean_log = psql.check_In_dean([designation])   # it return start date and fid of privious dean.
   
   print("fid :" ,fid)
   print(dean_log)
   if dean_log[0]!=False:
      psql.insert_LOG_OF_dean([dean_log[0],date.today(),dean_log[1],designation]) #insert that fid and start and end date into log of hod table.
      psql.update_dean_Table([date.today(),fid[0],designation]) 
   else : psql.insert_dean_Table([date.today(),fid[0],designation])  #insert new hod into hod table.
   return render_template("Admin.html")

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
      print(request.form['departement'])
      print(user,pwd1)
      fid = psql.insert_employee([request.form['Name'],request.form['password'],request.form['departement'],request.form['email']])
      my_collection.insert_one({"_id":fid , "email":user ,"name":request.form['Name'],"departement":request.form['departement']})
      leave = psql.check_leaves()
      psql.insert_faculty([fid,leave,leave])
      psql.insert_log_of_faculty([fid,date.today(),date.today(),request.form['departement']])
      return redirect(url_for('home'))  
   else :
      return render_template("register.html")  



if __name__ == '__main__': 
   psql = db_interface()
   app.run(debug = True) 