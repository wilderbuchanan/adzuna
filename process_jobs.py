import requests
import gzip
import xml.etree.ElementTree as ET
import json

try:
    # Fetch the compressed XML feed
    url = "https://feeds.adzuna.co.uk/collegelife-dynamic/jobs_US_7977.xml.gz"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues

    # Debug: Check response status and content length
    print(f"Response status code: {response.status_code}")
    print(f"Response content length: {len(response.content)} bytes")

    if response.status_code != 200 or len(response.content) == 0:
        print("Error: Invalid response received. Exiting.")
        exit(1)

    # Decompress the Gzipped content
    try:
        xml_data = gzip.decompress(response.content).decode("utf-8")
        print("Fetched and decompressed XML data successfully.")
    except gzip.BadGzipFile as e:
        print(f"Error decompressing XML data: {e}")
        exit(1)

    # Debug: Print decompressed XML data
    print("Debug: Fetched XML data (first 500 characters):")
    print(xml_data[:500])

    # Parse the XML
    try:
        root = ET.fromstring(xml_data)
        print("Parsed XML successfully.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print("Raw XML data:", xml_data[:500])  # Print partial data for debugging
        exit(1)

    # Process jobs
    jobs = []
    for job in root.findall("job"):
        try:
            title = job.find("title").text
            description = job.find("description").text
            company = job.find("employer").text
            location = f"{job.find('city').text}, {job.find('state').text}, {job.find('country').text}"
            url = job.find("url").text

            # Add UTM parameters to the URL
            utm_url = f"{url}?utm_source=adzuna&utm_medium=website&utm_campaign=zuna-listing"

            # Determine tags based on title
            tags = []
            if "mechanical" in title.lower():
                tags.append("mechanical engineering")
            if "internship" in title.lower():
                tags.append("internship")
            if "co-op" in title.lower():
                tags.append("co-op")
            if "manufacturing" in title.lower():
                tags.append("manufacturing")
            if "quality" in title.lower():
                tags.append("quality")

            # Add job data to the list
            jobs.append({
                "title": title,
                "description": description,
                "company": company,
                "location": location,
                "url": utm_url,
                "tags": tags,
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Tesla_logo.png/640px-Tesla_logo.png"
            })
        except AttributeError as e:
            print(f"Warning: Missing data in job entry: {e}")
            continue

    # Write jobs to a JSON file
    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

    print("Jobs processed and saved to jobs.json successfully.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the XML feed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
