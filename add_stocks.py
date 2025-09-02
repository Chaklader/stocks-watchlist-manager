from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import random

# Your list of stocks here
# stocks = [
#     ("HL", "NYSE"), ("EXK", "NYSE"), ("TRX", "NYSEAMERICAN"), ("GAU", "NYSEAMERICAN"),
#     ("BTG", "NYSEAMERICAN"), ("SAND", "NYSE"), ("UEC", "NYSEAMERICAN"), ("MUX", "NYSE"),
#     ("UROY", "NASDAQ"), ("ASM", "NYSEAMERICAN")
# ]

stocks = [
    ("SVM", "NYSEAMERICAN"), ("EXK", "NYSE"), ("BTG", "NYSEAMERICAN"), ("TGB", "NYSEAMERICAN"),
    ("DV", "TSX"), ("HL", "NYSE"), ("FSM", "NYSE"), ("SBSW", "NYSE"),
    ("CDE", "NYSE"), ("KGC", "NYSE")
]

def setup_driver():
    """Set up the Chrome WebDriver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_checkboxes(driver, max_wait=15):
    """Poll and wait until at least one checkbox is found or timeout reached"""
    print("Waiting for checkboxes to load...")
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            checkboxes = driver.find_elements(By.XPATH, "//span[@role='menuitemcheckbox']")
            if len(checkboxes) > 0:
                print(f"Found {len(checkboxes)} checkboxes after {time.time() - start_time:.1f} seconds")
                return True
        except:
            pass
        time.sleep(0.5)
    
    print(f"Warning: No checkboxes found after {max_wait} seconds")
    return False

def add_stock_to_watchlist(driver, stock_info):
    """Add a stock to specified watchlists on Google Finance."""
    ticker, exchange = stock_info
    try:
        # Navigate to the stock's page
        url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
        driver.get(url)
        print(f"Navigated to {url}")
        
        # Wait for page to fully load
        time.sleep(4)  # Increased wait time
        
        # Click the "Following" button
        follow_button = None
        try:
            # Try to find the button by different methods
            for xpath in [
                "//div[@role='button'][@jsname='pzCKEc']",
                "//div[@role='button']//*[text()='Following']/..",
                "//div[@role='button']//span[contains(text(), 'Following')]/.."
            ]:
                try:
                    follow_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    if follow_button:
                        break
                except:
                    continue
                    
            if follow_button:
                # Click using ActionChains
                ActionChains(driver).move_to_element(follow_button).click().perform()
                print("Clicked 'Following' button")
            else:
                print("Could not find 'Following' button")
                return False
        except Exception as e:
            print(f"Error clicking Following button: {str(e)}")
            return False
        
        # Wait for dropdown to appear
        try:
            dropdown = WebDriverWait(driver, 8).until(
                EC.visibility_of_any_elements_located((
                    By.XPATH, 
                    "//span[@role='menuitemcheckbox'] | //div[contains(@class, 'XvhY1d')] | //div[contains(@class, 'JAPqpe')]"
                ))
            )
            if dropdown:
                print("Dropdown is visible")
        except:
            print("Warning: Dropdown may not be visible")
            return False
        
        # Critical: Wait for checkboxes to load
        wait_for_checkboxes(driver)
        
        # Additional delay to ensure everything is properly rendered
        time.sleep(2)
        
        # Categories to check with their common attributes
        categories = [
            {"name": "Watchlist", "uuid": "watchlist"},
            {"name": "RES-NEW", "uuid": "a0fcb5d8-7398-4fba-87d0-be85faaedfaf"},
            {"name": "Mining", "uuid": "a0fcb5d8-7398-4fba-87d0-be85faaedfaf"},
        ]
        
        successful_categories = 0
        
        # Process each category
        for category in categories:
            category_name = category["name"]
            uuid = category["uuid"]
            
            try:
                # Try a simpler, more reliable approach to find checkboxes
                checkbox = None
                
                # Method 1: Find by class and text content
                try:
                    checkbox_elements = driver.find_elements(By.XPATH, "//span[@role='menuitemcheckbox']")
                    for element in checkbox_elements:
                        if category_name in element.text:
                            checkbox = element
                            break
                except:
                    pass
                
                # Method 2: Find by data-bundle-uuid
                if not checkbox:
                    try:
                        checkbox = driver.find_element(
                            By.XPATH, f"//div[@data-bundle-uuid='{uuid}']/ancestor::span[@role='menuitemcheckbox']"
                        )
                    except:
                        pass
                
                # Method 3: Find by text directly
                if not checkbox:
                    try:
                        checkbox = driver.find_element(
                            By.XPATH, f"//div[contains(text(), '{category_name}')]/ancestor::span[@role='menuitemcheckbox']"
                        )
                    except:
                        pass
                
                if not checkbox:
                    print(f"Could not locate {category_name} checkbox")
                    continue
                
                # Check if already selected
                try:
                    is_checked = checkbox.get_attribute("aria-checked") == "true"
                    print(f"{category_name} is currently {'checked' if is_checked else 'unchecked'}")
                    
                    if not is_checked:
                        # Scroll to make sure it's in view
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                        time.sleep(1)
                        
                        # Click with ActionChains - move to element with offset
                        actions = ActionChains(driver)
                        actions.move_to_element(checkbox).move_by_offset(5, 5).click().perform()
                        print(f"Clicked {category_name} checkbox")
                        
                        time.sleep(2)  # Wait for checkbox state to update
                    else:
                        print(f"{category_name} already checked, skipping")
                    
                    successful_categories += 1
                except Exception as e:
                    print(f"Error processing checkbox state for {category_name}: {str(e)}")
            except Exception as e:
                print(f"Error processing {category_name}: {str(e)}")
        
        # Try to close dropdown by clicking elsewhere
        try:
            # Click at coordinates away from the dropdown
            ActionChains(driver).move_by_offset(-300, -300).click().perform()
            print("Closed dropdown by clicking elsewhere")
        except:
            try:
                # Press ESC key as fallback
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                print("Closed dropdown with ESC key")
            except:
                print("Could not close dropdown, continuing anyway")
        
        # Success if we handled at least one category or if categories were already set
        return successful_categories > 0
        
    except Exception as e:
        print(f"Error adding {ticker}:{exchange}: {str(e)}")
        return False

def main():
    """Main function to execute the script."""
    driver = setup_driver()
    
    try:
        # Navigate to Google Finance for manual login
        driver.get("https://www.google.com/finance")
        print("\nPlease log in to Google manually now.")
        print("Once you're logged in and can see Google Finance, press Enter to continue...")
        input()
        
        successful_adds = []
        failed_adds = []
        
        # Process each stock
        for i, stock_info in enumerate(stocks):
            ticker, exchange = stock_info
            print(f"\nProcessing {i+1}/{len(stocks)}: {ticker}:{exchange}...")
            
            # Try twice for each stock
            success = False
            for attempt in range(2):
                if attempt > 0:
                    print(f"Retry attempt for {ticker}:{exchange}")
                
                if add_stock_to_watchlist(driver, stock_info):
                    successful_adds.append(f"{ticker}:{exchange}")
                    print(f"Successfully added {ticker}:{exchange}")
                    success = True
                    break
                
                # Wait before retry
                if not success and attempt < 1:
                    print(f"Waiting before retry...")
                    time.sleep(5)
            
            if not success:
                failed_adds.append(f"{ticker}:{exchange}")
                print(f"Failed to add {ticker}:{exchange}")
            
            # Add a delay between stocks
            if i < len(stocks) - 1:
                delay = random.uniform(3.0, 5.0)
                print(f"Waiting {delay:.1f} seconds before processing next stock...")
                time.sleep(delay)
        
        # Display summary
        print("\n=== SUMMARY ===")
        print(f"Successfully added: {len(successful_adds)} of {len(stocks)}")
        print(f"Failed to add: {len(failed_adds)}")
        
        if failed_adds:
            print("\nFailed stocks:")
            for stock in failed_adds:
                print(stock)
                
    except Exception as e:
        print(f"Major error occurred: {str(e)}")
    
    finally:
        print("\nPress Enter to close the browser...")
        input()
        driver.quit()

if __name__ == "__main__":
    main()