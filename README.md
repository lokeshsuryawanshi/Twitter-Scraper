# Twitter Scraper Without X API2

Robust Twitter scraping tool that retrieves tweets from a specific user over a date range, bypassing Twitter X API v2 restrictions. It processes tweets in batches, handles rate limits, and saves them in CSV format. It also generates a log file with real-time updates.

---

## Features
- Do not require API v2 credentials
- Fetch tweets within specific date ranges.
- Save data including tweet text, likes, retweets, and more in CSV files.
- Handles rate limits with automatic exponential backoff.
- Supports batch processing and saves output in CSV format.
- Allows fixed 180-day scraping windows for efficient performance.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lokeshsuryawanshi/Twitter-Scraper.git
   cd Twitter-Scraper
   
2. **Install required dependencies**

3. **Set Up cookies.json**:
- Log in to Twitter on your browser.
- Open Developer Tools (F12 or Ctrl+Shift+I/Cmd+Option+I).
- Go to the Application tab → Cookies → https://x.com or https://twitter.com.
- Export cookies as JSON or manually copy key-value pairs.
- Save as cookies.json in the project root directory.
- Adjust parameters in config.ini 

4. **Run the Scraper**:
python main.py
Replace parameters in the main() function to specify username, start date, and end date.

Notes -
Keep cookies.json secure. Add it to .gitignore to prevent accidental uploads.
Regenerate cookies if they expire or become invalid.












---
---

Keywords
Twitter scraper Python, fetch tweets without X API2, scrape Twitter data, Python tweet scraper, Twitter data extractor, export tweets CSV, bypass API limits, scrape tweets for free, Python Twitter scraper, no API required, tweet data analysis, Twitter scraper Python, Fetch tweets without API, Twitter scraping tool, Python tweet scraper, Download tweets CSV, Twitter data extractor, Scrape tweets using cookies, Twitter bypass API limits, Scraping tweets date range, Export tweets Python, Twitter bot automation, Python async scraper, Open-source tweet scraper, Twitter data analysis, How to scrape tweets without Twitter API, Best Python tools for Twitter scraping
Extract tweet data with cookies.json, Handle Twitter rate limits Python, Scraping Twitter using Python and cookies, "Get Twitter data for analysis", "Efficient tweet scraping solutions", "Retrieve tweets securely with Python", "Scrape tweets for research purposes", Twitter scraper Python without X API2, Fetch tweets without X API2, Scrape Twitter data without X API2, Python tweet scraper bypass X API2, Download tweets without X API2




