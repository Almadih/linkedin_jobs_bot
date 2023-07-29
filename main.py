from telegram import Bot
from time import sleep
from db import get_all_queries,get_user_job_by_linkedin_id,add_user_job
from scraper import scrape_jobs
import logging
import os


# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
BOT_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(BOT_TOKEN)


SLEEPING_TIME = 30 * 60 
def send_job_message(job,telegram_id):
    message = f"Job Title: {job['title']}\nLocation: {job['location']}\nCompany: {job['company']}\nTime: {job['time']}\nURL: {job['url']}"
    bot.send_message(telegram_id,message)

def main():
    all_queries = get_all_queries()
    logging.info(f"Processing {len(all_queries)} queries")
    for query in all_queries:
        _,user_telegram_id,job_title,job_location = query
        jobs = scrape_jobs(job_title,job_location)
        for job in jobs:
            if not get_user_job_by_linkedin_id(user_telegram_id,job['id']):
                send_job_message(job,user_telegram_id)
                add_user_job(user_telegram_id,job['id'])


if __name__ == '__main__':
    while True:
        main()
        sleep(SLEEPING_TIME)
