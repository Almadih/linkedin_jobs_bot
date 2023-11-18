import sqlite3
from google.cloud import firestore
from db import add_user_query

# Set up Google Cloud Firestore client
db = firestore.Client(project="attack-telegram-bot")

def migrate_users():
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('./database/database.db')
    cursor = sqlite_conn.cursor()

    # Fetch users from SQLite
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Migrate users to Firestore
    users_collection = db.collection('users')
    for user in users:
        user_data = {
            'telegram_id': int(user[1]),
            'name': user[2],
            "num_queries":0
        }
        users_collection.add(user_data)
        migrate_user_queries(user_data)

    # Close SQLite connection
    sqlite_conn.close()

def migrate_jobs():
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('./database/database.db')
    cursor = sqlite_conn.cursor()

    # Fetch jobs from SQLite
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    # Migrate jobs to Firestore
    jobs_collection = db.collection('jobs')
    for job in jobs:
        job_data = {
            'linkedin_job_id': job[1],
            'user_telegram_id': job[2]
        }
        jobs_collection.add(job_data)

    # Close SQLite connection
    sqlite_conn.close()

def migrate_user_queries(user):
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('./database/database.db')
    cursor = sqlite_conn.cursor()

    # Fetch queries from SQLite
    cursor.execute("SELECT * FROM queries where user_telegram_id = ?",[user['telegram_id']])
    queries = cursor.fetchall()


    for query in queries:
        print(query)
        add_user_query(query[1],query[2],query[3])

    # Close SQLite connection
    sqlite_conn.close()

# Execute migration functions
migrate_users()
# migrate_jobs()
