from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from service.crawler.crawler_service import CrawlerInterface


class SeleniumCrawler(CrawlerInterface):
    def __init__(self,max_links_to_fetch=10,sleep_between_interactions=1):
        # Path to your ChromeDriver
        super().__init__()
        self.DRIVER_PATH = os.environ.get("DRIVER_PATH", "/usr/lib/chromium-browser/chromedriver")
        self.search_url = os.environ.get("Search_url","https://www.google.com/search?hl=en&tbm=isch&q=")
        self.max_links_to_fetch = max_links_to_fetch
        self.sleep_between_interactions = sleep_between_interactions
        self.service = Service(executable_path=self.DRIVER_PATH)
        self.options = webdriver.ChromeOptions()
        # Add a user-agent to mimic a real browser
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

    def crawl_base_on_query(self, query) -> list[str]:
        try:
            image_urls = set()
            self.wd = webdriver.Chrome(service=self.service, options=self.options)
            self.wd.get("https://www.google.com")

            search_box = WebDriverWait(self.wd, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='q']"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            self.wd.get(self.search_url + query)
            while len(image_urls) < self.max_links_to_fetch:

                thumbnails = self.wd.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")

                for thumbnail in thumbnails[len(image_urls):self.max_links_to_fetch]:
                    try:
                        src = thumbnail.get_attribute('src')

                        image_urls.add(src)
                        if len(image_urls) >= self.max_links_to_fetch:
                            break
                    except Exception as e:
                        print(f"Error fetching image URL: {e}")


                self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.sleep_between_interactions)


                if len(thumbnails) >= self.max_links_to_fetch:
                    break

            print(f"Found {len(image_urls)} image URLs.")
            return list(image_urls)
        except Exception as e:
            print(f"unexpected error: {e}")
            self.wd.quit()
            exit(1)

        finally:
            self.wd.quit()
