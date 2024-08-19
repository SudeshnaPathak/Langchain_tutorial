import requests
from langchain.memory import ChatMessageHistory
history = ChatMessageHistory()

def get_serializable_history():
    # Convert message history to a serializable format
    # [{'type': 'human', 'content': 'Hello'}, {'type': 'ai', 'content': 'Hello! How can I assist you today?'}]
    return [{"type": msg.type, "content": msg.content} for msg in history.messages]

def get_response(question):
    data = {
        "input": {
            "question": question,
            "messages": get_serializable_history()
        }
    }
    response = requests.post("http://localhost:8000/chain/invoke", json = data)
    
    history.add_user_message(question)
    history.add_ai_message(response.json()['output'])
    return response.json()['output']

if __name__ == "__main__":
    while True:
        question = input("Ask me a question: ")
        print(get_response(question)) 
    
        
