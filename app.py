# -*- coding:utf-8 -*-
from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

chinese_bot = ChatBot("Chinese Bot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

chinese_bot.set_trainer(ChatterBotCorpusTrainer)
chinese_bot.train("chatterbot.corpus.chinese")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get/<string:query>")
def get_raw_response(query):
    return str(chinese_bot.get_response(query))


if __name__ == "__main__":
    app.run()
