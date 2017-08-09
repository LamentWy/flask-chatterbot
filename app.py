# -*- coding: utf-8 -*-

from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


app = Flask(__name__)

Lament = ChatBot("Lament",
                 storage_adapter="chatterbot.storage.SQLStorageAdapter",
                 database='./database.sqlite.2')

Lament.set_trainer(ChatterBotCorpusTrainer)
Lament.train("chatterbot.corpus.chinese")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat/<string:query>")
def get_raw_response(query):

    print type(query)

    temp = Lament.get_response(query)

    res = Lament.get_response(query).text

    return res.encode('utf-8')

@app.route("/train/<string:question>/<string:answer>")
def train_myrobot(question,answer):

    #question = "你叫什么名字"
    #answer = "请叫我小短君"
    Lament.set_trainer(ListTrainer)
    # Lament.train([question.decode('utf-8'),answer.decode('utf-8')])
    Lament.train([question,answer])

    return 'sucess!'

if __name__ == "__main__":
    app.run()
