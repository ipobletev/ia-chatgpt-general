from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')
PINECONE_APIKEY = os.getenv('PINECONE_APIKEY', '')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', '')
PINECONE_INDEX = os.getenv('PINECONE_INDEX', '')

#
DEFAULT_SYSTEM_PROMPT = os.getenv('DEFAULT_SYSTEM_PROMPT', 'You are a helpful assistant.')


