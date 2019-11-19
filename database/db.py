import psycopg2
import sqlite3
import logging
class db_interface:
    def __init__(self):
        self.connect()
    conn= None
    def connect(self):
        
        """ Connect to the PostgreSQL database server """
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn= psycopg2.connect(database = "dbms",user = "postgres",password = "12345678",host = "localhost",port = 5432)

            cur = self.conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def insert_employee(self , emp):
        """ insert a new vendor into the vendors table """
        sql = """INSERT INTO employee(Name,Password,Departement,EmailId)
                VALUES(%s,%s,%s,%s) RETURNING FacultyId;"""
        
        faculty_id = None
        try:
            print(emp)
            #self.conn= psycopg2.connect(database = "dbms",user = "postgres",password = "12345678",host = "localhost",port = 5432)
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3]))
            faculty_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            return faculty_id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def check_employee(self, log):
        email = log[0]
        passd = log[1]
        sql = """SELECT emailid , password , facultyid from employee where emailid = %s and password = %s ;"""
        try:
            #self.conn= psycopg2.connect(database = "dbms",user = "postgres",password = "12345678",host = "localhost",port = 5432)
            cur = self.conn.cursor()
            cur.execute("""SELECT emailid , password , facultyid from employee where emailid = %s and password = %s ;""",(log[0],log[1]))
            
            Exist = False
            val = [False]
            for x in cur :
                if x[0] == email and x[1] == passd :
                    Exist = True
                    val = [True,x[2]]
                    break
            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def clearPath(self):
        try :
            cur = self.conn.cursor()
            cur.execute("DELETE FROM admin_path_faculty");
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def setLeaves(self , nb_leave):
        try :
            cur = self.conn.cursor()
            print(nb_leave)
            
            cur.execute(" INSERT INTO Admin_leave (nb_leaves) VALUES(%s) " , (nb_leave ,))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
    def setPaths(self , path):
        try :
            cur = self.conn.cursor()
            cur.execute(" INSERT INTO Admin_path_faculty (designation) VALUES(%s) " , (path ,))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    ###########  HOD UPDATE #################
    def check_employee_for_HOD(self, log):
        email = log[0]
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT emailid , facultyid ,Departement from employee where emailid = %s  """,(log[0] ,))
            
            Exist = False
            val = []
            for x in cur :
                if x[0] == email :
                    Exist = True
                    val = [x[1],x[2]]
                    break
            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_In_hod(self, log):
        dep = log[0]
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT start_date_of_hod ,fid from HOD where departement = %s  """,(log[0],))
            
            val = [False]
            
            for x in cur :
                val = [x[0],x[1]]
            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def insert_LOG_OF_HOD(self , emp):
        sql = """INSERT INTO LOG_FOR_HOD(fid,start_date_of_hod,end_date_of_hod,departement)
                VALUES(%s,%s,%s,%s)"""  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_HOD_Table(self , emp):
        sql = """INSERT INTO HOD(start_date_of_hod,fid,departement)
                VALUES(%s,%s,%s)"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def update_HOD_Table(self , emp):
        sql = """UPDATE HOD
                SET start_date_of_hod = %s
                , fid = %s
                WHERE departement = %s"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def check_leaves(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT nb_leaves  from Admin_leave ORDER BY id DESC""")
            leaves = cur.fetchone()[0]
            cur.close()
            return leaves
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_faculty(self , emp):
        sql = """INSERT INTO faculty(fid,leaves_current_year,leaves_next_year)
                VALUES(%s,%s,%s)"""  # %d with date specifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_log_of_faculty(self , emp):
        sql = """INSERT INTO log_of_faculty(fid,start_date_of_faculty,end_date_of_faculty,departement)
                VALUES(%s,%s,%s,%s)"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    ######## HOD UPDATE ###############

    ######## CROSS FACULTY UPDATE #########
    def check_employee_for_dean(self, log):
        email = log[0]
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT emailid , facultyid  from employee where emailid = %s """,(log[0] ,))
            val = [False]
            for x in cur :
                if x[0] == email :
                    Exist = True
                    val = [x[1]]
                    break
            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def check_In_dean(self, log):
        desg = log[0]
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT start_date_of_cross_faculty ,fid from CROSS_FACULTY where designation = %s  """,(log[0] ,))
            
            val = [False]
            for x in cur :
                val = [x[0],x[1]]
            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_LOG_OF_dean(self , emp):
        sql = """INSERT INTO LOG_FOR_CROSS_FACULTY(start_date_of_cross_faculty,end_date_of_cross_faculty,fid,designation)
                VALUES(%s,%s,%s,%s) """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_dean_Table(self , emp):
        sql = """INSERT INTO CROSS_FACULTY(start_date_of_cross_faculty,fid,designation)
                VALUES(%s,%s,%s)"""  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def update_dean_Table(self , emp):
        sql = """UPDATE CROSS_FACULTY
                SET start_date_of_cross_faculty = %s,
                fid = %s
                WHERE designation = %s"""  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def getAllLeaveRequests(self, fid):
        sql1 = """ SELECT leave_id FROM log_of_leaves_comment WHERE fid = %s AND status_ = 1 """
        sql2 = """ SELECT leave_id FROM log_of_leaves_comment WHERE fid = %s AND status_ = 2 """
        sql3 = """ SELECT leave_id FROM log_of_leaves_comment WHERE fid = %s AND status_ = 0 """
        try:
            cur = self.conn.cursor()
            lid = {}
            cur.execute(sql1, (fid,))
            pendingLeaveIds = [False]
            li = []
            for x in cur:
                li.append(x[0])
                pendingLeaveIds = [True,li]
            approvedLeaveIds = [False]
            li = []
            cur.execute(sql2, (fid,))
            for x in cur:
                li.append(x[0])
                approvedLeaveIds = li
            rejectedLeaveIds = [False]
            li = []
            cur.execute(sql3 , (fid ,))
            for x in cur:
                li.append(x[0])
                rejectedLeaveIds = li
            lid['pendingLeaveIds'] = pendingLeaveIds
            lid['approvedLeaveIds'] = approvedLeaveIds
            lid['rejectedLeaveIds'] = rejectedLeaveIds
            print(lid)
            return lid 
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def getDetailsFromApplicant(self, leave_id):
        li = []
        sql = """SELECT reason , status_ , time_of_generation , borrow ,fid ,nb_leaves ,end_date FROM log_of_leaves WHERE leave_id = %s"""
        try:
            cur = self.conn.cursor()
            lid = [False]
            cur.execute(sql, (leave_id,))
            li = []
            for x in cur:
                print(x)
                li =[x[0], x[1], x[2], x[3],x[4],x[5],x[6]]
                lid = li
            cur.close()
            print(lid)
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
    def getlr(self, fid):
        li = []
        sql = """SELECT leave_id FROM log_of_leaves WHERE fid = %s"""
        try:
            cur = self.conn.cursor()
            lid = [False]
            cur.execute(sql, (fid,))
            li = []
            for x in cur:
                print(x)
                li.append(x[0])
                lid = li
            cur.close()
            print(lid)
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
    def getNamefromempl(self, fid):
        li = []
        sql = """SELECT name FROM employee WHERE facultyid = %s"""
        try:
            cur = self.conn.cursor()
            lid = [False]
            cur.execute(sql, (fid,))
            li = []
            for x in cur:
                li =[x[0]]
                lid = li
            cur.close()
            print(lid)
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def getDetailsFromVerifiers(self, leave_id):
        sql = """SELECT fid , position_level , comment , status_ , time_of_generation FROM log_of_leaves_comment WHERE leave_id = %s"""
        try:
            cur = self.conn.cursor()
            lid = [False]
            cur.execute(sql, (leave_id,))
            li = []
            for x in cur:
                li.append([x[0], x[1], x[2], x[3],x[4]])
                lid = li
            lid_new = []
            for x in lid :
                fid = x[0]
                print(fid)
                cur.execute("""SELECT name FROM employee WHERE facultyid = %s""",(fid,))
                tmp = cur.fetchone()
                lid_new.append([x[0], x[1], x[2], x[3],x[4],tmp[0]])
            if len(lid_new)!=0:
                lid = lid_new
            cur.close()
            print(lid)
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def checkPendingLeave(self, user_id):
        sql1 = """ SELECT leave_id FROM log_of_leaves WHERE fid = %s AND status_ = 1 """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (user_id,))
            lid = [False]
            for x in cur:
                lid = [True, x[0]]
            cur.close()
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def checkSentBackLeaveId(self, user_id):
        sql1 = """ SELECT leave_id FROM log_of_leaves WHERE fid = %s AND status_ = 3 """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (user_id , ))
            lid = [False]
            for x in cur:
                lid = [True, x[0]]
            cur.close()
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def getsendBackById(self, leave_id):
        sql1 = """ SELECT fid FROM log_of_leaves_comment WHERE leave_id = %s AND status_ = 3 """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (leave_id , ))
            lid = [False]
            for x in cur:
                lid = [True, x[0]]
            cur.close()
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def getInittialReason(self, leave_id):
        sql1 = """ SELECT reason FROM log_of_leaves WHERE leave_id = %s AND status_ = 3 """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (leave_id , ))
            lid = [False]
            for x in cur:
                lid = [True, x[0]]
            cur.close()
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def checkSpecialPortal(self, user_id):
        sql1 = """ SELECT fid FROM HOD WHERE fid = %s """
        sql2 = """ SELECT designation FROM CROSS_FACULTY WHERE fid = %s """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (user_id,))
            for x in cur:
                return [True,'HOD']
            cur.execute(sql2, (user_id,))
            for x in cur:
                return [True,x[0]]
            cur.close()
            return [False]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def getLeaves(self, user_id):
        sql1 = """ SELECT leaves_current_year , leaves_next_year FROM faculty WHERE fid = %s """
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (user_id,))
            lid = [False]
            for x in cur:
                lid = [x[0],x[1]]
            
            cur.close()
            return lid
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_log_of_leaves(self , emp):
        sql = """INSERT INTO log_of_leaves(status_,reason,borrow,fid,time_of_generation,end_date ,nb_leaves)
                VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING leave_id """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],emp[4],emp[5],emp[6],))
            leave_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            return leave_id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_path(self ,log ):
        sql1 = """ SELECT fid FROM hod WHERE fid = %s"""
        sql2 = """ SELECT fid FROM cross_faculty WHERE fid = %s"""
        try:
            cur = self.conn.cursor()
            flag = [-1]
            li = []
            cur.execute(sql1 , (log ,))
            for x in cur:
                cur.execute(""" select designation from Admin_path_hod """)
                for x in cur:
                    li.append(x[0])
                cur.close()
                return li
            cur.execute(sql2 , (log ,))
            for x in cur:
                cur.execute(""" select designation from Admin_path_hod """)
                for x in cur:
                    li.append(x[0])
                cur.close()
                return li
            else:
                cur.execute(""" select designation from Admin_path_faculty """)
                for x in cur:
                    li.append(x[0])
                cur.close()
                return li
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_current_leave(self , emp):
        sql = """INSERT INTO current_leaves(leave_id,status_,comment,borrow,fid,position_level,time_of_generation)
                VALUES(%s,%s,%s,%s,%s,%s,%s) """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],emp[4],emp[5],emp[6],))
            
            self.conn.commit()
            cur.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_fixed_level(self , log):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT level_posiotion from level_table where designation = %s """,(log[0],))
            post_level =cur.fetchone()[0]

            cur.close()
            return post_level
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_log_of_faculty_dep(self , log):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT departement from log_of_faculty where fid = %s """,(log[0],))
            dep =cur.fetchone()[0]

            cur.close()
            return dep
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def upudate_log_leave_comment(self , emp):
        sql = """UPDATE log_of_leaves_comment
          SET  status_ = %s,
          comment = comment || %s ,
          time_of_generation =%s 
          where fid =%s and leave_id = %s
            """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            print("emp : ",emp)
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],emp[4],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_log_of_leave_status(self , emp):
        sql = """UPDATE log_of_leaves
          SET  
          status_ = %s,
          reason = %s,
          time_of_generation =%s 
          where leave_id = %s
            """  #here i have to change %d %d with corresponding date signifier.
        try:
            print("1 : ",emp)
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_log_leave_comment(self , emp):
        sql = """INSERT INTO log_of_leaves_comment(leave_id , status_ , comment , fid , time_of_generation , position_level)
                VALUES(%s,%s,%s,%s,%s,%s) """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute("""INSERT INTO log_of_leaves_comment(leave_id , status_ , comment , fid , time_of_generation , position_level)
                VALUES(%s,%s,%s,%s,%s,%s) """, (emp[0],emp[1],emp[2],emp[3],emp[4],emp[5],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_current_leave(self , emp):
        sql = """UPDATE current_leaves
          SET  position_level = %s,
          time_of_generation =%s 
          where leave_id = %s
            """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_log_of_leave(self , emp):
        sql = """UPDATE log_of_leaves
          SET  status_ = %s
          
          where leave_id = %s and fid = %s
            """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def decrese_current_leave_in_faculty(self , user_id):
        sql = """UPDATE faculty
          SET  leaves_current_year = leaves_current_year-%s,
          leaves_next_year = leaves_next_year-%s 
          where  fid = %s
            """  #here i have to change %d %d with corresponding date signifier.
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (user_id[0],user_id[1],user_id[2],))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_reaction(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT comment ,status_  from reaction """)
            val = [False]
            for x in cur :
                val = [x[0],x[1]]

            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_for_leave_faculty(self, log):
        fid = log[0]
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT leaves_current_year  , leaves_next_year from faculty where fid = %s """,(log[0] ,))

            val = [False]
            for x in cur :
                if x[0] >= 0 :
                    val = [True,x[0],x[1]]
                    break
            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def delete_from_current_table_of_leave(self, log):
        fid = log[0]
        try:
            cur = self.conn.cursor()
            cur.execute("""DELETE FROM current_leaves where leave_id = %s """,(log[0] ,))
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def insertOrUpdateReview_in_log_of_review(self , log):
        sql1 = """ SELECT leave_id , to_fid FROM log_of_review WHERE leave_id = %s AND to_fid = %s """
        sql2 = """ INSERT INTO log_of_review(leave_id ,to_fid , review) VALUES(%s ,%s ,%s) """
        sql3 = """ UPDATE log_of_review 
                    SET review = review || %s 
                    WHERE leave_id = %s AND to_fid = %s"""
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql1,(log[0] ,log[1] , ))
            leave_id = [-1]
            for x in cur:
                leave_id = [x[0],x[1]]
            if leave_id[0] != -1:
                cur.execute(sql3,(log[2],log[0],log[1],))
            else : 
                cur.execute(sql2 , (log[0],log[1],log[2],))
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def getSendBackReview(self, log):
        sql = """ SELECT review FROM log_of_review WHERE leave_id = %s AND to_fid = %s """
        try:
            cur = self.conn.cursor()
            cur.execute(sql,(log[0] ,log[1],))
            lid = [-1]
            for x in cur:
                lid = [x[0]]
            cur.close()
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def setPathsCrf(self, log):
        sql = """ INSERT INTO admin_path_hod (designation) VALUES (%s) """
        try:
            cur = self.conn.cursor()
            cur.execute(sql,(log,))
            
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def clearPathrf(self):
        try :
            cur = self.conn.cursor()
            cur.execute("DELETE FROM admin_path_hod");
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_my_name_in_employee(self, log):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT name from employee where facultyid = %s  """,(log[0] ,))

            val = []
            for x in cur :
                val = [x[0]]

            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def check_log_of_faculty_for_fid(self):
        #email = log[0]
        sql1= """SELECT fid  from log_of_faculty where start_date_of_faculty = end_date_of_faculty """
        sql2= """SELECT fid  from log_of_faculty where start_date_of_faculty != end_date_of_faculty """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1)
            
            val = []
            val1 = []
            for x in cur :
                val.append(x[0]) 

            cur.execute(sql2)
            for x in cur:
                val1.append(x[0])
                
            cur.close()
            return val,val1
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def chek_details_in_log_of_leave(self, log):
        try:
            cur = self.conn.cursor()
            cur.execute("""SELECT leave_id , status_ , reason , borrow ,end_date ,nb_leaves ,time_of_generation  from log_of_leaves where fid = %s  """,(log[0] ,))

            val = []
            for x in cur :
                val.append(x)

            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def check_in_log_leave_comment(self, log):
        try :
            cur = self.conn.cursor()
            cur.execute("""SELECT leave_id , status_ , comment,time_of_generation,position_level from log_of_leaves_comment where fid = %s  """,(log[0] ,))

            val = []
            for x in cur :
                val.append(x)

            cur.close()
            return val
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)