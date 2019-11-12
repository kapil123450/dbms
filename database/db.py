import psycopg2

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
        sql = """INSERT INTO employee(Name,Password,Departement,Gender,EmailId)
                VALUES(%s,%s,%s,%s,%s) RETURNING FacultyId;"""
        
        faculty_id = None
        try:
            print(emp)
            #self.conn= psycopg2.connect(database = "dbms",user = "postgres",password = "12345678",host = "localhost",port = 5432)
            cur = self.conn.cursor()
            cur.execute(sql, (emp[0],emp[1],emp[2],emp[3],emp[4]))
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


        
    
    
