import ollama 
while True:
    user_input=input()
    if user_input=="stop" or user_input=="exit":
        break
    else:
            responce=ollama.chat(
            model= "mistral:latest",
            messages=[{
                'role': 'user',
                'content': user_input
            }]
            )
            print(responce['message']['content'])