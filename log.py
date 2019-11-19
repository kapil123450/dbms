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
   leaves = []
   specialPortal = [False]
   pendingLeave = [False]
   sentBackForReview = [False]
   sendBackById = [False]
   reason = [False]
   if not user_id:
      editflag = True
      user_id = session.get('_id')
      if user_id :
         leaves = psql.getLeaves(user_id)
         specialPortal = psql.checkSpecialPortal(user_id)
         pendingLeave = psql.checkPendingLeave(user_id)
         print("1 : uid : ", user_id)
         sentBackForReview = psql.checkSentBackLeaveId(user_id)
         if sentBackForReview[0] != False:
            sendBackById = psql.getsendBackById(sentBackForReview[1])
            reason = psql.getInittialReason(sentBackForReview[1])
         print("sp:",specialPortal)

   if not user_id :
      return redirect(url_for('login'))
   
   data = my_collection.find_one({"_id": int(user_id)})
   data['editflag'] = editflag
   if len(leaves) != 0:
      print(leaves)
      data['leaves_current_year'] = leaves[0]
      data['leaves_next_year']    = leaves[1]
   if pendingLeave[0] != False :
      data['pendingLeave'] = pendingLeave[0]
      data['pendingLeaveid'] = pendingLeave[1]
   if sentBackForReview[0] != False:
      data['sentBackForReview'] = sentBackForReview[0]
      data['sentBackForReviewId'] = sentBackForReview[1]
   if sendBackById[0] != False:
      data['sendBackById'] = sendBackById[1]
   if reason[0] != False:
      data['reason'] = reason[1]
   data['specialPortal'] = specialPortal[0]
   return render_template("Fac_port.html",data = data)

#### LEAVES ###### 
@app.route('/getResponseAccept', methods = ['POST','GET'])
def getResponseAccept(  ):
   leave_id = request.form['leave_id']
   applicant_id = request.form['applicant_id']
   nb_current_leaves = request.form['nb_current_leaves']
   nb_borrow_leaves = request.form['nb_borrow_leaves']
   print("2 : ",leave_id)
   print("3 : ",applicant_id)
   dep = psql.check_log_of_faculty_dep([applicant_id])
   comment = request.form['comment']
   spid = session.get('_id')
   print("4: ",spid)
   psql.upudate_log_leave_comment([2,comment,date.today(),spid,leave_id])
   list_path = psql.check_path(applicant_id)
   post = psql.checkSpecialPortal(spid)
   print("5 : " ,post)
   post_new = 0
   flag = False
   for i in range(len(list_path)):
      if list_path[i] == post[1] :
         if i== len(list_path)-1:
            flag = True
         else :
            post_new = list_path[i+1]
         break;
   
   print("6 : ",post_new)
   if flag :
      print("new post_last",post_new)
      psql.delete_from_current_table_of_leave([leave_id])
      psql.decrese_current_leave_in_faculty([nb_current_leaves,nb_borrow_leaves,applicant_id])  #it is like update we have to decrese leave number
      psql.update_log_of_leave([2,leave_id,applicant_id])
   else :
      sp_id = []
      if post_new in ['HOD']:
         sp_id = psql.check_In_hod([dep])
         print("spid:",sp_id)
         if sp_id[0] != False:
            spid = sp_id[1]
      else:
         sp_id = psql.check_In_dean([post_new])
         if sp_id[0] != False:
            spid = sp_id[1]
      print("7 : ",spid)
      post_level = psql.check_fixed_level([post_new])
      print("8 : ",post_level)
      psql.update_current_leave([post_level,date.today(),leave_id])
      psql.insert_log_leave_comment([leave_id,1,' ',spid,date.today(),post_level]) 
      return redirect(url_for("specialPortal"))  

   return redirect(url_for("specialPortal"))


@app.route('/getResponseReview', methods = ['POST','GET'])
def getResponseReview():
   leave_id = request.form['leave_id']
   applicant_id = request.form['applicant_id']
   print("2 : ",leave_id)
   print("3 : ",applicant_id)
   dep = psql.check_log_of_faculty_dep([applicant_id])
   comment = request.form['comment']
   spid = session.get('_id')
   print("4: ",spid)
   psql.upudate_log_leave_comment([3,comment,date.today(),spid,leave_id])
   psql.update_log_of_leave([3,leave_id,applicant_id])
   return redirect(url_for("specialPortal"))

@app.route('/getResponseRejected', methods = ['POST','GET'])
def getResponseRejected():
   leave_id = request.form['leave_id']
   applicant_id = request.form['applicant_id']
   print("2 : ",leave_id)
   print("3 : ",applicant_id)
   dep = psql.check_log_of_faculty_dep([applicant_id])
   comment = request.form['comment']
   spid = session.get('_id')
   print("4: ",spid)
   psql.upudate_log_leave_comment([0,comment,date.today(),spid,leave_id])
   psql.update_log_of_leave([0,leave_id,applicant_id])
   psql.delete_from_current_table_of_leave([leave_id])
   return redirect(url_for("specialPortal"))

@app.route('/sendBackAgain', methods = ['POST','GET'])
def sendBackAgain():
   if request.method == "POST" :
      sendBackById = request.form['sendBackById']
      review = request.form['review']
      leave_id = request.form['leave_id']
      reason = request.form['reason']
      print("sendId : ",sendBackById)
      print("review : ",review)
      print("leave_id : ",leave_id)
      print("reason : ",reason)

      psql.upudate_log_leave_comment([1," ",date.today(),sendBackById,leave_id])
      psql.insertOrUpdateReview_in_log_of_review([leave_id,sendBackById,review])
      psql.update_log_of_leave_status([1,reason,date.today(),leave_id])
   return redirect(url_for("portal"))



