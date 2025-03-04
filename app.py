from flask import Flask, render_template, request, jsonify
from models import claude_chat, gemini_chat, openai_chat, llama_chat


#for render
# import os
# gemini_api_key = os.getenv('gemini_api_key_render')
# openai_api_key = os.getenv('openai_api_key_render')
# claude_api_key = os.getenv('claude_api_key_render')

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
        response = llama_chat(prompt)
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
