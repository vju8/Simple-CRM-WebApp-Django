# Install Mysql on computer
# libraries: mysql, mysql-connector-python 



import mysql.connector
from decouple import config

dataBase = mysql.connector.connect(
    host = config('DB_HOST', default='localhost'), 
    user = config('DB_USER'), 
    password = config('DB_PASSWORD')
)


# initiate cursor object
cursorObject = dataBase.cursor()

# create a database 
cursorObject.execute("CREATE DATABASE CRM_APP")

print("Database created.")