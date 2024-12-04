import abc
import base64
import aiohttp
import os
from PIL import Image
import io
import hashlib


class CrawlerInterface:
    def __init__(self):
        pass

    @abc.abstractmethod
    def crawl_base_on_query(self, query: str) -> list[str]:
        pass


class StorageInterface:
    def __init__(self):
        pass

    @abc.abstractmethod
    def save_image(self, address: list[str], src: list[str], query: str) -> None:
        pass


class CrawlerService:
    def __init__(self, crawler: CrawlerInterface, storage: StorageInterface):
        self.crawler = crawler
        self.storage = storage
        self.folder_path = os.environ.get('CRAWLER_FOLDER_PATH', "./result_images/")

    async def query(self, query: str) -> None:
        links = self.get_google_images_link(query)
        saved_address = []
        src_links = []
        for link in links:
            address = await self.save_image_files(link, query)
            if address is not None:
                saved_address.append(address)
                src_links.append(link)
        self.storage.save_image(saved_address, src_links, query)

    def get_google_images_link(self, query: str) -> list[str]:
        links = self.crawler.crawl_base_on_query(query)
        return links

    async def save_image_files(self, url: str, file_name: str) -> None | str:
        try:
            # Check if the URL is a base64-encoded string
            if url.startswith("data:image"):
                # Extract base64 string from the data URL
                base64_str = url.split(",", 1)[1]  # Split and get the base64 string
                image_content = base64.b64decode(base64_str)  # Decode the base64 string
            elif url.startswith("http"):
                # For regular HTTP URLs, download the image as before
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        image_content = await response.read()
            else:
                print(f"ERROR - Unsupported URL format: {url}")
                return None

        except Exception as e:
            print(f"ERROR - Could not download image: {url} - {e}")
            return None

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            folder_path = os.path.join(self.folder_path, file_name)
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=100)
            print(f"SUCCESS - saved {url} - as {file_path}")
            return file_path
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
            return None
