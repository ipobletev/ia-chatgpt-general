import openai
import userconfig

#Creds
openai.api_key = userconfig.OPENAI_APIKEY

conversation=[{"role": "system", "content": userconfig.DEFAULT_SYSTEM_PROMPT}]

print("#############################")
print("Basic chatGPT")
print("#############################")

while True:
    try:
        
        user_input = input("User: ")

        #### ChatGPT 3.5
        conversation.append({"role": "user", "content": user_input})

        # fetch response from open AI api
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = conversation,
            temperature=2,
            max_tokens=250,
            top_p=0.9
        )
        response_str=response['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": response_str})
        print("assistant: " + response_str + "\n")
        ####
    
    except KeyboardInterrupt:
        break
    
print("\n#############################")
print("Finish program")