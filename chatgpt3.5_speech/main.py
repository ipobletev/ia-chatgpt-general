import openai
import pyttsx3
import speech_recognition as sr
import userconfig

#Creds
openai.api_key = userconfig.OPENAI_APIKEY

#
microfone_index = userconfig.MICROPHONE_INDEX

engine = pyttsx3.init()

r = sr.Recognizer()
mic = sr.Microphone(device_index=microfone_index)

conversation=[{"role": "system", "content": userconfig.SYSTEM_PROMPT}]

print("#############################")
print("Basic chatGPT")
print("#############################")

while True:
    try:
        
        with mic as source:
            print("\nlistening...")
            r.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = r.listen(source)
            except KeyboardInterrupt: 
                break
            
        print("no longer listening.\n")

        try:
            user_input = r.recognize_google(audio, language="es-ES")
        except KeyboardInterrupt:
            break
        except:
            continue
        
        print("User: " + user_input)
        
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
        print("Assistant: " + response_str + "\n")
        ####

        engine.say(response_str)
        engine.runAndWait()
    
    except KeyboardInterrupt:
        break
    
print("\n#############################")
print("Finish program")