from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import YoutubeLoader
from abc import ABC, abstractmethod
from db.models import DbSummary
from sqlalchemy.orm import Session
from db.database import get_db
from routers.schemas import SummarySourceBase, SummaryBase, FlashCardBase, UserDisplay
from db.flashcard import create_flash_card
import json
from fastapi import Depends
import os
from time import sleep
from email1.emailSender import send_email
from email1.summaryReady import create_subject_body

class SummaryGenerator(ABC):

    @abstractmethod
    def get_loader(self, path: str):
        pass

    def generate_metadata(self, path: str):
        loader = self.get_loader(path)
        docs = loader.load()

        prompt_template = """Return a this information: 'title' and 'category' in json format where 'title' represents a suggestive title for the following
        text and 'category' specifies the number corresponding to the correct category: 2 (math), 3 (science), 4 (history), 5 (languages), 6 (computer science), 7 (geography), 8 (economics), 9 (others). 
        "{text}" """
        prompt = PromptTemplate.from_template(prompt_template)

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", api_key=os.environ.get("OPENAI_API_KEY"))
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

        docs = loader.load()
        return stuff_chain.run(docs)


    def generate_summaries(self, path: str):
        loader = self.get_loader(path)
        docs = loader.load()
        prompt_template = """Summarize the following text in exactly 5, 2-3 sentence ideas formatted as a json. The number of ideas HAS to be 5,10 or 15. The json should be a list containing the generated ideas, and each idea has a 'title' and 'content' keys. This is the text:
        "{text}" """
        prompt = PromptTemplate.from_template(prompt_template)

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", api_key=os.environ.get("OPENAI_API_KEY"))
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

        docs = loader.load()
        v = stuff_chain.run(docs)  # Modificarea aici
        print(v)
        return v
       


    def generate_summary(self, request: SummarySourceBase, db: Session = Depends(get_db)):

        title_category = self.generate_metadata(request.path)
        print(title_category)
        newJsonMeta = json.loads(title_category)

        message = self.generate_summaries(request.path)
        newJson = json.loads(message)
        print(newJson)

        new_summary = DbSummary(
            title=newJsonMeta["title"],
            ownerId=request.ownerId,
            categoryId=newJsonMeta["category"],
            isPublic=request.isPublic
        )
        db.add(new_summary)
        db.commit()
        db.refresh(new_summary)

        for json_item in newJson:
            new_flash = FlashCardBase(
                title=json_item['title'],
                content=json_item['content'],
                imagePath="https://www.shutterstock.com/image-photo/example-word-written-on-wooden-260nw-1765482248.jpg",
                summaryId=new_summary.summaryId
            )
            create_flash_card(new_flash, db)
            
        
        if os.path.exists(request.path):
            os.remove(request.path)

        return new_summary.summaryId

class PDFSummaryGenerator(SummaryGenerator):
    def get_loader(self, path: str):
        loader = PyPDFLoader(path)
        return loader

class YoutubeSummaryGenerator(SummaryGenerator):
    def get_loader(self, path: str):
        loader = YoutubeLoader(path)
        return loader

