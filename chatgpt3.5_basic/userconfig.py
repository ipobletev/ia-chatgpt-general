from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')

#
DEFAULT_SYSTEM_PROMPT = os.getenv('DEFAULT_SYSTEM_PROMPT', 'You are a helpful assistant.')
