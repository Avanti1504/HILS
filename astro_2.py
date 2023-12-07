#!/usr/bin/env python3

import sys
from astrometry_client import Client  # Assuming the Astrometry.net client code is in astrometry_client.py
import requests
from bs4 import BeautifulSoup
from astrometry_client import Client

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def upload_image(apikey, server_url, image_path):
    # Create an Astrometry.net client
    client = Client(apiurl=server_url)

    try:
        # Login with the provided API key
        client.login(apikey)

        # Upload the image
        print(f"Uploading image: {image_path}")
        upload_result = client.upload(image_path, wait=True)

        # Check the status of the job
        job_id = upload_result.get('job_id')
        if job_id:
            print(f"Job submitted successfully with ID: {job_id}")

            # Wait for the job to complete
            print("Waiting for job completion...")
            while True:
                job_status = client.job_status(job_id, justdict=True)
                if job_status.get('status') == 'success':
                    print("Job completed successfully.")
                    break
                elif job_status.get('status') == 'failure':
                    print("Job failed. Check the Astrometry.net web interface for details.")
                    break

        else:
            print("Upload failed. Check the Astrometry.net web interface for details.")

    except Exception as e:
        print(f"Error: {e}")
#!/usr/bin/env python3


def scrape_results(apikey, server_url):
    # Use Selenium to navigate the Astrometry.net dashboard
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: Run Chrome in headless mode
    # options.binary_location = '/mnt/c/Users/DELL/Download/'  # Replace with the path to your ChromeDriver executable

    # driver = webdriver.Chrome(options=options)
    # Set up the Selenium WebDriver (you may need to adjust the path to the WebDriver executable)
    driver = webdriver.Chrome('/mnt/c/Users/DELL/Download/')

    # Get the Astrometry.net dashboard URL
    dashboard_url = f"{server_url}/dashboard/submissions"
    print(f"Scraping Astrometry.net dashboard: {dashboard_url}")

    try:
        # Open the dashboard URL
        driver.get(dashboard_url)

        # Wait for the page to load (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'joblist')))

        # Find all submission links using Selenium
        submission_links = driver.find_elements(By.XPATH, '//a[contains(@href, "status")]')

        # Iterate through each submission link
        for link in submission_links:
            submission_url = f"{server_url}{link.get_attribute('href')}"

            # Extract submission number from the URL
            submission_number = submission_url.split('/')[-1]

            print(f"Processing submission: {submission_number}")

            # Visit the submission status page
            status_page_url = f"{server_url}/status/{submission_number}"
            driver.get(status_page_url)

            # Wait for the status page to load (adjust the timeout as needed)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'id_checking')))
            
            # Find the "go to results page" link
            results_link = driver.find_element(By.XPATH, '//a[contains(text(), "go to results page")]')

            if results_link:
                results_url = f"{server_url}{results_link.get_attribute('href')}"

                # Fetch and print the content of the results page
                driver.get(results_url)
                print("Results Page Content:")
                print(driver.page_source)
            else:
                print("No 'go to results page' link found on the submission status page.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Your existing code remains unchanged

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python upload_and_scrape.py <API_KEY> <ASTROMETRY_NET_URL> <IMAGE_PATH>")
        sys.exit(1)

    api_key = sys.argv[1]
    server_url = sys.argv[2]
    image_path = sys.argv[3]

    upload_image(api_key, server_url, image_path)

    # Scrape the Astrometry.net dashboard for results
    scrape_results(api_key, server_url)
 


