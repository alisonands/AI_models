from flask import Flask, render_template, request, jsonify, make_response
# from models import claude_chat, gemini_chat, openai_chat, llama_chat
# from SECRETS import gemini_api_key, openai_api_key, claude_api_key
from google import genai
from openai import OpenAI
from together import Together
# import requests #llama
import anthropic #claude
from sqlalchemy import create_engine, text
from datetime import datetime
import os

# Import functions from models.py
from models import (
    handle_conversation, 
    add_to_conversation, 
    get_conversation_history, 
    clear_conversation_history,
    clean_conversation_history
)

#for render
gemini_api_key = os.getenv('gemini_api_key_render')
openai_api_key = os.getenv('openai_api_key_render')
claude_api_key = os.getenv('claude_api_key_render')
together_llama_api_key = os.getenv('together_llama_api_key_render')
deepseek_api_key = os.getenv('deepseek_api_key_render')

# --------------------------
# ---------GEMINI-----------
# --------------------------
# --------genai-2.0---------

# clients
genai_client = genai.Client(api_key=gemini_api_key)
genai_chat2_0 = genai_client.chats.create(model='gemini-2.0-flash')

# function calling gemini api
def gemini_2_0_flash_chat(prompt):
    # genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
    response = genai_chat2_0.send_message(prompt)
    gemini_response = response.text
    print('Gemini 2.0 flash:', gemini_response)
    #to clear chats, just... create a new one. genai_client.chats.create...
    return gemini_response

# ------genai-2.0-lite------
genai_chat2_0_lite = genai_client.chats.create(model='gemini-2.0-flash-lite')
def gemini_2_0_flash_lite_chat(prompt):
    # genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
    response = genai_chat2_0_lite.send_message(prompt)
    gemini_response = response.text
    print('Gemini 2.0 flash lite:', gemini_response)
    #to clear chats, just... create a new one. genai_client.chats.create...
    return gemini_response

# ---------------------------
# --------OPENAI-------------
# ---------------------------

#openai clients
openai_client = OpenAI(api_key=openai_api_key)
openai_conversation_history = []

# --------- 4.5-preview ----------
# function calling openai api 
def openai_gpt_4_5_preview_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4.5-preview-2025-02-27",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI 4.5 preview:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response

# --------- 4o ----------
# function calling openai api 
def openai_gpt_4o_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI 4o:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response


# ----------- o1 ------------
def openai_gpt_o1_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="o1",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI o1:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response

# --------- o1-mini ----------
def openai_gpt_o1_mini_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="o1-mini",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI o1-mini:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response

    
# --------- o3-mini ----------
def openai_gpt_o3_mini_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="o3-mini",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI o3-mini:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response



# --------------------------
# ---------LLAMA------------
# --------------------------
llama_client = Together(api_key=together_llama_api_key)
llama_conversation_history = []

def llama_3_3_tog_chat(prompt):
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

    print("Llama3.3:", content)
    return content

# -------------------------------------
# ---------------CLAUDE----------------
# -------------------------------------
claude_client = anthropic.Anthropic(api_key=claude_api_key)
claude_conversation_history = []
# -------------3.7 sonnet--------------
def claude_3_7_sonnet_chat(prompt):
    claude_conversation_history.append(
        {"role": "user", "content":[{"type": "text", "text": prompt}]}
    )

    # create the message
    message = claude_client.messages.create(
        model = "claude-3-7-sonnet-20250219",
        max_tokens=500,
        temperature=0,
        # system="You are a world class poet. reply in short messages only",
        messages=claude_conversation_history
    )

    claude_response = message.model_dump()['content'][0]['text']
    print('Claude 3.7 sonnet:', claude_response)

     # append to conversation history
    role = message.model_dump()['role']
    content = message.model_dump()['content']

    claude_conversation_history.append(
    {'role': role,
    'content': content}
    )

    return claude_response

