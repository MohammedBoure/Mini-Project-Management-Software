import sqlite3

def create_db_and_table(DB_name):
    try:
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            Number INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PriceData (
            Number INTEGER PRIMARY KEY AUTOINCREMENT,
            Price REAL NOT NULL,
            Comment TEXT
        )
        '''
        )
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS CostsEmloye (
            Number INTEGER PRIMARY KEY AUTOINCREMENT,
            Price REAL NOT NULL,
            name TEXT
        )
        '''
        )

        conn.commit()
        return "Database and tables created (if not exists)."
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()


def add_employee(DB_name, name_employee):
    if name_employee and name_employee.strip():
        try:
            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO Employee (Name)
            VALUES (?)
            ''', (name_employee,))
            conn.commit()
            return "Employee added successfully."
        except sqlite3.Error as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()

def fetch_all_data(DB_name):
    try:
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM Employee')
        rows = cursor.fetchall()
        
        if rows:
            return rows
        else:
            return None
    except sqlite3.Error as e:
        return None
    finally:
        conn.close()           


def add_price_data(DB_name, price, comment=None):
    try:
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO PriceData (Price, Comment)
        VALUES (?, ?)
        ''', (price, comment))
        conn.commit()
        return "Price and comment added successfully."
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()

def fetch_all_price_data(DB_name):
    try:
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM PriceData')
        rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
    except sqlite3.Error as e:
        return None
    finally:
        conn.close()


def add_costs_emloye_data(DB_name, price, name=None):
    try:
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO CostsEmloye (Price, name)
        VALUES (?, ?)
        ''', (price, name))
        conn.commit()
        return "Price and comment added successfully."
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()

def fetch_all_costs_emloye_data(DB_name):
    try:
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM CostsEmloye')
        rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
    except sqlite3.Error as e:
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    #tests
    print(create_db_and_table('data.db'))
    print(fetch_all_price_data('data.db'))
    
    add_price_data('data.db',1000,"رمل")
    