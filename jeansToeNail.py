import sqlite3

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

sql = """CREATE TABLE IF NOT EXISTS users(
    userID INT SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type CHAR(30) NOT NULL,
    login FOREGIN KEY,
    contact_phone INT NOT NULL,
    email VARCHAR(50) NOT NULL,
    gender CHAR(20) NOT NULL,
    approved TEXT CHECK (approved IN('Pending', 'Approved', 'Rejected'))
    )"""

cursor.execute(sql)

sql = """CREATE TABLE IF NOT EXISTS login(
    userID INT PRIMARY KEY,
    username CHAR(30) NOT NULL,
    password VARCHAR(120) NOT NULL,
)"""

cursor.execute(sql)



sql = """CREATE TABLE IF NOT EXISTS membership(
    userID PRIMARY KEY,
    club VARCHAR(50)
    )"""

cursor.execute(sql)

#coordinator name



print("PASAPORTE")


conn.commit()
conn.close()



