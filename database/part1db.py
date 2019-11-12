import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="postgres",
  passwd="12345678",
  port = 5432
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)