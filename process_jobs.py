import xml.etree.ElementTree as ET
import requests
import json

# Fetch the XML feed
FEED_URL = "https://feeds.adzuna.co.uk/collegelife-dynamic/jobs_US_7977.xml.gz"
response = requests.get(FEED_URL)
xml_data = response.content

# Parse XML
root = ET.fromstring(xml_data)
jobs = []
for job in root.findall("job"):
    job_data = {
        "guid": job.find("guid").text,
        "title": job.find("title").text,
        "description": job.find("description").text,
        "url": job.find("url").text,
        "employer": job.find("employer").text,
        "category": job.find("category").text,
        "salary": job.find("salary").text,
        "location": f"{job.find('city').text}, {job.find('state').text}",
        "post_date": job.find("post_date").text,
    }
    jobs.append(job_data)

# Save to JSON
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("Jobs processed and saved to jobs.json")
