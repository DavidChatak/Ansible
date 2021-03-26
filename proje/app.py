import mysql.connector as mc
from flask import Flask, request, render_template
from flaskext.mysql import MySQL

# Create an object named app
app = Flask(__name__)

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] =  'localhost'  # 'test_db_server' #
app.config['MYSQL_DATABASE_USER'] = 'david'
app.config['MYSQL_DATABASE_PASSWORD'] = 'David_123'
app.config['MYSQL_DATABASE_DB'] = 'phonebook_db'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

mydb = mc.connect(
  host= 'localhost', #"test_db_server",
  user="david",
  password="David_123"
)
mycursor = mydb.cursor()
q = '''
CREATE DATABASE IF NOT EXISTS mydatabase;
'''
mycursor.execute(q)
print("PYTHON DB CONNECTOR DB")
mycursor.execute("select * from phonebook_db.phonebook")
res2 = mycursor.fetchall()
for x in res2:   print(x)
query = """
CREATE TABLE IF NOT EXISTS phonebook_db.phonebook(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    number VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
cursor.execute(query)
query = '''

INSERT INTO phonebook_db.phonebook (name, number)
    VALUES
        ("Callahan2", "1234567890"),
        ("Sergio Taco2", "67854"),
        ("Vincenzo Altobelli2", "876543554");
'''
# cursor.execute(query)
cursor.execute("select * from phonebook")
res = cursor.fetchall()
print("the R E S U L T:", len(res))
@app.route("/")
def main():
    # return "hello world2"
    return f"""
    {str(len(res))} 
    """



app.run(host='0.0.0.0', port=81, debug='On')