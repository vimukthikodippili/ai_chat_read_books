from sqlalchemy import Column, String, Integer, Text
from app.core.db import Base

class PdfDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)