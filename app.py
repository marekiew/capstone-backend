import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, send_from_directory, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    chat_room = db.Column(db.String(50))

allMessages = {}
directory = os.getcwd() + "/build"

@app.get('/chats')
def get_chats():
    print("request received")
    return list(allMessages.keys())

@app.get('/messages/<chat_number>')
def get_messages(chat_number):
    return allMessages.get(chat_number, [])

@app.post('/messages/<chat_number>')
def store_message(chat_number):
    print(f"""request post received: {request.data}""")
    chat_list = allMessages.get(chat_number, [])
    chat_list.append(request.json)
    allMessages[chat_number] = chat_list
    
    content = request.json.get('content')
    new_message = Message(content=content, chat_room=chat_number)
    db.session.add(new_message)
    db.session.commit()
    return 'message success'


@app.delete('/chats')
def delete_chats():
    global allMessages
    allMessages = {}
    return 'All chat rooms deleted successfully'

if __name__ == '__main__':
    app.run()