import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database = "accounting"
)

mycursor = mydb.cursor()
mycursor.execute(' CREATE TABLE accounting( id int(11) NOT NULL AUTO_INCREMENT, userid VARCHAR(255), minecraftNick VARCHAR(20),debit INTEGER(10), credit INTEGER(10), PRIMARY KEY (id))')