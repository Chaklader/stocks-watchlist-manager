from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# List of stocks to process (ticker, exchange)
stocks = [
    ("ABSI", "NASDAQ"), ("APLD", "NASDAQ"), ("ARBE", "NASDAQ"), ("BMR", "NASDAQ"),
    ("BBAI", "NYSE"), ("BTBT", "NASDAQ"), ("BZAI", "NASDAQ"), ("BLIN", "NASDAQ"),
    ("CRNC", "NASDAQ"), ("CEVA", "NASDAQ"), ("COHU", "NASDAQ"), ("DRIO", "NASDAQ"),
    ("DTSS", "NASDAQ"), ("DCBO", "NASDAQ"), ("DUOT", "NASDAQ"), ("EVLV", "NASDAQ"),
    ("FSLY", "NYSE"), ("GXAI", "NASDAQ"), ("HIVE", "NASDAQ"), ("INOD", "NASDAQ"),
    ("IVDA", "NASDAQ"), ("KSCP", "NASDAQ"), ("LTRN", "NASDAQ"), ("LTRX", "NASDAQ"),
    ("MFH", "NASDAQ"), ("MITK", "NASDAQ"), ("NNOX", "NASDAQ"), ("OTRK", "NASDAQ"),
    ("PDYN", "NASDAQ"), ("PENG", "NASDAQ"), ("PERI", "NASDAQ"), ("POET", "NASDAQ"),
    ("PRO", "NYSE"), ("RZLV", "NASDAQ"), ("RR", "NASDAQ"), ("RSKD", "NYSE"),
    ("SPAI", "NASDAQ"), ("SERV", "NASDAQ"), ("SES", "NYSE"), ("SLNH", "NASDAQ"),
    ("STGW", "NASDAQ"), ("IDAI", "NASDAQ"), ("TSSI", "NASDAQ"), ("VCIG", "NASDAQ"),
    ("VRNT", "NASDAQ"), ("WBUY", "NASDAQ"), ("XMTR", "NASDAQ"), ("ZEPP", "NYSE")
]

def setup_driver():
    """Set up the Chrome WebDriver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def add_stock_to_watchlist(driver, stock_info):
    """Add a stock to specified watchlists on Google Finance."""
    ticker, exchange = stock_info
    try:
        # Navigate to the stock's page
        url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
        driver.get(url)
        print(f"Navigated to {url}")
        
        # Wait for the "Following" button to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='button'][@jsname='pzCKEc']"))
        )
        
        # Click the "Following" button to open the dropdown
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][@jsname='pzCKEc']"))
        )
        driver.execute_script("arguments[0].click();", follow_button)
        print("Clicked 'Following' button")
        
        # Wait for the dropdown to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "XvhY1d"))
        )
        print("Dropdown is visible")
        
        # Add a short delay to ensure dropdown is fully loaded
        time.sleep(1)
        
        # Define watchlist categories with their UUIDs
        categories = {
            "Watchlist": "watchlist",
            "Artificial Intelligence": "a0fcb5d8-7398-4fba-87d0-be85faaedfaf",
            "Small Caps": "cd1bffe1-eaf7-4ed0-b1b6-a41bb9db9ac2"  # Fixed the UUID here
        }
        
        # Check each category's checkbox if not already checked
        for category_name, uuid in categories.items():
            try:
                checkbox_xpath = f"//div[@data-bundle-uuid='{uuid}']/ancestor::span[@role='menuitemcheckbox']"
                checkbox = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
                )
                
                # Check if already selected
                is_checked = checkbox.get_attribute("aria-checked") == "true"
                print(f"{category_name} is currently {'checked' if is_checked else 'unchecked'}")
                
                # Only click if not already checked
                if not is_checked:
                    driver.execute_script("arguments[0].click();", checkbox)
                    print(f"Checked {category_name}")
                    time.sleep(0.7)  # Give time for the check to register
                else:
                    print(f"{category_name} already checked, skipping")
                    
            except Exception as e:
                print(f"Couldn't process {category_name}: {str(e)}")
                continue
        
        # Close dropdown by clicking elsewhere (optional)
        try:
            driver.execute_script("document.body.click();")
            print("Closed dropdown")
        except:
            pass
            
        # Small delay before moving to next stock
        time.sleep(1.5)
        return True
        
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
        for stock_info in stocks:
            ticker, exchange = stock_info
            print(f"\nProcessing {ticker}:{exchange}...")
            if add_stock_to_watchlist(driver, stock_info):
                successful_adds.append(f"{ticker}:{exchange}")
                print(f"Successfully added {ticker}:{exchange}")
            else:
                failed_adds.append(f"{ticker}:{exchange}")
                print(f"Failed to add {ticker}:{exchange}")
            
            # Delay between stocks to avoid rate limiting
            time.sleep(2)
        
        # Display summary
        print("\n=== SUMMARY ===")
        print(f"Successfully added: {len(successful_adds)}")
        print(f"Failed to add: {len(failed_adds)}")
        
        if failed_adds:
            print("\nFailed stocks:")
            for stock in failed_adds:
                print(stock)
                
    except Exception as e:
        print(f"Major error occurred: {str(e)}")
    
    finally:
        input("\nPress Enter to close the browser...")
        driver.quit()

if __name__ == "__main__":
    main()