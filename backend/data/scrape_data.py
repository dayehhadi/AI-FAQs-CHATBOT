from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

def scrape_faq_with_selenium_and_bs(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)

        # Wait a bit longer to ensure all content has loaded
        time.sleep(10)  # Adjust this as needed, up to 30 seconds

        # Print the page source for inspection
        page_source = driver.page_source
        print(page_source)  # Review this to ensure the content is present
        
        # Use WebDriverWait to wait until the accordion groups are loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'accordion-toggle'))
        )

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Quit the driver
        driver.quit()

    # Continue with BeautifulSoup parsing
    soup = BeautifulSoup(page_source, 'html.parser')
    faqs = []

    accordion_groups = soup.find_all('div', class_='panel accordion-group')
    print(f"Found {len(accordion_groups)} accordion groups.")

    for group in accordion_groups:
        question_tag = group.find('a', class_='accordion-toggle')
        answer_tag = group.find('div', class_='accordion-body collapse')

        if question_tag and answer_tag:
            question = question_tag.get_text(strip=True)
            answer = answer_tag.get_text(strip=True)
            faqs.append({
                'question': question,
                'answer': answer
            })

    return faqs

def main():
    faq_url = 'https://www.aub.edu.lb/admissions/Pages/faq.aspx'
    faqs = scrape_faq_with_selenium_and_bs(faq_url)

    if not faqs:
        print("No FAQs found. Please check the HTML structure and update the selectors accordingly.")
        return

    # Save the scraped FAQs to a JSON file
    with open('faqs.json', 'w', encoding='utf-8') as f:
        json.dump(faqs, f, indent=4, ensure_ascii=False)

    print(f"Scraped {len(faqs)} FAQs and saved to faqs.json")

if __name__ == "__main__":
    main()
