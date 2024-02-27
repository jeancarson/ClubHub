import sqlite3 



if __name__ == '__main__':
    dbname = r'C:\Users\jeanl\College\Blocks\Block 3\Mini Project\ClubHub\application\database\database.db'
    empty = ""
    with sqlite3.connect(dbname) as con:
        cursor = con.cursor()
        cursor.execute('select sql from sqlite_master')
        for r in cursor.fetchall():
            empty += f'\n{r[0]}' 
    cursor.close()
    f = open("application\database\output.sql", "a")
    f.write(empty)
    f.close()

