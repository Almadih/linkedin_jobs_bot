import sqlite3

# Function to create the tables if they don't exist
def create_tables():
    connection = create_connection()
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id TEXT NOT NULL,
                name TEXT NOT NULL
            )
        ''')
        connection.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                linkedin_job_id TEXT NOT NULL,
                user_telegram_id INTEGER
            )
        ''')

        connection.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY,
            user_telegram_id INTEGER,
            job_title TEXT,
            job_location TEXT
        )
        ''')
    connection.close()
def get_user_job_by_linkedin_id(telegram_id,linkedin_id):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
        SELECT * FROM jobs where user_telegram_id = ? and linkedin_job_id = ?
        ''',(telegram_id,linkedin_id,))
        return cursor.fetchall()
    
def add_user_job(telegram_id,linkedin_id):
    connection = create_connection()
    with connection:
        connection.execute('''
        INSERT INTO jobs (linkedin_job_id,user_telegram_id) values (?,?)
        ''',(linkedin_id,telegram_id,))
    connection.close()

def get_user_queries(telegram_id):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
        SELECT id,job_title,job_location from queries where user_telegram_id = ?
        ''',(telegram_id,))
        return cursor.fetchall()
    

def insert_user_query(telegram_id,job_title,job_location):
    connection = create_connection()
    with connection:
        connection.execute('''
        INSERT INTO queries (user_telegram_id,job_title,job_location) values (?,?,?)
        ''',(telegram_id,job_title,job_location,))
def delete_query(id,telegram_id):
    connection = create_connection()
    with connection:
        connection.execute('''
        DELETE FROM queries where id = ? and user_telegram_id = ?
        ''',(id,telegram_id,))
def get_query(telegram_id,job_title,job_location):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
        SELECT * FROM queries where user_telegram_id = ? and job_title = ? and job_location = ?
        ''',(telegram_id,job_title,job_location,))
        return cursor.fetchone()
    
def get_query_by_id(id,telegram_id):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
        SELECT * FROM queries where id = ? and user_telegram_id = ?
        ''',(id,telegram_id,))
        return cursor.fetchone()
    
def get_all_queries():
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
        SELECT * FROM queries
        ''',())
        return cursor.fetchall()
# Function to insert a new user into the users table
def insert_user(telegram_id,name):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
            INSERT INTO users (telegram_id,name) VALUES (?,?)
        ''', (telegram_id,name))

    connection.close()

def get_user_by_telegram_id(telegram_id):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
            SELECT * FROM users WHERE telegram_id = ?
        ''',(telegram_id,))
        return cursor.fetchone()

# Function to insert a new job into the jobs table associated with a user
def insert_job(linkedin_job_id, user_id):
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
            INSERT INTO jobs (linkedin_job_id,user_telegram_id) VALUES (?,?)
        ''', (linkedin_job_id,user_id,))

    connection.close()

def get_all_users():
    connection = create_connection()
    with connection:
        cursor = connection.execute('''
            SELECT * FROM users
        ''',())
        return cursor.fetchall()


def create_connection():
    db_path = "./database/database.db"
    return sqlite3.connect(db_path)

