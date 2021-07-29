import sqlite3

def  HandleScriptStart(sim):
    connection = sqlite3.connect(".\\data\\missions\\database\\\pyaquarium.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE if not exists fish (name TEXT, species TEXT, tank_number INTEGER)")
    cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
    cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
    rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    connection.commit()
    connection.close()
    print(rows)

def  HandleScriptTick(sim):
    pass