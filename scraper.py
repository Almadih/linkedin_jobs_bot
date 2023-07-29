from bs4 import BeautifulSoup
import requests
from dateparser import parse
from datetime import datetime,timedelta




def is_job_time_greater_than_time_limit(human_readable_time,limit_in_hours=1):
    parsed_time = parse(human_readable_time)
    now = datetime.now()
    time_difference = abs(now - parsed_time)
    time_delta = timedelta(hours=limit_in_hours)
    return time_difference > time_delta

def scrape_jobs(job_title,location):
    time = 'r86400' #aka 24 hours
    geo_id = '104305776'
    base_url = f'https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}&geoId={geo_id}&f_TPR={time}&position=1&pageNum=0'
    response = requests.get(base_url)
    html = response.text
    bs = BeautifulSoup(html,'html.parser')

    jobs_section = bs.find('ul','jobs-search__results-list')
    jobs = jobs_section.find_all('li')
    results = []
    for job in jobs:
    # Extract job details
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        location = job.find('span', class_='job-search-card__location').text.strip()
        time_posted = job.select('time[class*="job-search-card__listdate"]')[0].text.strip()
        job_id = ''
        job_id_item = job.find('div', class_='base-card')
        if job_id_item:
            job_id = job_id_item['data-entity-urn'].split(':')[-1]
        else:
            job_id = job.find('a', class_='base-card')['data-entity-urn'].split(':')[-1]
        
        job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
        if not is_job_time_greater_than_time_limit(time_posted,1):
            results.append({'title':job_title,'company':company,'location':location,'time':time_posted,'url':job_url,'id':job_id})
    
    return results




