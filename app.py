from flask import Flask, render_template, request, jsonify, make_response
from models import claude_3_7_sonnet_chat, claude_3_opus_chat, claude_3_5_sonnet_chat, claude_3_haiku_chat, claude_3_5_haiku_chat, gemini_2_0_flash_chat, gemini_2_0_flash_lite_chat, openai_gpt_4o_mini_chat, llama_3_3_tog_chat, openai_gpt_o1_chat, openai_gpt_o1_mini_chat, openai_gpt_o3_mini_chat


#for render
# import os
# gemini_api_key = os.getenv('gemini_api_key_render')
# openai_api_key = os.getenv('openai_api_key_render')
# claude_api_key = os.getenv('claude_api_key_render')

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

@app.route("/reset_conversations", methods=["POST"])
def reset_conversations():
    try:
        # Reset all conversation histories
        from models import reset_all_conversations
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