# ---------------3 opus----------------
def claude_3_opus_chat(prompt):
    claude_conversation_history.append(
        {"role": "user", "content":[{"type": "text", "text": prompt}]}
    )

    # create the message
    message = claude_client.messages.create(
        model = "claude-3-opus-20240229",
        max_tokens=500,
        temperature=0,
        # system="You are a world class poet. reply in short messages only",
        messages=claude_conversation_history
    )

    claude_response = message.model_dump()['content'][0]['text']
    print('Claude 3 opus:', claude_response)

     # append to conversation history
    role = message.model_dump()['role']
    content = message.model_dump()['content']

    claude_conversation_history.append(
    {'role': role,
    'content': content}
    )

    return claude_response

# --------------3.5 sonnet--------------
def claude_3_5_sonnet_chat(prompt):
    claude_conversation_history.append(
        {"role": "user", "content":[{"type": "text", "text": prompt}]}
    )

    # create the message
    message = claude_client.messages.create(
        model = "claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0,
        # system="You are a world class poet. reply in short messages only",
        messages=claude_conversation_history
    )

    claude_response = message.model_dump()['content'][0]['text']
    print('Claude 3.5 sonnet:', claude_response)

     # append to conversation history
    role = message.model_dump()['role']
    content = message.model_dump()['content']

    claude_conversation_history.append(
    {'role': role,
    'content': content}
    )

    return claude_response


# --------------3.5 haiku--------------
def claude_3_5_haiku_chat(prompt):
    claude_conversation_history.append(
        {"role": "user", "content":[{"type": "text", "text": prompt}]}
    )

    # create the message
    message = claude_client.messages.create(
        model = "claude-3-5-haiku-20241022",
        max_tokens=500,
        temperature=0,
        # system="You are a world class poet. reply in short messages only",
        messages=claude_conversation_history
    )

    claude_response = message.model_dump()['content'][0]['text']
    print('Claude 3.5 haiku:', claude_response)

     # append to conversation history
    role = message.model_dump()['role']
    content = message.model_dump()['content']

    claude_conversation_history.append(
    {'role': role,
    'content': content}
    )

    return claude_response

# lightweight testing
# ---------------3 haiku---------------
def claude_3_haiku_chat(prompt):
    claude_conversation_history.append(
        {"role": "user", "content":[{"type": "text", "text": prompt}]}
    )

    # create the message
    message = claude_client.messages.create(
        model = "claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0,
        # system="You are a world class poet. reply in short messages only",
        messages=claude_conversation_history
    )

    claude_response = message.model_dump()['content'][0]['text']
    print('Claude 3 haiku:', claude_response)

     # append to conversation history
    role = message.model_dump()['role']
    content = message.model_dump()['content']

    claude_conversation_history.append(
    {'role': role,
    'content': content}
    )

    return claude_response

# -------------------------------------
# --------------DEEPSEEK---------------
# -------------------------------------

deepseek_client=OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
deepseek_conversation_history = []

# -----------deepseek-chat------------
def deepseek_chatx2(prompt):
    deepseek_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=deepseek_conversation_history,
        stream=False
    )

    deepseek_response = response.choices[0].message.content
    print('Deepseek chat:', deepseek_response)

    deepseek_conversation_history.append(
        {"role": "assistant", "content": deepseek_response}
    )

    return deepseek_response

# ---------deepseek-reasoner----------
def deepseek_reasoner_chat(prompt):
    deepseek_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=deepseek_conversation_history,
        stream=False
    )

    deepseek_response = response.choices[0].message.content
    print('Deepseek reasoner:', deepseek_response)

    deepseek_conversation_history.append(
        {"role": "assistant", "content": deepseek_response}
    )

    return deepseek_response

# -------------------------------------------------
# ------------ RESET CONVERSATIONS ----------------
# -------------------------------------------------
# Function to reset all conversation histories
def reset_all_conversations():
    global openai_conversation_history, claude_conversation_history, llama_conversation_history, deepseek_conversation_history, genai_chat2_0, genai_chat2_0_lite
    
    # Reset conversation histories
    deepseek_conversation_history.clear()
    openai_conversation_history.clear()
    claude_conversation_history.clear()
    llama_conversation_history.clear()
    
    # Reset Gemini conversations
    global genai_client
    genai_chat2_0 = genai_client.chats.create(model='gemini-2.0-flash')
    genai_chat2_0_lite = genai_client.chats.create(model='gemini-2.0-flash-lite')
    
    # Clear the conversation database
    clear_conversation_history()
    
    print("All conversation histories have been reset")
    return True

