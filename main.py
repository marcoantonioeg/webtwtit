from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

URL = "https://nitter.net/NeonCypherX"
SEEN_TWEETS = set()

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    chromedriver_path = os.path.join(os.getcwd(), "chromedriver")
    service = Service(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_tweets(driver):
    driver.get(URL)
    time.sleep(3)

    tweets = driver.find_elements(By.CSS_SELECTOR, "div.timeline-item div.tweet-content")
    tweet_texts = []

    for tweet in tweets:
        text = tweet.text.strip()
        if text:
            tweet_texts.append(text)

    return tweet_texts

def monitor_tweets():
    driver = setup_driver()
    print("🔍 Monitoreando tuits en Nitter...\n")

    try:
        while True:
            tweets = get_tweets(driver)
            new_tweets = []

            for tweet in tweets:
                if tweet not in SEEN_TWEETS:
                    SEEN_TWEETS.add(tweet)
                    new_tweets.append(tweet)

            if new_tweets:
                print("\n🆕 Nuevos tuits encontrados:")
                for t in new_tweets:
                    print(f"- {t}")
            else:
                print("⏳ Sin nuevos tuits...")

            time.sleep(60)

    finally:
        driver.quit()

if __name__ == "__main__":
    monitor_tweets()
