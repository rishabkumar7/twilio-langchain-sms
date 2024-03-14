from langchain_openai import OpenAI
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from twilio.rest import Client
import textwrap
import os


from dotenv import load_dotenv
load_dotenv()


def create_db_from_url(url: str):
    loader = WebBaseLoader(url)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)[:4]
    return docs

def generate_summary(docs):
  llm = Ollama(model="mistral")
  chain = load_summarize_chain(llm,
                            chain_type="map_reduce",
                            verbose = True)
  output_summary = chain.invoke(docs)
  summary = output_summary["output_text"]
  return summary

"""
url = "https://arxiv.org/abs/2401.09334"


if url:
  docs = create_db_from_url(url)
  response = generate_summary(docs)
  print (response["output_text"])
"""

def send_summary(number, summary):
  account_sid = os.environ['TWILIO_ACCOUNT_SID']
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  client = Client(account_sid, auth_token)

  message = client.messages \
    .create(
          body=summary,
          from_= os.getenv("FROM_NUMBER"),
          to= number
        )
  print(message.sid)