from telegram import Bot,constants
from time import sleep
from db import get_all_queries,get_user_job_by_linkedin_id,add_user_job
from scraper import scrape_jobs
import logging
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()



# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
BOT_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(BOT_TOKEN)


SLEEPING_TIME = 30 * 60 
async def send_job_message(job,telegram_id):
    message = f'''
**Job Title**: {job['title']}

**Location:** {job['location']}

**Company:** {job['company']}

**Time:** {job['time']}

[View Job]({job['url']})
'''
    await bot.send_message(telegram_id,message,parse_mode=constants.ParseMode.MARKDOWN)

async def main():
    all_queries = get_all_queries()
    logging.info(f"Processing {len(all_queries)} queries")
    for query in all_queries:
        _,user_telegram_id,job_title,job_location = query
        logging.info(f"scraping ({job_title} - {job_location})")
        jobs = scrape_jobs(job_title,job_location)
        new_jobs = 0
        for job in jobs:
            if not get_user_job_by_linkedin_id(user_telegram_id,job['id']):
                await send_job_message(job,user_telegram_id)
                new_jobs = new_jobs + 1
                add_user_job(user_telegram_id,job['id'])
        logging.info(f"found {new_jobs} new jobs")


if __name__ == '__main__':
    while True:
        asyncio.run(main())
        sleep(SLEEPING_TIME)
