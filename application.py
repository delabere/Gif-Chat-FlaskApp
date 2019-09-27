import os

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import json

# temporary application data for teting socketio
messages = ['First message', 'Second message']


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/start")
def home():
    return render_template('start.html')

@app.route("/", methods=['GET', 'POST'])
@app.route("/chat", methods=['GET', 'POST'])
def index():
    with open('data.json', mode='r') as f:
        data = json.load(f)
    return render_template('chat.html', data=data)


@socketio.on("send message")
def vote(data):
    message = data["message"]
    messages.append(message)
    print(messages)
    emit("all messages", messages, broadcast=True)


# if not run like this then SocketIO error is raised
if __name__ == "__main__":
    socketio.run(app)
