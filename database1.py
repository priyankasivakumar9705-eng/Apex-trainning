import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="",
    raise_on_warnings=True
)
cursor = conn.cursor()
print("Connected Successfully")
