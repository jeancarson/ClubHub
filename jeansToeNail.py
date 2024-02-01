import sqlite3

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

sql = """CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    type CHAR(30) NOT NULL,
    username CHAR(30) NOT NULL,
    password VARCHAR(120) NOT NULL,
    contact_phone INT NOT NULL,
    email VARCHAR(50) NOT NULL,
    gender CHAR(20) NOT NULL,
    approved TEXT CHECK (approved IN('Pending', 'Approved', 'Rejected'))
    )"""

cursor.execute(sql)


sql = """CREATE TABLE IF NOT EXISTS connections(
    id PRIMARY KEY,
    club VARCHAR(50)
    )"""

cursor.execute(sql)

#sql = """CREATE TABLE IF NOT EXISTS typesBabes(
#    id PRIMARY KEY,
#    type CHAR(30) NOT NULL,
#    )"""


print("PASAPORTE")


conn.commit()
conn.close()



