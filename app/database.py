from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@db/documents"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    rubrics = Column(String)
    text = Column(String)
    created_date = Column(DateTime)

class DatabaseClient:
    def __init__(self):
        self.db = SessionLocal()

    async def create_document(self, doc):
        db_doc = DocumentModel(**doc.dict())
        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)

    async def delete_document(self, doc_id):
        doc = self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if doc:
            self.db.delete(doc)
            self.db.commit()