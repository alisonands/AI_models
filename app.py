from flask import Flask, render_template, request, jsonify
from google import genai
from openai import OpenAI
from SECRETS import gemini_api_key, openai_api_key
import requests #llama

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
    return gemini_response

# --------OPENAI-------------
#openai clients
openai_client = OpenAI(api_key=openai_api_key)

# function calling openai api 
def openai_chat(prompt):
    openai_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
    print ('OpenAI:', openai_response)
    return openai_response

# ---------LLAMA------------
# ollama run llama3.2
url = "http://0.0.0.0:11434/api/chat"
data = {
    "model": "llama3.2",
    "messages": [],
    "stream": False,
    }

def llama_chat(prompt):
    # append prompt to data
    user_prompt = {
        "role": "user",
        "content": prompt}
    data['messages'].append(user_prompt)
    # print(data)

    response = requests.post(url, json=data)
    
    data['messages'].append(response.json()['message'])
    llama_response = response.json()['message']['content']
    print('Llama:', llama_response)
    return llama_response


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Handle the form submission
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        try:
            #call/recieve genai chats
            gemini_response = gemini_chat(prompt)

            # call/recieve open ai chats
            openai_response = openai_chat(prompt)

            # call/recievev llama chats
            llama_response = llama_chat(prompt)
            print (llama_response)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # Return the responses
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "gemini_response": gemini_response,
            "openai_response": openai_response,
            "llama_response": llama_response
        })

    # Render the HTML template for GET requests
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
