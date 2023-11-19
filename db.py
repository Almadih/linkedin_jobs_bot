from google.cloud import firestore
from datetime import datetime, timedelta

# Set up Google Cloud Firestore client
db = firestore.Client(project="attack-telegram-bot")

def get_user_job_by_linkedin_id(linkedin_job_id,user_telegram_id):
    jobs_collection = db.collection('jobs')
    jobs = jobs_collection.where('user_telegram_id','==',user_telegram_id).where('linkedin_job_id','==',linkedin_job_id).get()
    for job in jobs:
        return job.to_dict()

    return None
    
def add_user_job(user_telegram_id,linkedin_job_id):
    jobs_collection = db.collection('jobs')
    jobs_collection.add({"user_telegram_id":int(user_telegram_id),"linkedin_job_id":linkedin_job_id,"created_at":datetime.now()})

def get_user_queries(user_telegram_id):
    user = get_user_by_telegram_id(user_telegram_id)
    if not user:
        return False
    user_ref = db.collection('users').document(user.id)
    user_queries_collection = user_ref.collection('queries')
    user_queries = user_queries_collection.stream()
    queries = [query.to_dict() for query in user_queries]
    for query in queries:
        query.update({"user_telegram_id":user.to_dict()['telegram_id']})
    
    return queries
    

def add_user_query(user_telegram_id,job_title,job_location):
    user = get_user_by_telegram_id(user_telegram_id)
    if not user:
        return False
    user_ref = db.collection('users').document(user.id)
    user_queries_collection = user_ref.collection('queries')
    new_query_id = user.to_dict()['num_queries'] + 1
    user_queries_collection.add({"id":new_query_id,"job_title":job_title,"job_location":job_location})
    user_ref.update({"num_queries":new_query_id})

def delete_user_query(id,user_telegram_id):
    user = get_user_by_telegram_id(user_telegram_id)
    if not user:
        return False
    
    user_ref = db.collection('users').document(user.id)
    user_queries_collection = user_ref.collection('queries')
    user_queries = user_queries_collection.where('id','==',id).limit(1).get()
    for query in user_queries:
        user_ref.collection('queries').document(query.id).delete()

def get_user_query(user_telegram_id,job_title,job_location):
    user = get_user_by_telegram_id(user_telegram_id)
    if not user:
        return False
    
    user_ref = db.collection('users').document(user.id)
    user_queries_collection = user_ref.collection('queries')
    user_queries = user_queries_collection.where('job_title','==',job_title).where('job_location','==',job_location).limit(1).get()
    for query in user_queries:
        return query
    return None
    
def get_user_query_by_id(id,user_telegram_id):
    user = get_user_by_telegram_id(user_telegram_id)
    if not user:
        return False
    
    user_ref = db.collection('users').document(user.id)
    user_queries_collection = user_ref.collection('queries')
    user_queries = user_queries_collection.where('id','==',id).limit(1).get()
    for query in user_queries:
        return query
    return None
    
def get_all_queries():
    total_queries = []
    for user in get_all_users():
        total_queries.extend(get_user_queries(user['telegram_id']))
    return total_queries

def add_new_user(name,telegram_id):
    users_collection = db.collection('users')
    users_collection.add({"name":name,"telegram_id":telegram_id,"num_queries":0})

def get_user_by_telegram_id(telegram_id):
    users_collection = db.collection('users')
    users = users_collection.where('telegram_id','==',telegram_id).limit(1).get()
    for user in users:
        return user
    return None


def get_all_users():
    users_collection = db.collection('users')
    users = users_collection.stream()
    return [user.to_dict() for user in users]

def delete_old_job_documents():
    jobs_collection = db.collection('jobs')
    cutoff_datetime = datetime.now() - timedelta(hours=10)
    jobs = jobs_collection.where('created_at','<=',cutoff_datetime)

    # Get the documents
    docs_to_delete = jobs.stream()

    # Delete the documents
    for doc in docs_to_delete:
        doc.reference.delete()