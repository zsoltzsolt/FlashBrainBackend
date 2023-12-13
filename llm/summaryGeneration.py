from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from config import OPENAI_API_KEY

def generate_metadata(path: str) -> dict:
    loader = PyPDFLoader(path)
    docs = loader.load()

    prompt_template = """Return a this information: 'title' and 'category' in json format where 'title' represents a sugestive title for the following
    text and 'category' spcifies the number coresponding to the correct category: 2 (math), 3 (science), 4 (history), 5 (languages), 6 (computer science), 7 (geography), 8 (economics), 9 (others). 
    "{text}" """
    prompt = PromptTemplate.from_template(prompt_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", api_key=OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    docs = loader.load()
    return stuff_chain.run(docs)

def generate_summaries(path: str) -> str:
    loader = PyPDFLoader(path)
    docs = loader.load()
    prompt_template = """Summarize the following text in exactly 5, 2-3 sentence ideas formatted as a json. The number of ideas HAS to be 5,10 or 15. The json should be a list containing the generated ideas, and each idea has a 'title' and 'content' keys. This is the text:
    "{text}" """
    prompt = PromptTemplate.from_template(prompt_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", api_key=OPENAI_API_KEY)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    docs = loader.load()
    v = stuff_chain.run(docs)
    print(v)
    return v