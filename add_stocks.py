from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Updated stock list with exchange information
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
    ticker, exchange = stock_info
    try:
        # Go to stock page
        url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
        driver.get(url)
        time.sleep(3)
        
        # Find and click Follow button
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][@jsname='pzCKEc']"))
        )
        driver.execute_script("arguments[0].click();", follow_button)
        time.sleep(1)
        
        # Select categories
        categories = {
            "Watchlist": "watchlist",
            "Artificial Intelligence": "a0fcb5d8-7398-4fba-87d0-be85faaedfaf",
            "Small Caps": "cd1bffe1-eaf7-4ed0-b1b6-a41bb9db9ac2"
        }
        
        for category_name, uuid in categories.items():
            try:
                checkbox = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        f"//div[@data-bundle-uuid='{uuid}']/ancestor::span[@role='menuitemcheckbox']"))
                )
                if checkbox.get_attribute("aria-checked") != "true":
                    driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.5)
            except:
                print(f"Couldn't add to {category_name}")
        
        # Click Done
        done_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Done']"))
        )
        driver.execute_script("arguments[0].click();", done_button)
        time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"Error adding {ticker}:{exchange}: {str(e)}")
        return False
    
    
# def add_stock_to_watchlist(driver, stock_info):
#     ticker, exchange = stock_info
#     try:
#         # Directly navigate to the stock's page
#         url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
#         driver.get(url)
#         time.sleep(2)
        
#         # Find and click the Follow button
#         follow_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Follow') or contains(@aria-label, 'Following')]"))
#         )
        
#         # If not already following, click to follow
#         if "Following" not in follow_button.get_attribute("aria-label"):
#             follow_button.click()
#             time.sleep(1)
        
#         # Click again to open categories
#         follow_button.click()
#         time.sleep(1)
        
#         # Add to categories
#         categories = ["Watchlist", "Artificial Intelligence", "Small Caps"]
#         for category in categories:
#             try:
#                 category_elem = WebDriverWait(driver, 5).until(
#                     EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{category}']/ancestor::div[@role='checkbox']"))
#                 )
#                 if category_elem.get_attribute("aria-checked") != "true":
#                     category_elem.click()
#                 time.sleep(0.5)
#             except Exception as e:
#                 print(f"Could not add to {category}: {str(e)}")
        
#         # Click Done
#         done_button = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[text()='Done']"))
#         )
#         done_button.click()
#         time.sleep(1)
        
#         return True
#     except Exception as e:
#         print(f"Error adding {ticker}:{exchange}: {str(e)}")
#         return False

def main():
    driver = setup_driver()
    
    try:
        # Go to Google Finance
        driver.get("https://www.google.com/finance")
        print("\nPlease log in to Google manually now.")
        print("Once you're logged in and can see Google Finance, press Enter to continue...")
        input()
        
        successful_adds = []
        failed_adds = []
        
        for stock_info in stocks:
            ticker, exchange = stock_info
            print(f"\nProcessing {ticker}:{exchange}...")
            if add_stock_to_watchlist(driver, stock_info):
                successful_adds.append(f"{ticker}:{exchange}")
                print(f"Successfully added {ticker}:{exchange}")
            else:
                failed_adds.append(f"{ticker}:{exchange}")
                print(f"Failed to add {ticker}:{exchange}")
            
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