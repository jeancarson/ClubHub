import sqlite3 



if __name__ == '__main__':
    dbname = r"C:\Users\jeanl\College\Blocks\Block 3\Mini Project\ClubHub\app\application\database\database.db"
    empty = ""
    with sqlite3.connect(dbname) as con:
        cursor = con.cursor()
        cursor.execute('select sql from sqlite_master')
        for r in cursor.fetchall():
            empty += f'\n{r[0]}' 
    cursor.close()
    f = open(r"app\application\database\out.sql", "a")
    f.write(empty)
    f.close()

