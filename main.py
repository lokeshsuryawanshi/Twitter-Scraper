from twikit import Client, TooManyRequests
import time
from datetime import datetime, timedelta
import csv
from configparser import ConfigParser
from random import randint
import os
import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TwitterScraper:
    def __init__(self):
        self.client = None
        self.config = None
        self.total_tweets = 0
        self.min_window_days = 180  # Changed to 180 days
        self.max_window_days = 180  # Changed to match min_window_days
        self.window_expansion_factor = 1  # No expansion needed since using fixed window
        
    async def setup(self):
        """Initialize the Twitter client and configuration"""
        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.client = Client()
        self.client.load_cookies('cookies.json')
        
    def setup_csv(self, filename, headers=None):
        """Create a new CSV file with headers if it doesn't exist"""
        if headers is None:
            headers = ['Tweet_ID', 'Tweet_count', 'Username', 'Text', 'Created_At', 
                      'Retweets', 'Likes', 'Reply_Count', 'Quote_Count']
            
        if not os.path.exists(filename):
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

    async def handle_rate_limit(self, e):
        """Handle rate limit exceptions with exponential backoff"""
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        wait_time = (rate_limit_reset - datetime.now()).total_seconds() + 5
        
        logger.warning(f'Rate limit reached. Waiting {wait_time} seconds until {rate_limit_reset}')
        await asyncio.sleep(wait_time)

    def build_query(self, username, start_date, end_date):
        """Build an optimized search query based on documentation guidelines"""
        return (
            f'from:{username} '
            f'since:{start_date} '
            f'until:{end_date}'
            # Removed -is:retweet to include retweets
        )

    async def check_activity(self, username, start_date, end_date):
        """Quick check if there are any tweets in the period"""
        query = self.build_query(username, start_date, end_date)
        try:
            tweets = await self.client.search_tweet(query, product='Latest', count=1)
            return bool(tweets)
        except Exception as e:
            logger.warning(f'Error checking activity: {str(e)}')
            return False

    async def process_tweets_batch(self, tweets, filename):
        """Process and save a batch of tweets"""
        count = 0
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            for tweet in tweets:
                count += 1
                tweet_data = [
                    tweet.id,
                    self.total_tweets + count,
                    tweet.user.name,
                    tweet.text,
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count,
                    getattr(tweet, 'reply_count', 0),
                    getattr(tweet, 'quote_count', 0)
                ]
                writer.writerow(tweet_data)
        
        self.total_tweets += count
        logger.info(f'Processed {count} tweets. Total tweets: {self.total_tweets}')
        return count

    async def get_tweets_for_period(self, username, start_date, end_date, filename):
        """Get tweets for a specific date range with improved pagination and error handling"""
        query = self.build_query(username, start_date, end_date)
        logger.info(f'Getting tweets for period {start_date} to {end_date}')
        
        tweets = None
        tweet_count = 0
        retry_count = 0
        max_retries = 5
        
        while True:
            try:
                if tweets is None:
                    tweets = await self.client.search_tweet(
                        query,
                        product='Latest',
                        count=100
                    )
                else:
                    wait_time = randint(3, 7)
                    await asyncio.sleep(wait_time)
                    tweets = await tweets.next()
                
                if not tweets:
                    break
                
                tweet_count += await self.process_tweets_batch(tweets, filename)
                retry_count = 0
                
            except TooManyRequests as e:
                await self.handle_rate_limit(e)
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error(f'Max retries reached for period {start_date} to {end_date}. Error: {str(e)}')
                    break
                    
                wait_time = 2 ** retry_count + randint(1, 5)
                logger.warning(f'Error occurred: {str(e)}. Retrying in {wait_time} seconds...')
                await asyncio.sleep(wait_time)
        
        return tweet_count

    async def run(self, username, start_date, end_date):
        """Main execution method with fixed 180-day window size"""
        await self.setup()
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        current_start = start_dt
        
        while current_start < end_dt:
            # Calculate current window end date
            current_end = min(current_start + timedelta(days=self.min_window_days), end_dt)
            
            # Format dates for query
            start_str = current_start.strftime('%Y-%m-%d')
            end_str = current_end.strftime('%Y-%m-%d')
            
            # Process the window
            filename = f'tweets_{start_str}_{end_str}.csv'
            self.setup_csv(filename)
            
            try:
                period_tweets = await self.get_tweets_for_period(
                    username,
                    start_str,
                    end_str,
                    filename
                )
                
                logger.info(f'Completed period {start_str} to {end_str}. Retrieved {period_tweets} tweets.')
                
            except Exception as e:
                logger.error(f'Error processing period {start_str} to {end_str}: {str(e)}')
                raise
            
            # Move to next period
            current_start = current_end + timedelta(days=1)
            
            # Add random delay between periods
            await asyncio.sleep(randint(5, 10))

async def main():
    scraper = TwitterScraper()
    try:
        await scraper.run(
            username='elonmusk',
            start_date='2022-01-01',
            end_date=datetime.now().strftime('%Y-%m-%d')
        )
        logger.info(f'Scraping completed! Total tweets retrieved: {scraper.total_tweets}')
    except Exception as e:
        logger.error(f'Scraping failed: {str(e)}')

if __name__ == "__main__":
    asyncio.run(main())