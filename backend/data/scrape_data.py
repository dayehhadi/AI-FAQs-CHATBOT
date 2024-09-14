import requests
from bs4 import BeautifulSoup
import json

def scrape_faq(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    faqs = []

    # Adjust the selectors based on the website's structure
    faq_items = soup.find_all('div', class_='faq-item')  # Example selector
    for item in faq_items:
        question = item.find('h3').text.strip()
        answer = item.find('p').text.strip()
        faqs.append({'question': question, 'answer': answer})
    return faqs

def scrape_course_catalog(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    courses = []

    # Adjust the selectors based on the website's structure
    course_items = soup.find_all('div', class_='course-item')  # Example selector
    for course in course_items:
        title = course.find('h4').text.strip()
        description = course.find('p').text.strip()
        courses.append({'title': title, 'description': description})
    return courses

def main():
    faq_url = 'https://www.aub.edu.lb/admissions/Pages/faq.aspx'  # Replace with actual URL

    faqs = scrape_faq(faq_url)

    # Save to JSON files
    with open('faqs.json', 'w') as f:
        json.dump(faqs, f, indent=4)

if __name__ == "__main__":
    main()
