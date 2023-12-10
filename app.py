import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient("mongodb+srv://markpetrov010:ZDX7k8hrVxvzNXmT@cluster0.kqmvxqq.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
chats = db.chats

allMessages = {}
directory = os.getcwd() + "/build"

@app.get('/api/chats')
def get_chats():
    print("request received")
    chat_list = list()
    for chat_id in chats.find({}):
        chat_list.append(chat_id['_id'])
    return chat_list

@app.get('/api/messages/<chat_number>')
def get_messages(chat_number):
    chat = chats.find_one({'_id': chat_number})
    print("testing")
    if chat == None:
        return []
    return chats.find_one({'_id': chat_number})['chat']

@app.post('/api/messages/<chat_number>')
def store_message(chat_number):
    print(f"""request post received: {request.data}""")
    chat = chats.find_one({'_id': chat_number})
    if chat == None:
        chat = {'_id': chat_number, 'chat': [request.json]}
        chats.insert_one(chat)
    else:
        chats.update_one({'_id': chat_number},{'$push': {'chat': request.json}})
    return 'message added'

@app.delete('/api/chats')
def delete_chats():
    chats.delete_many({})
    return 'All chat rooms deleted successfully'

if __name__ == '__main__':
    app.run()