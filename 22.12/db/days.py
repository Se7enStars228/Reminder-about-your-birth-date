import sqlite3

def table():
    db = sqlite3.connect('imdays.db')
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS days (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        date TEXT NOT NULL
    )""")
    db.commit()
    db.close()

def add_date(user_id, name, surname, date):
    db = sqlite3.connect('imdays.db')
    c = db.cursor()
    c.execute("INSERT INTO days (user_id, name, surname, date) VALUES (? ,?, ?, ?)", (user_id ,name, surname, date))
    db.commit()
    db.close()
    
def delete_date(user_id, name, surname):
    db = sqlite3.connect('imdays.db')
    c = db.cursor()
    c.execute("DELETE FROM days WHERE user_id = ? AND name = ? AND surname = ?", (user_id, name, surname))
    db.commit()
    db.close()
    
def update_all(user_id, name, surname, date):
    db = sqlite3.connect('imdays.db')
    c = db.cursor()
    c.execute("UPDATE days SET date = ? WHERE user_id = ? AND name = ? AND surname = ?", (user_id, date, name, surname))
    db.commit()
    db.close()

def view_all(user_id):
    db = sqlite3.connect('imdays.db')
    c = db.cursor()
    c.execute("SELECT name, surname, date FROM days WHERE user_id = ?", (user_id,))
    data = c.fetchall()
    db.close()
    return data