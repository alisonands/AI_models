from google import genai
from openai import OpenAI
from SECRETS import gemini_api_key, openai_api_key, claude_api_key, together_llama_api_key
import requests #llama
from together import Together #llama
import anthropic #claude

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
    llama_conversation_history.clear()
    
    # Reset Gemini conversation
    global genai_client
    genai_chat = genai_client.chats.create(model='gemini-2.0-flash')
    
    print("All conversation histories have been reset")
    return True