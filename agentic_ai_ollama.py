import ollama 
while True:
    user_input=input("Enter our query here (type 'exit' or 'stop' to stop): ")
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
            print("models output: ",responce['message']['content'])