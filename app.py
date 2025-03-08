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
        # system="You are a helpful assistant",
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

# ------------ RESET CONVERSATIONS ----------------
# Function to reset all conversation histories
def reset_all_conversations():
    global openai_conversation_history, claude_conversation_history, llama_conversation_history, genai_chat
    
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

# -----------APP------------

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def main_page():
    return render_template("main.html")

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

# --------- 4o-mini ---------
@app.route("/chat/openai-4o-mini", methods=["POST"])
def openai_route():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai_gpt_4o_mini_chat(prompt)
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


@app.route("/reset_conversations", methods=["POST"])
def reset_conversations():
    try:
        # Reset all conversation histories
        reset_all_conversations()
        return jsonify({"status": "success", "message": "All conversation histories cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         # form submission
#         data = request.get_json()
#         prompt = data.get("prompt")

#         if not prompt:
#             return jsonify({"error": "No prompt provided"}), 400

#         try:
#             #call/recieve chats
#             gemini_response = gemini_chat(prompt)

#             openai_response = openai_chat(prompt)

#             llama_response = llama_chat(prompt)

#             claude_response = claude_chat(prompt)

#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#         # Return responses
#         return jsonify({
#             "status": "success",
#             "prompt": prompt,
#             "gemini_response": gemini_response,
#             "openai_response": openai_response,
#             "llama_response": llama_response,
#             "claude_response": claude_response
#         })

#     return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
