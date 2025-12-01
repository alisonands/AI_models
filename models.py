from google import genai
from openai import OpenAI
from SECRETS import gemini_api_key, openai_api_key, claude_api_key, together_llama_api_key, deepseek_api_key
import requests #llama
from together import Together #llama
import anthropic #claude
from sqlalchemy import create_engine, text
from datetime import datetime
import os
from openai import OpenAI

# --------------------------
# ---------GEMINI-----------
# --------------------------
gemini_conversation_history = []
gemini_client = OpenAI(api_key=gemini_api_key, 
                       base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# --------genai-2.5---------
def gemini_2_5_pro_chat(prompt):
    gemini_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = gemini_client.chat.completions.create(
        messages=gemini_conversation_history,
        model="gemini-2.5-pro-exp-03-25",
        stream=False
        )
    
    gemini_response = response.choices[0].message.content
    print('Gemini:', gemini_response)
    
    gemini_conversation_history.append(
        {"role": "assistant", "content": gemini_response}
    )

    return gemini_response

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

# --------- 4o-mini ----------
# function calling openai api 
def openai_gpt_4o_mini_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI 4o-mini:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response

# ----------- 4o ------------
def openai_gpt_4o_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=openai_conversation_history,
        store=False
        )
    
    openai_response = response.choices[0].message.content
    print('openAI 4o:', openai_response)
    
    openai_conversation_history.append(
        {"role": "assistant", "content": openai_response}
    )

    return openai_response

# ----------- 4.5 preview ------------
def openai_gpt_4_5_preview_chat(prompt):

    openai_conversation_history.append(
        {"role": "user", "content": prompt}
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o",
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
        model="deepseek-reasoner",
        messages=deepseek_conversation_history,
        stream=False
    )

    deepseek_response = response.choices[0].message.content
    print('Deepseek reasoner:', deepseek_response)

    deepseek_conversation_history.append(
        {"role": "assistant", "content": deepseek_response}
    )

    return deepseek_response

# database connection - SQLite
sqlite_path = os.path.join(os.path.dirname(__file__), "conversation.db")
database_path = f"sqlite:///{sqlite_path}"
engine = create_engine(database_path)

# Create the table if it doesn't exist
with engine.connect() as connection:
    connection.execute(text('''
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        model TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    '''))
    connection.commit()
print("Connected to SQLite database")

# Function to add a message to the conversation database
def add_to_conversation(role, content, model=None):
    with engine.connect() as connection:
        query = text("INSERT INTO prompts(role, content, model) VALUES(:role, :content, :model)")
        connection.execute(query, {"role": role, "content": content, "model": model})
        connection.commit()

# Function to get the full conversation history
def get_conversation_history():
    with engine.connect() as connection:
        query = text("SELECT role, model, content FROM prompts ORDER BY id")
        result = connection.execute(query)
        
        history = []
        for row in result:
            role = row.role
            model = row.model
            content = row.content
            
            if model:
                formatted_content = f"[{model}] {content}"
            else:
                formatted_content = content
                
            history.append({"role": role, "content": formatted_content})
        
        return history

# Function to clear the conversation history
def clear_conversation_history():
    with engine.connect() as connection:
        delete_query = text('DELETE FROM prompts')
        connection.execute(delete_query)
        connection.commit()

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
            if model == "gemini-2_5-pro":
                response = gemini_2_5_pro_chat(formatted_prompt)
            elif model == "gemini-2_0-flash":
                response = gemini_2_0_flash_chat(formatted_prompt)
            elif model == "gemini-2_0-flash-lite":
                response = gemini_2_0_flash_lite_chat(formatted_prompt)
            elif model == "openai-o1-mini":
                response = openai_gpt_o1_mini_chat(formatted_prompt)
            elif model == "openai-o3-mini":
                response = openai_gpt_o3_mini_chat(formatted_prompt)
            elif model == "openai-o1":
                response = openai_gpt_o1_chat(formatted_prompt)
            elif model == "openai-4o":
                response = openai_gpt_4o_chat(formatted_prompt)
            elif model == "openai-4o-mini":
                response = openai_gpt_4o_mini_chat(formatted_prompt)
            elif model == "openai-4_5_preview":
                response = openai_gpt_4_5_preview_chat(formatted_prompt)
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

# Update the reset function to also clear the conversation database
def reset_all_conversations():
    global openai_conversation_history, claude_conversation_history, llama_conversation_history, genai_chat2_0, genai_chat2_0_lite
    
    # Reset OpenAI conversation history
    openai_conversation_history.clear()
    
    # Reset Claude conversation history
    claude_conversation_history.clear()
    
    # Reset Llama conversation history
    llama_conversation_history.clear()
    
    # Reset Gemini conversation
    global genai_client
    genai_chat2_0 = genai_client.chats.create(model='gemini-2.0-flash')
    genai_chat2_0_lite = genai_client.chats.create(model='gemini-2.0-flash-lite')
    
    # Clear the conversation database
    clear_conversation_history()
    
    print("All conversation histories have been reset")
    return True

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