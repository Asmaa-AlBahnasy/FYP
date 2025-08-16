import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re  # To sanitize filenames

# Setup WebDriver.
driver = webdriver.Chrome()  # Replace with the correct WebDriver path if needed

# Base URL
BASE_URL = "https://www.lazurde.com/en-eg/gold-jewelry?view-all=true&sort=price-desc&page={}"

# Directory to save images
SAVE_DIR = "scrap1"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def save_image(img_url, description):
    """Download and save an image locally."""
    try:
        # Create a filename using the description
        filename = f"{sanitize_filename(description)}_{img_url.split('/')[-1].split('?')[0]}"
        filepath = os.path.join(SAVE_DIR, filename)

        # Check if the file already exists to avoid re-downloading
        if os.path.exists(filepath):
            print(f"Image already exists: {filepath}")
            return

        # Download the image
        img_data = requests.get(img_url).content
        with open(filepath, "wb") as file:
            file.write(img_data)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed to save {img_url}: {e}")

def scrape_with_selenium(page_number):
    """Scrape image URLs and descriptions using Selenium."""
    url = BASE_URL.format(page_number)
    print(f"Scraping page {page_number} with Selenium...")
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load the page

    # Parse the fully loaded HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find the main wrapper
    cards_wrapper = soup.find("div", {"id": "cards-wrapper", "class": "style_product-listing__cards__nQqDj"})
    if not cards_wrapper:
        print(f"No cards wrapper found on page {page_number}")
        return
    
    # Find all product cards
    product_cards = cards_wrapper.find_all("div", {"class": "show-arrow-on-hover ProductCard_product-card__wrapper__mBp2Z style_fade-in___WGWh"})
    print(f"Found {len(product_cards)} product cards on page {page_number}")
    
    # Loop through each product card
    for product_index, card in enumerate(product_cards, start=1):
        # Extract the description from the title div
        title_tag = card.find("div", {"class": "heading-c ProductCard_product-card__title__af0zt"})
        if title_tag:
            description = title_tag.text.strip()
        else:
            description = "unknown"

        # Find the image wrapper
        img_wrapper = card.find("div", {"class": "ProductCard_product-card__img-wrapper__4vDVQ"})
        if img_wrapper:
            # Find the first image inside the wrapper
            img_tag = img_wrapper.find("img")
            if img_tag:
                img_url = img_tag.get("src") or img_tag.get("data-src")
                if img_url and img_url.startswith("http"):
                    print(f"Image URL: {img_url}")  # Debug: Print the image URL
                    print(f"Description: {description}")  # Debug: Print the description
                    save_image(img_url, description)

# Run the scraper for all pages
for page in range(1, 22):  # Adjust the range based on the number of pages
    scrape_with_selenium(page)
    print(f"Finished scraping page {page}!")

# Close the browser when done
driver.quit()
