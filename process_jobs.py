import requests
import gzip
import xml.etree.ElementTree as ET

try:
    # Fetch the compressed XML feed
    url = "https://feeds.adzuna.co.uk/collegelife-dynamic/jobs_US_7977.xml.gz"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues

    # Decompress the Gzipped content
    compressed_data = response.content  # Use .content to get raw bytes
    xml_data = gzip.decompress(compressed_data).decode("utf-8")
    print("Fetched and decompressed XML data successfully.")

    # Remove BOM if present
    xml_data = xml_data.lstrip("\ufeff")

    # Parse the XML
    root = ET.fromstring(xml_data)
    print("Parsed XML successfully.")

    # Process jobs
    jobs = []
    for job in root.findall("job"):
        title = job.find("title").text
        description = job.find("description").text
        company = job.find("employer").text
        location = f"{job.find('city').text}, {job.find('state').text}, {job.find('country').text}"
        url = job.find("url").text

        jobs.append({
            "title": title,
            "description": description,
            "company": company,
            "location": location,
            "url": url
        })

    # Write jobs to a JSON file
    import json
    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

    print("Jobs processed and saved to jobs.json successfully.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the XML feed: {e}")
except gzip.BadGzipFile as e:
    print(f"Error decompressing the XML feed: {e}")
except ET.ParseError as e:
    print(f"Error parsing the XML feed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
