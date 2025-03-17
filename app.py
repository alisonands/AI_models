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

#for render
import os
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
    global openai_conversation_history, claude_conversation_history, llama_conversation_history, genai_chat2_0, genai_chat2_0_lite, deepseek_conversation_history
    
    # Reset OpenAI conversation history
    openai_conversation_history.clear()
    
    # Reset Claude conversation history
    claude_conversation_history.clear()
    
    # Reset Llama conversation history
    llama_conversation_history.clear()
    
    # Reset Deepseek conversation history
    deepseek_conversation_history.clear()
    
    # Reset Gemini conversation
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

# testinf if the database connects
try:
    database_path = "postgresql://ai_models_user:l48XPVOJmaBcWwFMS6MnnapeF7BCXOi5@dpg-cvbkam3tq21c73e0fk1g-a.oregon-postgres.render.com/ai_models"
    engine = create_engine(database_path)
    # Test the connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("Connected to PostgreSQL database")
    #if not use sqlite database
except Exception as e:
    print(f"Error connecting to PostgreSQL: {str(e)}")
    print("Falling back to SQLite database")
    sqlite_path = os.path.join(os.path.dirname(__file__), "conversation.db")
    database_path = f"sqlite:///{sqlite_path}"
    engine = create_engine(database_path)
    
    # Create the table if it doesn't exist
    with engine.connect() as connection:
        connection.execute(text('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            model TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''))
        connection.commit()

# Function to add a message to the conversation database
def add_to_conversation(role, content, model=None):
    try:
        with engine.connect() as connection:
            # First, let's check the table structure
            inspect_query = text("SELECT column_name FROM information_schema.columns WHERE table_name = 'prompts'")
            columns = [row[0] for row in connection.execute(inspect_query)]
            print(f"Available columns in prompts table: {columns}")
            
            # Adjust the query based on the actual column names
            if 'text' in columns:
                content_column = 'text'
            elif 'content' in columns:
                content_column = 'content'
            else:
                # If we can't find a suitable column, create a new table
                print("Creating new prompts table with correct structure")
                connection.execute(text('''
                DROP TABLE IF EXISTS conversation_prompts;
                CREATE TABLE conversation_prompts (
                    id SERIAL PRIMARY KEY,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    model TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                '''))
                connection.commit()
                
                # Use the new table
                query = text("INSERT INTO conversation_prompts(role, content, model) VALUES(:role, :content, :model)")
                connection.execute(query, {"role": role, "content": content, "model": model})
                connection.commit()
                return
            
            # Use the existing table with the correct column name
            query = text(f"INSERT INTO prompts(role, {content_column}, model) VALUES(:role, :content, :model)")
            connection.execute(query, {"role": role, "content": content, "model": model})
            connection.commit()
    except Exception as e:
        print(f"Error adding to conversation: {str(e)}")
        # Fall back to SQLite
        use_sqlite_fallback(role, content, model)

def use_sqlite_fallback(role, content, model=None):
    print("Using SQLite fallback for database operations")
    import os
    import sqlite3
    
    sqlite_path = os.path.join(os.path.dirname(__file__), "conversation.db")
    
    # Create the SQLite database and table if they don't exist
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        model TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    
    # Insert the data
    cursor.execute(
        "INSERT INTO prompts (role, content, model) VALUES (?, ?, ?)",
        (role, content, model)
    )
    conn.commit()
    conn.close()

# Function to get the full conversation history
def get_conversation_history():
    try:
        with engine.connect() as connection:
            # Check the table structure
            inspect_query = text("SELECT column_name FROM information_schema.columns WHERE table_name = 'prompts'")
            columns = [row[0] for row in connection.execute(inspect_query)]
            
            # Determine which table and column to use
            if 'text' in columns:
                content_column = 'text'
                table_name = 'prompts'
            elif 'content' in columns:
                content_column = 'content'
                table_name = 'prompts'
            else:
                # Try the new table
                try:
                    connection.execute(text("SELECT 1 FROM conversation_prompts LIMIT 1"))
                    content_column = 'content'
                    table_name = 'conversation_prompts'
                except:
                    # Fall back to SQLite
                    return get_sqlite_conversation_history()
            
            query = text(f"SELECT role, model, {content_column} FROM {table_name} ORDER BY id")
            result = connection.execute(query)
            
            history = []
            for row in result:
                try:
                    role = row.role
                    model = row.model
                    content = getattr(row, content_column)
                    
                    if model:
                        formatted_content = f"[{model}] {content}"
                    else:
                        formatted_content = content
                        
                    history.append({"role": role, "content": formatted_content})
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue
            
            return history
    except Exception as e:
        print(f"Error getting conversation history: {str(e)}")
        return get_sqlite_conversation_history()

def get_sqlite_conversation_history():
    print("Using SQLite fallback for getting conversation history")
    import os
    import sqlite3
    
    sqlite_path = os.path.join(os.path.dirname(__file__), "conversation.db")
    
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prompts'")
        if not cursor.fetchone():
            return []
        
        cursor.execute("SELECT role, model, content FROM prompts ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            role, model, content = row
            if model:
                formatted_content = f"[{model}] {content}"
            else:
                formatted_content = content
            history.append({"role": role, "content": formatted_content})
        
        return history
    except Exception as e:
        print(f"Error getting SQLite conversation history: {str(e)}")
        return []

# Function to clear the conversation history
def clear_conversation_history():
    try:
        with engine.connect() as connection:
            # Try to clear the PostgreSQL tables
            try:
                delete_query = text('DELETE FROM prompts')
                connection.execute(delete_query)
                connection.commit()
            except:
                pass
            
            try:
                delete_query = text('DELETE FROM conversation_prompts')
                connection.execute(delete_query)
                connection.commit()
            except:
                pass
            
            # Try to reset sequences
            try:
                reset_query = text('ALTER SEQUENCE prompts_id_seq RESTART WITH 1')
                connection.execute(reset_query)
                connection.commit()
            except:
                pass
            
            try:
                reset_query = text('ALTER SEQUENCE conversation_prompts_id_seq RESTART WITH 1')
                connection.execute(reset_query)
                connection.commit()
            except:
                pass
    except Exception as e:
        print(f"Error clearing PostgreSQL conversation history: {str(e)}")
    
    # Also clear SQLite if it exists
    try:
        import os
        import sqlite3
        
        sqlite_path = os.path.join(os.path.dirname(__file__), "conversation.db")
        if os.path.exists(sqlite_path):
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prompts")
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error clearing SQLite conversation history: {str(e)}")

# Function to handle the conversation between models
def handle_conversation(prompt, models):
    print(f"Starting conversation with prompt: '{prompt}'")
    print(f"Selected models: {models}")
    
    # Special commands
    if prompt and prompt.lower().strip() == "clean history":
        clean_conversation_history()
        return [{"model": "System", "response": "Conversation history has been cleaned."}]
    
    if prompt and prompt.lower().strip() == "clear conversation":
        clear_conversation_history()
        return [{"model": "System", "response": "Conversation history has been cleared."}]
    
    # Check if this is a blank prompt for continuing model conversation
    is_blank_continue = not prompt or prompt.strip() == ""
    print(f"Is blank continue: {is_blank_continue}")
    
    # Only add user prompt to conversation if it's not blank
    if not is_blank_continue:
        try:
            add_to_conversation("user", prompt, None)
            print("Added user prompt to conversation")
        except Exception as e:
            print(f"Error adding user prompt to conversation: {str(e)}")
    
    responses = []
    
    # Process each model in sequence
    for model in models:
        print(f"Processing model: {model}")
        try:
            # Get the full conversation history
            conversation = get_conversation_history()
            print(f"Got conversation history with {len(conversation)} messages")
            
            # Format the conversation for the current model - clean up any role confusion
            formatted_prompt = f"Here is the conversation so far:\n\n"
            for msg in conversation:
                content = msg['content']
                
                # Clean up any role confusion in the content
                if msg["role"] == "user" and content.startswith("User:"):
                    content = content[5:].strip()
                elif msg["role"] == "assistant" and content.startswith("User:"):
                    # Skip assistant messages that are actually user messages
                    continue
                
                # Format based on the role
                if msg["role"] == "user":
                    formatted_prompt += f"User: {content}\n\n"
                else:
                    # Extract model name if present
                    if "[" in content and "]" in content and content.index("[") < content.index("]"):
                        model_prefix = content[:content.index("]")+1]
                        content = content[content.index("]")+1:].strip()
                        formatted_prompt += f"Assistant {model_prefix}: {content}\n\n"
                    else:
                        formatted_prompt += f"Assistant: {content}\n\n"
            
            # Add special instructions for blank continue
            if is_blank_continue:
                formatted_prompt += "The user wants you to continue the conversation with the other AI assistants. Please respond to the previous messages and continue the discussion."
            else:
                formatted_prompt += "Please continue the conversation as an assistant. Respond directly to the last message without adding 'Assistant:' or similar prefixes to your response."
            
            print(f"Formatted prompt for {model}")
            
            # Get response from the appropriate model
            print(f"Calling {model} API...")
            response = ""
            if model == "gemini-2_0-flash":
                response = gemini_2_0_flash_chat(formatted_prompt)
            elif model == "gemini-2_0-flash-lite":
                response = gemini_2_0_flash_lite_chat(formatted_prompt)
            elif model == "openai-o1-mini":
                response = openai_gpt_o1_mini_chat(formatted_prompt)
            elif model == "openai-o3-mini":
                response = openai_gpt_o3_mini_chat(formatted_prompt)
            elif model == "openai-o1":
                response = openai_gpt_o1_chat(formatted_prompt)
            elif model == "openai-4o-mini":
                response = openai_gpt_4o_mini_chat(formatted_prompt)
            elif model == "claude_3_7_sonnet":
                response = claude_3_7_sonnet_chat(formatted_prompt)
            elif model == "claude_3_opus":
                response = claude_3_opus_chat(formatted_prompt)
            elif model == "claude_3_5_sonnet":
                response = claude_3_5_sonnet_chat(formatted_prompt)
            elif model == "claude_3_5_haiku":
                response = claude_3_5_haiku_chat(formatted_prompt)
            elif model == "claude_3_haiku":
                response = claude_3_haiku_chat(formatted_prompt)
            elif model == "deepseek_chat":
                response = deepseek_chatx2(formatted_prompt)
            elif model == "deepseek_reasoner":
                response = deepseek_reasoner_chat(formatted_prompt)
            elif model == "llama3_3":
                response = llama_3_3_tog_chat(formatted_prompt)
            else:
                print(f"Unknown model: {model}")
                continue
                
            # Clean up the response
            if response.startswith("Assistant:"):
                response = response[10:].strip()
                
            print(f"Got response from {model}: {response[:50]}...")
            
            # Add the model's response to the conversation history
            try:
                add_to_conversation("assistant", response, model)
                print(f"Added {model} response to conversation")
            except Exception as e:
                print(f"Error adding {model} response to conversation: {str(e)}")
            
            # Add to the responses list
            responses.append({
                "model": model,
                "response": response
            })
            print(f"Added {model} response to responses list")
        except Exception as e:
            print(f"Error processing model {model}: {str(e)}")
            # Continue with other models instead of failing completely
            responses.append({
                "model": model,
                "response": f"Error: {str(e)}"
            })
    
    print(f"Returning {len(responses)} responses")
    return responses

def clean_conversation_history():
    """Clean up the conversation history by removing duplicate messages and fixing role confusion"""
    try:
        # Get the current history
        history = get_conversation_history()
        
        # Clear the current history
        clear_conversation_history()
        
        # Process and re-add messages
        last_role = None
        last_content = None
        
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            
            # Skip assistant messages that are actually user messages
            if role == "assistant" and content.startswith("User:"):
                # Extract the actual user message
                user_content = content[5:].strip()
                # Add it as a user message instead
                add_to_conversation("user", user_content, None)
                last_role = "user"
                last_content = user_content
                continue
            
            # Skip duplicate messages
            if role == last_role and content == last_content:
                continue
                
            # Extract model if present in content
            model = None
            if role == "assistant" and "[" in content and "]" in content:
                start_idx = content.find("[")
                end_idx = content.find("]")
                if start_idx < end_idx and start_idx == 0:
                    model_name = content[start_idx+1:end_idx]
                    content = content[end_idx+1:].strip()
                    model = model_name
            
            # Add the message
            add_to_conversation(role, content, model)
            last_role = role
            last_content = content
            
        return True
    except Exception as e:
        print(f"Error cleaning conversation history: {str(e)}")
        return False

if __name__ == "__main__":
    app.run(debug=True)
