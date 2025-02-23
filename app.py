from flask import Flask, render_template, request, jsonify
from google import genai
from openai import OpenAI

#genai clients
genai_client = genai.Client(api_key="AIzaSyAXgh68n1heuatP5gd8NvKn2soZGf2sf04")
genai_chat = genai_client.chats.create(model='gemini-2.0-flash')

#openai clients
openai_client = OpenAI(api_key='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')
# openai_chat = client.beta.assistants.create(
#     instructions="keep responses short and minimize tokens",
#     # name="Math Tutor",
#     # tools=[{"type": "code_interpreter"}],
#     model="gpt-4o",
# )

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Handle the form submission
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Call the Gemini API
        try:
            #call/recieve genai chats
            genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
            response = genai_chat.send_message(prompt)
            gemini_response = response.text
            print('Gemini:', gemini_response)

            # call/recieve open ai chats
            openai_response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content
            print ('OpenAI:', openai_response)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # Return the responses
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "gemini_response": gemini_response,
            "openai_response": openai_response
        })

    # Render the HTML template for GET requests
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
