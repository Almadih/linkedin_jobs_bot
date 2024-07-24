from db import get_all_queries,get_user_job_by_linkedin_id,add_user_job
from scraper import scrape_jobs
import logging



# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


async def send_job_message(bot,job,telegram_id):
    message = f'''
Job Title: {job['title']}\n

Location: {job['location']}\n

Company: {job['company']}\n

Time: {job['time']}\n

View Job:({job['url']})\n
'''
    await bot.send_message(telegram_id,message)

async def send_jobs(context):
    all_queries = get_all_queries()
    logging.info(f"Processing {len(all_queries)} queries")
    for query in all_queries:
        _,user_telegram_id,job_title,job_location = query
        logging.info(f"scraping ({job_title} - {job_location})")
        jobs = scrape_jobs(job_title,job_location)
        new_jobs = 0
        for job in jobs:
            if not get_user_job_by_linkedin_id(user_telegram_id,job['id']):
                await send_job_message(context.bot,job,user_telegram_id)
                new_jobs = new_jobs + 1
                add_user_job(user_telegram_id,job['id'])
        logging.info(f"found {new_jobs} new jobs")
