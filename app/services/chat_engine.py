from pathlib import Path
import fitz
import pyttsx3
from threading import Thread

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document

class PDFReaderService:
    @staticmethod
    def extract_text(pdf_path: Path) -> str:
        with fitz.open(pdf_path) as doc:
            return "".join(page.get_text() for page in doc)


class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.thread = None
        self._is_speaking = False

    def _speak(self, text: str):
        self._is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self._is_speaking = False

    def speak(self, text: str):
        if self._is_speaking:
            self.stop()
        self.thread = Thread(target=self._speak, args=(text,), daemon=True)
        self.thread.start()

    def stop(self):
        self.engine.stop()
        self._is_speaking = False

    def is_speaking(self) -> bool:
        return self._is_speaking


class ChatEngine:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.qa_chain = None
        self.tts = TTSService()

    def build_qa_chain(self, chunks: list[str]):
        docs = [Document(page_content=chunk) for chunk in chunks]
        vectordb = FAISS.from_documents(docs, self.embedding_model)
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=vectordb.as_retriever())

    def answer_question(self, question: str, speak: bool = False) -> str:
        if not self.qa_chain:
            return "No knowledge base loaded."
        answer = self.qa_chain.run(question)
        if speak:
            self.tts.speak(answer)
        return answer