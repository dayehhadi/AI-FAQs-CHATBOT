from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import os

def scrape_faq_with_selenium_and_bs(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)

        # Wait a bit longer to ensure all content has loaded
        time.sleep(3)  # Adjust this as needed, up to 30 seconds

        # Use WebDriverWait to wait until the accordion groups are loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'accordion-toggle'))
        )

        # Get the page source
        page_source = driver.page_source

    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return []

    finally:
        # Quit the driver
        driver.quit()

    # Continue with BeautifulSoup parsing
    soup = BeautifulSoup(page_source, 'html.parser')
    faqs = []

    accordion_groups = soup.find_all('div', class_='panel accordion-group')
    print(f"Found {len(accordion_groups)} accordion groups on {url}.")

    for group in accordion_groups:
        question_tag = group.find('a', class_='accordion-toggle')
        answer_tag = group.find('div', class_='accordion-body collapse')

        if question_tag and answer_tag:
            question = question_tag.get_text(strip=True)
            answer = answer_tag.get_text(strip=True)
            if question and answer:  # Ensure both question and answer are present
                faqs.append({
                    'question': question,
                    'answer': answer
                })

    return faqs

def save_faqs_to_json(faqs, filename='faqs.json'):
    """Append scraped FAQs to an existing JSON file."""
    
    # Check if the JSON file already exists
    if os.path.exists(filename):
        # Load existing data
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []  # Ensure it's a list
            except json.JSONDecodeError:
                existing_data = []  # Handle empty or malformed JSON files
    else:
        existing_data = []  # File does not exist, start with an empty list

    # Append new FAQs to the existing data
    existing_data.extend(faqs)

    # Save the updated data back to the JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"Appended {len(faqs)} FAQs to {filename}")

def main():
    faq_urls = [
        'https://www.aub.edu.lb/admissions/Pages/faq.aspx',
        'https://www.aub.edu.lb/graduatecouncil/Pages/faq.aspx'
        ,'https://www.aub.edu.lb/Registrar/Pages/faq.aspx',
        'https://www.aub.edu.lb/provost/Pages/FAQ-students.aspx',
        'https://www.aub.edu.lb/SAO/Pages/WSP-faq.aspx'
    ]

    all_faqs = []
    for url in faq_urls:
        faqs = scrape_faq_with_selenium_and_bs(url)
        if faqs:
            all_faqs.extend(faqs)

    if not all_faqs:
        print("No FAQs found. Please check the HTML structure and update the selectors accordingly.")
        return

    # Save the scraped FAQs to a JSON file
    save_faqs_to_json(all_faqs, 'faqs.json')

if __name__ == "__main__":
    main()
