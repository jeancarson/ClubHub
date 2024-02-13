import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


sql_users = """
CREATE TABLE IF NOT EXISTS users(
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    contact_phone INT NOT NULL,
    email TEXT NOT NULL,
    gender TEXT NOT NULL,
    approved TEXT CHECK (approved IN('Pending', 'Approved', 'Rejected'))
)
"""
cursor.execute(sql_users)


sql_login = """
CREATE TABLE IF NOT EXISTS login (
    loginID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (userID) REFERENCES users(userID)
)
"""
cursor.execute(sql_login)





sql_coordinators = """
CREATE TABLE IF NOT EXISTS coordinators (
    coordinatorID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER UNIQUE,
    clubID INTEGER,
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (clubID) REFERENCES clubs(clubID)
)
"""
cursor.execute(sql_coordinators)


sql_membership = """
CREATE TABLE IF NOT EXISTS membership (
    userID INTEGER,
    clubID INTEGER,
    PRIMARY KEY (userID, clubID)
)
"""
cursor.execute(sql_membership)

conn.commit()
conn.close()