@app.route('/generateLeave', methods = ['POST','GET'])
def generateLeave():
   fid = session.get('_id')

   reason = request.form['reason']
   nb_leaves = request.form['nb_leaves']
   start_date = request.form['start_date']
   end_date = request.form['end_date']
   check_leave = psql.check_for_leave_faculty([fid]) #check whteher this faculty can avail leave or not
   dep = psql.check_log_of_faculty_dep([fid])
   print(check_leave)
   nb_borrow = 0
   nb_current = 0
   flag = True
   print("1 : ", check_leave)
   if check_leave[0] == True :
      if int(check_leave[1]) >= int(nb_leaves): 
         nb_current = int(nb_leaves)  
      else :
         nb_current = check_leave[1]
         print("2 : ", nb_current)
         nb_borrow = int(nb_leaves) - nb_current
         print("3 : ",nb_borrow)
         if nb_borrow > int(check_leave[2]) :
            flag = False
      
      if not flag :
         return redirect(url_for("portal"))
      else :
         leave_id = psql.insert_log_of_leaves([1,reason,nb_borrow,fid,start_date,end_date,nb_current]) # insert information in log_of _leave table for faculty.
         list_path = psql.check_path(fid) #check for list of path set by admin
         print(list_path)
         post_level = psql.check_fixed_level([list_path[0]])
         post = list_path[0]
         spid = 0
         psql.insert_current_leave([leave_id,1,' ',nb_borrow,fid,post_level,date.today()]) #insert information about leave in current leave table
         if post in ['HOD']:
            sp_id = psql.check_In_hod([dep])
            if sp_id[0] != False:
               spid = sp_id[1]
         else:
            sp_id = psql.check_In_dean([post])
            if sp_id[0] != False:
               spid = sp_id[1]
         print("1  : ", spid)
         psql.insert_log_leave_comment([leave_id,1,' ',spid,date.today(),post_level])

   return redirect(url_for("portal"))

@app.route('/generateLeaveApplicationPortal', methods = ['POST','GET'])
def generateLeaveApplicationPortal():
   return render_template("generatenewLeave.html")

@app.route('/specialPortal',methods = ['POST','GET'])
def specialPortal():
   fid = session.get('_id')
   data = {}
   lid = psql.getAllLeaveRequests(fid)
   print(lid)
   
   data['pendingLeaveIds'] = lid['pendingLeaveIds']
   data['approvedLeaveIds'] = lid['approvedLeaveIds']
   data['rejectedLeaveIds'] = lid['rejectedLeaveIds']
   return render_template("Special_portal.html",data = data)

@app.route('/detailsofleaveid/<leave_id>',methods = ['POST','GET'])
def detailsofleaveid(leave_id):
   fid = session.get('_id')
   data = {}
   leave_details_to_applicant = psql.getDetailsFromApplicant(leave_id)
   leave_details_to_verifier = psql.getDetailsFromVerifiers(leave_id)
   print(leave_details_to_applicant)
   print(leave_details_to_verifier)
   data['reason'] = leave_details_to_applicant[0]
   data['status_shown_to_applicant'] = leave_details_to_applicant[1]
   data['time_of_generation_applicant'] = leave_details_to_applicant[2]
   data['borroe_by_applicant'] = leave_details_to_applicant[3]
   data['applicant_id'] = leave_details_to_applicant[4]
   data['end_date_leave'] = leave_details_to_applicant[6]
   data['leave_details_to_verifier'] = leave_details_to_verifier
   data['name_applicant'] = psql.getNamefromempl(data['applicant_id'])
   print(data['name_applicant'])
   fid_ver = []
   for x in leave_details_to_verifier:
      fid_ver.append(psql.getNamefromempl(x[0])[0])
   data['name_of_ver'] = fid_ver
   print(fid_ver)
   return render_template("leaveid_details.html",data = data)

@app.route('/detailsofleaveidPending/<leave_id>',methods = ['POST','GET'])
def detailsofleaveidPending(leave_id):
   fid = session.get('_id')
   data = {}
   leave_details_to_applicant = psql.getDetailsFromApplicant(leave_id)
   leave_details_to_verifier = psql.getDetailsFromVerifiers(leave_id)
   leave_details_review = psql.getSendBackReview([leave_id,fid])
   data['reason'] = leave_details_to_applicant[0]
   data['status_shown_to_applicant'] = leave_details_to_applicant[1]
   data['time_of_generation_applicant'] = leave_details_to_applicant[2]
   data['borrow_by_applicant'] = leave_details_to_applicant[3]
   data['applicant_id'] = leave_details_to_applicant[4]
   data['nb_current_leaves'] = leave_details_to_applicant[5]
   data['end_date_leave'] = leave_details_to_applicant[6]
   data['name_applicant'] = psql.getNamefromempl(data['applicant_id'])
   data['leave_details_to_verifier'] = leave_details_to_verifier
   data['leave_id'] = leave_id
   data['leave_details_review'] = leave_details_review
   print(leave_details_review)
   return render_template("leaveid_details_pending.html",data = data)
##### ADMIN #####
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

@app.route('/setPathForCrossFaculty',methods = ['POST','GET'])
def setPathForCrossFaculty():
   if request.method == "POST":
      pathmember  = request.form['pathmember']
      psql.setPathsCrf(pathmember)
   return render_template("Admin.html")

@app.route('/clearPathCrossFaculty')
def clearPathCrossFaculty():
   psql.clearPathrf()
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

####Admin #########
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