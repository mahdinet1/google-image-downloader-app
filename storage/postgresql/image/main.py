from sqlalchemy.orm import sessionmaker, Session
from model.images import Image
from service.crawler.crawler_service import StorageInterface


class SaveImage(StorageInterface):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def save_image(self, address: list[str], src: list[str], query: str):
        db_images = []
        for addr, s in zip(address, src):
            db_images.append(Image(saved_address=addr, src=s,query=query))
        self.db.add_all(db_images)
        self.db.commit()
