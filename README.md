# Repository Name: google-finance-watchlist-manager

Here's a README.md file for your GitHub repository:

```markdown
# Google Finance Watchlist Manager

An automated tool to add stocks to Google Finance watchlists using Selenium. This script helps investors efficiently manage their watchlists by automatically adding specified stocks to selected categories like "Watchlist", "Artificial Intelligence", and "Small Caps".

## 📋 Overview

Google Finance doesn't provide an official API for managing watchlists, making it tedious to add multiple stocks to different watchlist categories manually. This tool automates the process using Selenium WebDriver to simulate browser interactions, saving you time and effort.

## ✨ Features

- Automatically add stocks to multiple Google Finance watchlist categories
- Handles already checked/selected stocks intelligently
- Simulates natural human interaction to avoid detection
- Detailed progress logging and summary report
- Error handling and retry logic for reliability

## 🔧 Prerequisites

- Python 3.6+
- Chrome browser installed
- Google account with access to Google Finance

## 📦 Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/google-finance-watchlist-manager.git
   cd google-finance-watchlist-manager
   ```

2. Install required packages:
   ```
   pip install selenium webdriver-manager
   ```

## 🚀 Usage

1. Edit the `stocks` list in the script to include the stocks you want to add:
   ```python
   stocks = [
       ("ABSI", "NASDAQ"),
       ("APLD", "NASDAQ"),
       # Add more stocks as needed
   ]
   ```

2. Run the script:
   ```
   python add_stocks.py
   ```

3. When prompted, log in to your Google account manually in the browser window that opens.

4. Press Enter to begin the automation process.

5. The script will process each stock, adding it to the specified watchlist categories.

## ⚙️ How It Works

1. Opens Google Finance in a Chrome browser
2. Pauses for manual login (Google's CAPTCHA and security measures make automated login unreliable)
3. For each stock:
   - Navigates to the stock's page
   - Clicks the "Following" button
   - Checks or unchecks watchlist categories as needed
   - Waits between actions to avoid detection
4. Provides a summary of successfully added stocks and any failures

## ⚠️ Limitations

- The script requires manual login to avoid Google's security measures
- Web page structure changes by Google may require script updates
- Excessive usage might trigger Google's anti-automation measures

## 📝 Customization

To modify which watchlist categories are used, edit the `categories` list in the `add_stock_to_watchlist` function:

```python
categories = [
    {"name": "Watchlist", "uuid": "watchlist"},
    {"name": "Artificial Intelligence", "uuid": "a0fcb5d8-7398-4fba-87d0-be85faaedfaf"},
    {"name": "Small Caps", "uuid": "cd1bffe1-eaf7-4ed0-b1b6-a41bb9db9ac2"}
    # Add more categories as needed
]
```

## 🙏 Acknowledgements

- [Selenium](https://www.selenium.dev/) for browser automation capabilities
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) for simplifying driver management

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
```

Feel free to adjust the README to better match your preferences or add any additional sections you might need. The repository name "google-finance-watchlist-manager" clearly communicates the purpose of the project while remaining concise and professional.

Would you like me to make any changes to either the repository name or the README?
