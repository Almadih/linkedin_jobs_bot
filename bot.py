import logging
from telegram.ext import  CommandHandler,Application
from telegram import Update
from db import insert_user,create_tables,get_all_queries,get_all_users,get_user_by_telegram_id,insert_user_query,get_user_queries,get_query,get_query_by_id,delete_query
import re
import os

import dotenv

dotenv.load_dotenv()

create_tables()

ADMIN_TELEGRAM_ID = os.environ['ADMIN_TELEGRAM_ID']

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Define the function to handle the /start command
async def start(update, context):
    user = update.message.from_user
    if not get_user_by_telegram_id(user.id):
        insert_user(user.id,user.username)
    await update.message.reply_text(f"Hello, {user.first_name}! I am your Telegram bot.")
async def number_of_users(update, context):
    user = update.message.from_user
    if user.id == int(ADMIN_TELEGRAM_ID):
       await update.message.reply_text(f"Total number of users ({len(get_all_users())})")

async def number_of_queries(update, context):
    user = update.message.from_user
    if user.id == int(ADMIN_TELEGRAM_ID):
       await update.message.reply_text(f"Total number of queries ({len(get_all_queries())})")

async def get_queries(update,context):
    user = update.message.from_user
    queries = get_user_queries(user.id)
    if len(queries) == 0:
         await update.message.reply_text("You don't have any active queries")
         return 
    
    for query in queries:
        id,job_title,job_location = query
        message = f"ID: {id}\nJob Title: {job_title}\nJob Location: {job_location}"
        await update.message.reply_text(message) 

async def cancel_query(update,context):
    user = update.message.from_user
    # Use re.match to check if the input matches the pattern
    match = re.match(r'^/cancel_query\s\d+$', update.message.text)
    if not match:
        await update.message.reply_text("Invalid input, your input should be in this format:\n/cancel_query ID")
        return

    query_id = update.message.text.split('/cancel_query')[1]
    if not get_query_by_id(int(query_id),user.id):
        await update.message.reply_text("Query was not found")
        return 
    
    delete_query(int(query_id),user.id)
    await update.message.reply_text("Query was canceled")

            
async def add_query(update,context):
    user = update.message.from_user
    if not bool(re.match(r"^/add_query\s+[a-zA-Z\s]+-\s+[a-zA-Z\s]+$", update.message.text.strip())):
        await update.message.reply_text("invalid input, your input should be in this format:\n/add_query job title - location")
        return 

    job_title,job_location = update.message.text.split('/add_query')[1].split('-')
    if get_query(user.id,job_title.strip(),job_location.strip()):
        await update.message.reply_text("The query already exists")
        return 

    insert_user_query(user.id,job_title.strip(),job_location.strip())
    await update.message.reply_text("A new query was added")


def main():
    BOT_TOKEN = os.environ['BOT_TOKEN']
    # Replace 'YOUR_API_TOKEN' with the token you obtained from BotFather
    
    # Get the dispatcher to register handlers
    dp = Application.builder().token(BOT_TOKEN).build()

    # Register the /start handler
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler('add_query',add_query))
    dp.add_handler(CommandHandler('queries',get_queries))
    dp.add_handler(CommandHandler('cancel_query',cancel_query))
    dp.add_handler(CommandHandler('num_users',number_of_users))
    dp.add_handler(CommandHandler('num_queries',number_of_queries))

    # Start the Bot
    dp.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
