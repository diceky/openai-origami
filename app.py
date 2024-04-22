import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

messages=[
        {
            "role": "system", 
            "content": "You are a customer support staff, skilled in making sure that the customer is heard and their ask is being processed."
        },
    ]

def add_message(role, message):
    messages.append({"role": role, "content": message})

def converse_with_chatGPT():
    model_engine = "gpt-3.5-turbo"
    response = client.chat.completions.create(
        model=model_engine,
        messages=messages,
        max_tokens = 1024, # this is the maximum number of tokens that can be used to provide a response.
        n=1, #number of responses expected from the Chat GPT
        stop=None, 
        temperature=0.5 #making responses deterministic
    )
    message = response.choices[0].message.content
    return message.strip()

def process_user_query(prompt):
    user_prompt = (f"{prompt}")
    add_message("user", user_prompt)
    result = converse_with_chatGPT()
    add_message("assistant", result)
    print(result)

#### uncomment here if you want to run in console ####
# def start_conversation():
#     while True:
#         prompt = input("Enter your question: ")
#         response = process_user_query(prompt)
#         print(json.dumps(messages, indent=4))

# start_conversation()


@app.route('/sendMessage', methods=['POST'])
def send_message():
    global messages
    if request.method == "POST":
        content = request.json
        if 'message' in content:
            newMessage = content['message']
            add_message("user", newMessage)
            result = converse_with_chatGPT()
            add_message("assistant", result)
        return 'OK'

@app.route('/getResponse', methods=['GET'])
def get_response():
    global messages
    if request.method == "GET":
        values = {
            'length': len(messages),
            'response': messages[len(messages)-1]["content"]
        }
        return jsonify({'values': values})

if __name__ == "__main__":
    app.run() #add host='0.0.0.0' as parameter to access from other local PCs