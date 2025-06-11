# --- UPDATED FILE: tasks/shopping_helper.py (with Robust Waits) ---

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait # <-- NEW IMPORT
from selenium.webdriver.support import expected_conditions as EC # <-- NEW IMPORT
from webdriver_manager.chrome import ChromeDriverManager

def search_shopping(platform, item_name):
    """
    Automates searching on a specified e-commerce or food delivery platform.
    Currently supports: Zomato.
    """
    platform = platform.lower()
    
    if platform != "zomato":
        return f"Sorry, I am currently configured to search only on Zomato, not {platform}."

    try:
        print(f"🖥️  Initiating search for '{item_name}' on {platform.title()}...")

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True) 
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        driver.get("https://www.zomato.com")
        
        # --- THE FIX: Replace time.sleep with a robust WebDriverWait ---
        # We will wait up to 10 seconds for the element to be clickable.
        print("INFO: Waiting for the Zomato search bar to become available...")
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Search for restaurant, cuisine or a dish')]"))
        )
        print("INFO: Search bar found!")
        # --- END OF THE FIX ---
        
        # Type the item name and press Enter
        search_box.send_keys(item_name)
        time.sleep(1) # a small pause
        search_box.send_keys(Keys.RETURN)

        return f"I have successfully searched for '{item_name}' on Zomato for you. The browser window is open."

    except Exception as e:
        error_message = f"I ran into an error while trying to search on Zomato: {e}"
        print(f"❌ {error_message}")
        return error_message