# -----------APP------------

app = Flask(__name__)

@app.route("/")
def home():
    if request.authorization and request.authorization.username == "admin" and request.authorization.password =="aimodels271": 
        return render_template("main.html")
    return make_response("<h1>Access Denied!</h1>", 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})

# --------------------------
# ---------GEMINI-----------
# --------------------------
# --------genai-2.0---------
@app.route("/chat/gemini-2_0-flash", methods=["POST"])
def gemini_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = gemini_2_0_flash_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------genai-2.0-lite------
@app.route("/chat/gemini-2_0-flash-lite", methods=["POST"])
def gemini_lite_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = gemini_2_0_flash_lite_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ---------------------------
# --------OPENAI-------------
# ---------------------------

# ----------- o1 ------------
@app.route("/chat/openai-o1", methods=["POST"])
def openai_o1_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_gpt_o1_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ----------- o1-mini ------------
@app.route("/chat/openai-o1-mini", methods=["POST"])
def openai_o1_mini_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_gpt_o1_mini_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------- o3-mini ------------
@app.route("/chat/openai-o3-mini", methods=["POST"])
def openai_o3_mini_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_gpt_o3_mini_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------- 4o ---------
@app.route("/chat/openai-4o", methods=["POST"])
def openai_4o_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_gpt_4o_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# --------- 4o ---------
@app.route("/chat/openai-4_5_preview", methods=["POST"])
def openai_4_5_preview_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_gpt_4_5_preview_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# ---------LLAMA------------
# --------------------------
@app.route("/chat/llama3_3", methods=["POST"])
def llama3_2_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = llama_3_3_tog_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------------
# ---------------CLAUDE----------------
# -------------------------------------
# -------------3.7 sonnet--------------
@app.route("/chat/claude_3_7_sonnet", methods=["POST"])
def claude_3_7_sonnet_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = claude_3_7_sonnet_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------3 opus----------------
@app.route("/chat/claude_3_opus", methods=["POST"])
def claude_3_opus_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = claude_3_opus_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------3.5 sonnet--------------
@app.route("/chat/claude_3_5_sonnet", methods=["POST"])
def claud_3_5_sonnet_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = claude_3_5_sonnet_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------3.5 haiku--------------
@app.route("/chat/claude_3_5_haiku", methods=["POST"])
def claud_3_5_haiku_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = claude_3_5_haiku_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------3 haiku---------------
@app.route("/chat/claude_3_haiku", methods=["POST"])
def claude_3_haiku_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = claude_3_haiku_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# -------------------------------------
# --------------DEEPSEEK---------------
# -------------------------------------
# -----------deepseek-chat------------

@app.route("/chat/deepseek_chat", methods=["POST"])
def deepseek_chatx2_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = deepseek_chatx2(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------deepseek-reasoner----------
@app.route("/chat/deepseek_reasoner", methods=["POST"])
def deepseek_reasoner_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = deepseek_reasoner_chat(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# conversation mode
@app.route("/conversation", methods=["POST"])
def conversation_route():
    data = request.get_json()
    prompt = data.get("prompt", "")  # Default to empty string if not provided
    models = data.get("models", [])
    
    # Check if models array is provided and not empty
    if not models:
        return jsonify({"error": "No models provided", "responses": []}), 400
    
    try:
        responses = handle_conversation(prompt, models)
        return jsonify({"responses": responses})
    except Exception as e:
        print(f"Error in conversation mode: {str(e)}")
        # Return an empty responses array to prevent frontend errors
        return jsonify({"error": str(e), "responses": []}), 500

@app.route("/reset_conversations", methods=["POST"])
def reset_conversations():
    try:
        # Reset all conversation histories
        reset_all_conversations()
        return jsonify({"status": "success", "message": "All conversation histories cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
