from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')

#
MICROPHONE_INDEX =int(os.getenv('MICROPHONE_INDEX', '1'))
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant.')