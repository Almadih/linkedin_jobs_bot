from db import get_all_queries,get_all_users,get_user_by_telegram_id,add_new_user,get_user_queries,get_user_query_by_id,delete_user_query,get_user_query,add_user_query
import re
from telegram import Update
from constants import ADMIN_CHAT_ID
from telegram.ext import (
    Application,
    CallbackContext,
    ExtBot,
)



class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates of type
    `WebhookUpdate`.
    """

    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        return super().from_update(update, application)

async def start(update: Update, context: CustomContext):
    user = update.message.from_user
    if not get_user_by_telegram_id(user.id):
        add_new_user(user.username,user.id)
    await update.message.reply_text(f"Hello, {user.first_name}! I am your Telegram bot.")

async def number_of_users(update: Update, context: CustomContext):
    user = update.message.from_user
    if user.id == int(ADMIN_CHAT_ID):
        await update.message.reply_text(f"Total number of users ({len(get_all_users())})")

async def number_of_queries(update: Update, context: CustomContext):
    user = update.message.from_user
    if user.id == int(ADMIN_CHAT_ID):
        await update.message.reply_text(f"Total number of queries ({len(get_all_queries())})")

async def get_queries(update: Update, context: CustomContext):
    user = update.message.from_user
    queries = get_user_queries(user.id)
    if len(queries) == 0:
         await update.message.reply_text("You don't have any active queries")
         return 
    
    for query in queries:
        message = f"ID: {query['id']}\nJob Title: {query['job_title']}\nJob Location: {query['job_location']}"
        await update.message.reply_text(message) 

async def cancel_query(update: Update, context: CustomContext):
    user = update.message.from_user
    # Use re.match to check if the input matches the pattern
    match = re.match(r'^/cancel_query\s\d+$', update.message.text)
    if not match:
        await update.message.reply_text("Invalid input, your input should be in this format:\n/cancel_query ID")
        return

    query_id = update.message.text.split('/cancel_query')[1]
    if not get_user_query_by_id(int(query_id),user.id):
        await update.message.reply_text("Query was not found")
        return 
    
    delete_user_query(int(query_id),user.id)
    await update.message.reply_text("Query was canceled")

            
async def add_query(update: Update, context: CustomContext):
    user = update.message.from_user
    if not bool(re.match(r"^/add_query\s+[a-zA-Z\s]+-\s+[a-zA-Z\s]+$", update.message.text.strip())):
        await update.message.reply_text("invalid input, your input should be in this format:\n/add_query job title - location")
        return 

    job_title,job_location = update.message.text.split('/add_query')[1].split('-')
    if get_user_query(user.id,job_title.strip(),job_location.strip()):
        await update.message.reply_text("The query already exists")
        return 

    add_user_query(user.id,job_title.strip(),job_location.strip())
    await update.message.reply_text("A new query was added")