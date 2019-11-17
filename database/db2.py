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
        sql1 = """ SELECT leave_id FROM log_of_leaves WHERE fid = %s AND status_ = 1 """
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
                pendingLeaveIds = li
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
            return lid 
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def getDetailsFromApplicant(self, leave_id):
        li = []
        sql = """SELECT reason , status_ , time_of_generation , borrow ,fid FROM log_of_leaves WHERE leave_id = %s"""
        try:
            cur = self.conn.cursor()
            lid = [False]
            cur.execute(sql, (leave_id,))
            li = []
            for x in cur:
                li.append([x[0], x[1], x[2], x[3],x[4]])
                lid = li
            cur.close()
            return lid
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def getDetailsFromVerifiers(self, leave_id):
        sql = """SELECT fid , position_level , comment , status_ FROM log_of_leaves_comment WHERE leave_id = %s"""
        try:
            cur = self.conn.cursor()
            lid = [False]
            cur.execute(sql, (leave_id,))
            li = []
            for x in cur:
                li.append([x[0], x[1], x[2], x[3]])
                lid = li
            cur.close()
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
    
    def checkSpecialPortal(self, user_id):
        sql1 = """ SELECT fid FROM HOD WHERE fid = %s """
        sql2 = """ SELECT fid FROM CROSS_FACULTY WHERE fid = %s """
        try:
            cur = self.conn.cursor()
            cur.execute(sql1, (user_id,))
            for x in cur:
                return [True]
            cur.execute(sql2, (user_id,))
            for x in cur:
                return [True]
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