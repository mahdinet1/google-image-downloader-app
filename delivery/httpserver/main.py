import uvicorn
from fastapi import FastAPI, Depends
from service.crawler.crawler_service import CrawlerService

app = FastAPI()

class FastHttpServer:
    def __init__(self, crawler_svc):

        self.crawlerService = crawler_svc
        self.register_routes()

    def register_routes(self):
        @app.get("/query")
        async def get_query(query: str):
            await self.crawlerService.query(query)
            return {"status": "ok"}

    def start(self):
        uvicorn.run(app, host='0.0.0.0', port=8813,workers=1)
