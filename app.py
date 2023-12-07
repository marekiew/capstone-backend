import os

from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

allMessages = {}
directory = os.getcwd() + "/build"

@app.get('/chats')
def get_chats():
    print("request received")
    return list(allMessages.keys())

@app.get('/messages/<chat_number>')
def get_messages(chat_number):
    print("request received")
    print(allMessages.get(chat_number))
    return allMessages.get(chat_number, [])

@app.post('/messages/<chat_number>')
def store_message(chat_number):
    print(f"""request post received: {request.data}""")
    chat_list = allMessages.get(chat_number, [])
    chat_list.append(request.json)
    allMessages[chat_number] = chat_list
    return 'message success'


directory= os.getcwd() + '/build/static'


@app.route('/')
def index():
    path= os.getcwd() + '/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

#
@app.route('/static/<folder>/<file>')
def css(folder,file):
    ''' User will call with with thier id to store the symbol as registered'''

    path = folder+'/'+file
    return send_from_directory(directory=directory,path=path)



if __name__ == '__main__':
    app.run()