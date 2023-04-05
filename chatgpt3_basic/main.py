import openai
import userconfig

#Creds
openai.api_key = userconfig.OPENAI_APIKEY

#
user_name = userconfig.USER_NAME
bot_name = userconfig.BOT_NAME

conversation = ""

print("#############################")
print("Basic chatGPT")
print("#############################")

while True:
    try:
        
        user_input = input("User: ")
        
        prompt = user_name + ": " + user_input + "\n" + bot_name+ ": "

        #print(user_name + ": " + user_input)
        
        conversation += prompt  # allows for context

        # fetch response from open AI api
        response = openai.Completion.create(
            engine='text-davinci-003', 
            prompt=conversation, 
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0)
        
        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

        conversation += response_str + "\n"
        print(bot_name+ ": " + response_str + "\n")
    
    except KeyboardInterrupt:
        break
    
print("\n#############################")
print("Finish program")