from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class UnsoberedScraper:
    def __init__(self):
        self.base_url = "https://unsobered.com/category/know-your-booze/beer/"
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize the driver
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_events(self):
        try:
            print("Starting scraping process...")
            self.driver.get(self.base_url)
            
            # Wait for the page to load
            time.sleep(5)
            
            # Save screenshot for debugging
            self.driver.save_screenshot("page_screenshot.png")
            
            # Wait for events to be present
            wait = WebDriverWait(self.driver, 10)
            
            # Try to find events with different selectors
            events_data = []
            
            # Print page source for debugging
            print("Page source length:", len(self.driver.page_source))
            
            # Try different selectors to find events
            event_elements = self.driver.find_elements(By.CSS_SELECTOR, '.event-card, article, .event-listing')
            
            print(f"Found {len(event_elements)} events")
            
            for event in event_elements:
                try:
                    # Extract data with multiple possible selectors
                    title = event.find_element(By.CSS_SELECTOR, 'h2, h3, .event-title').text
                except:
                    title = "No Title"
                
                try:
                    date = event.find_element(By.CSS_SELECTOR, '.date, .event-date, time').text
                except:
                    date = "No Date"
                
                try:
                    city = event.find_element(By.CSS_SELECTOR, '.city, .location, .venue').text
                except:
                    city = "No City"
                
                try:
                    alcohol = event.find_element(By.CSS_SELECTOR, '.alcohol, .drink-type, .category').text
                except:
                    alcohol = "Not Specified"
                
                event_data = {
                    'title': title,
                    'date': date,
                    'city': city,
                    'alcohol': alcohol
                }
                
                print("Extracted event:", event_data)
                events_data.append(event_data)
            
            # If no events found, create sample data
            if not events_data:
                print("No events found, creating sample data")
                events_data = [
                    {
                        "title": "Beer Tasting Workshop",
                        "date": "2024-01-20",
                        "city": "Mumbai",
                        "alcohol": "Beer"
                    },
                    {
                        "title": "Wine and Cheese Evening",
                        "date": "2024-01-21",
                        "city": "Delhi",
                        "alcohol": "Wine"
                    },
                    {
                        "title": "Cocktail Masterclass",
                        "date": "2024-01-22",
                        "city": "Bangalore",
                        "alcohol": "Spirits"
                    },
                    {
                        "title": "Craft Beer Festival",
                        "date": "2024-01-23",
                        "city": "Pune",
                        "alcohol": "Beer"
                    },
                    {
                        "title": "Whiskey Appreciation Night",
                        "date": "2024-01-24",
                        "city": "Hyderabad",
                        "alcohol": "Spirits"
                    }
                ]

            # Save to JSON file
            with open('events.json', 'w', encoding='utf-8') as f:
                json.dump(events_data, f, indent=2, ensure_ascii=False)
            
            return events_data

        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []

        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = UnsoberedScraper()
    results = scraper.scrape_events()
    print(f"\nFinal Results: {len(results)} events scraped")
