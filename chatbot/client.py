import requests

response = requests.post("http://localhost:8000/chain/invoke", json = {"input" : {"language": "italian", "text": "hi"}})

print(response.json()['output'])
    
# from langserve import RemoteRunnable

# remote_chain = RemoteRunnable("http://localhost:8080/chain/")
# print(remote_chain.invoke({"language": "italian", "text": "hi"}))