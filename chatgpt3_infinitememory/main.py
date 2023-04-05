import openai
import pinecone
import userconfig
import sme_chatgpt
import datetime
from time import time,sleep
from uuid import uuid4
import json

def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_json(filepath, payload):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)
        
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)
        
def load_conversation(results):
    result = list()
    for m in results['matches']:
        info = load_json('nexus/%s.json' % m['id'])
        result.append(info)
    ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    messages = [i['message'] for i in ordered]
    return '\n'.join(messages).strip()

if __name__=="__main__":

    convo_length = 30 # Return convo_length results with semantic similarity
    openai.api_key = userconfig.OPENAI_APIKEY
    pinecone.init(api_key=userconfig.PINECONE_APIKEY, environment=userconfig.PINECONE_ENVIRONMENT)
    vdb = pinecone.Index(userconfig.PINECONE_INDEX)
    
    while True:
        print("##########################################")
        #### get user input, save it, vectorize it, save to pinecone
        payload = list()
        user_input = input('\n\nUser: ')
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        message = user_input
        vector = sme_chatgpt.gpt3_embedding(message)
        unique_id = str(uuid4())
        metadata = {'speaker': 'user', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
        save_json('./nexus/%s.json' % unique_id, metadata)
        payload.append((unique_id, vector))
        #### search for relevant messages (semantic relevant), and generate a response
        results = vdb.query(vector=vector, top_k=convo_length)
        conversation = load_conversation(results)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        prompt = open_file('prompt_response.txt').replace('<<CONVERSATION>>', conversation).replace('<<MESSAGE>>', user_input)
        #### generate response, vectorize, save, etc
        output = sme_chatgpt.gpt3_completion(prompt)
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        vector = sme_chatgpt.gpt3_embedding(output)
        unique_id = str(uuid4())
        metadata = {'speaker': 'assistant', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
        save_json('./nexus/%s.json' % unique_id, metadata)
        payload.append((unique_id, vector))
        vdb.upsert(payload)
        print('assistant: %s' % output) 