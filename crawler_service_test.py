import pytest
from unittest.mock import MagicMock
from service.crawler.crawler_service import CrawlerService
from service.crawler.crawler_service import StorageInterface
from crawler.selenium import SeleniumCrawler


@pytest.fixture
def mock_storage():
    return MagicMock(StorageInterface)


@pytest.fixture
def mock_crawler():
    return MagicMock(SeleniumCrawler)


@pytest.fixture
def crawler_service(mock_crawler, mock_storage):
    return CrawlerService(crawler=mock_crawler, storage=mock_storage)

@pytest.mark.asyncio
async def test_query(crawler_service, mock_crawler, mock_storage):

    mock_crawler.crawl_base_on_query.return_value = ["https://picsum.photos/id/237/200/300", "https://picsum.photos/seed/picsum/200/300"]
    await crawler_service.query("test query")
    mock_crawler.crawl_base_on_query.assert_called_once_with("test query")
    mock_storage.save_image.assert_called_once_with(
        ["./result_images/test query/e50c1c76e8.jpg", "./result_images/test query/f8b0ca4a4b.jpg"],
        ["https://picsum.photos/id/237/200/300", "https://picsum.photos/seed/picsum/200/300"],
        "test query"
    )
