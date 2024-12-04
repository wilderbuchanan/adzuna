import requests
import gzip
import xml.etree.ElementTree as ET
import json

try:
    # Fetch the compressed XML feed
    url = "https://feeds.adzuna.co.uk/collegelife-dynamic/jobs_US_7977.xml.gz"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues

    # Check for valid response content
    if not response.content:
        print("Error: Received empty response from the server.")
        exit(1)

    # Decompress the Gzipped content
    compressed_data = response.content  # Use .content to get raw bytes
    try:
        xml_data = gzip.decompress(compressed_data).decode("utf-8")
        print("Fetched and decompressed XML data successfully.")
    except gzip.BadGzipFile as e:
        print(f"Error decompressing XML data: {e}")
        exit(1)

    # Debug: Print the first 500 characters of XML data
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

            jobs.append({
                "title": title,
                "description": description,
                "company": company,
                "location": location,
                "url": url
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
