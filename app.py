from flask import Flask, render_template, request, jsonify
# from models import claude_chat, gemini_chat, openai_chat, llama_chat
# from SECRETS import gemini_api_key, openai_api_key, claude_api_key
from google import genai
from openai import OpenAI
from together import Together
# import requests #llama
import anthropic #claude


#for render
import os
gemini_api_key = os.getenv('gemini_api_key_render')
openai_api_key = os.getenv('openai_api_key_render')
claude_api_key = os.getenv('claude_api_key_render')
together_llama_api_key = os.getenv('together_llama_api_key_render')

# ---------GEMINI-----------
# clients
genai_client = genai.Client(api_key=gemini_api_key)
genai_chat = genai_client.chats.create(model='gemini-2.0-flash')

# function calling gemini api
def gemini_chat(prompt):
    # genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
    response = genai_chat.send_message(prompt)
    gemini_response = response.text
    print('Gemini:', gemini_response)
    #to clear chats, just... create a new one. genai_client.chats.create...
    return gemini_response

# --------OPENAI-------------
#openai clients
openai_client = OpenAI(api_key=openai_api_key)
openai_conversation_history = []

# function calling openai api 
def openai_chat(prompt):
    # user_input = input(str)

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI response:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    # user_input = input(str)

    return openai_response
    
# ---------LLAMA------------
llama_client = Together(api_key=together_llama_api_key)
llama_conversation_history = []

def llama_tog_chat(prompt):
    llama_conversation_history.append(
        {"role": "user", "content": prompt}
    )
    llama_response = llama_client.chat.completions.create(
        model = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages = llama_conversation_history
    )

    content = llama_response.choices[0].message.content
    llama_conversation_history.append(
        {"role": "assistant", "content": content}
    )

    print("Llama:", content)
    return content

# ---------------CLAUDE----------------
claude_client = anthropic.Anthropic(api_key=claude_api_key)
claude_conversation_history = []

def claude_chat(prompt):
    claude_conversation_history.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    )

    # create the message
    message = claude_client.messages.create(
        model = "claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0,
        system="You are a world class poet. reply in short messages only",
        messages=claude_conversation_history
    )

    claude_response = message.model_dump()['content'][0]['text']
    print('Claude:', claude_response)

     # append to conversation history
    role = message.model_dump()['role']
    content = message.model_dump()['content']

    claude_conversation_history.append(
    {'role': role,
    'content': content}
    )

    return claude_response

# Function to reset all conversation histories
def reset_all_conversations():
    global openai_conversation_history, claude_conversation_history, data, genai_chat
    
    # Reset OpenAI conversation history
    openai_conversation_history.clear()
    
    # Reset Claude conversation history
    claude_conversation_history.clear()
    
    # Reset Llama conversation history
    data["messages"].clear()
    
    # Reset Gemini conversation
    global genai_client
    genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
    
    print("All conversation histories have been reset")
    return True
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat/gemini", methods=["POST"])
def gemini_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = gemini_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat/openai", methods=["POST"])
def openai_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat/llama", methods=["POST"])
def llama_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = llama_tog_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat/claude", methods=["POST"])
def claude_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = claude_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def reset_all_conversations():
    global openai_conversation_history, claude_conversation_history, data, genai_chat
    
    # Reset OpenAI conversation history
    openai_conversation_history.clear()
    
    # Reset Claude conversation history
    claude_conversation_history.clear()
    
    # Reset Llama conversation history
    llama_conversation_history.clear()
    
    # Reset Gemini conversation
    global genai_client
    genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
    
    print("All conversation histories have been reset")
    return True

# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         # Handle the form submission
#         data = request.get_json()
#         prompt = data.get("prompt")

#         if not prompt:
#             return jsonify({"error": "No prompt provided"}), 400

#         try:
#             #call/recieve genai chats
#             gemini_response = gemini_chat(prompt)

#             # call/recieve open ai chats
#             openai_response = openai_chat(prompt)

#             # call/recievev llama chats
#             llama_response = llama_chat(prompt)

#             # call/recieve claude chats
#             claude_response = claude_chat(prompt)

#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#         # Return the responses
#         return jsonify({
#             "status": "success",
#             "prompt": prompt,
#             "gemini_response": gemini_response,
#             "openai_response": openai_response,
#             "llama_response": llama_response,
#             "claude_response": claude_response
#         })

#     # Render the HTML template for GET requests
#     return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
