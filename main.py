import uvicorn

from crawler.selenium import SeleniumCrawler
from delivery.cli.app import CliApp
from delivery.httpserver.main import FastHttpServer
from service.crawler.crawler_service import CrawlerService
from storage.postgresql.image.main import SaveImage
from storage.postgresql.main import PostgreSQL
import asyncio


def main():
    # cli_app = CliApp()
    storage = PostgreSQL()
    image_storage = SaveImage(db=storage.get_db())
    crawler_svc = CrawlerService(crawler=SeleniumCrawler(), storage=image_storage)
    http_server = FastHttpServer(crawler_svc=crawler_svc)
    http_server.start()


if __name__ == '__main__':
    main()
