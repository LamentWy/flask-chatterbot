# -*- coding: utf-8 -*-

from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from flask import request
import hashlib

import wxmsg
import towxmsg

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

    res = Lament.get_response(query).text

    return res.encode('utf-8')

@app.route("/train/<string:question>/<string:answer>")
def train_myrobot(question,answer):

    #question = "你叫什么名字"
    #answer = "请叫我小短君"
    Lament.set_trainer(ListTrainer)
    # Lament.train([question.decode('utf-8'),answer.decode('utf-8')])
    Lament.train([question,answer])

    return '小短get了新技能!'.encode('utf-8')

'''
    /wxcheck get  微信公众平台用来校验开发者身份的
'''
@app.route("/wxcheck" , methods = ['GET'])
def check_token_from_wx():

    #  args : A MultiDict with the parsed contents of the query string.
    in_data = request.args

    signature = in_data.get('signature')

    timestamp = in_data.get('timestamp')
    nonce = in_data.get('nonce')
    echostr = in_data.get('echostr')

    token = "lament"  # 请按照公众平台官网\基本配置中信息填写
    # 将 token, timestamp, nonce字典序排序得到字符串list
    list = [token, timestamp, nonce]
    list.sort()

    #加密
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    print "handle/GET func: hashcode, signature: ", hashcode, signature
    # 如果相等则返回 echostr ，失败则return ""
    if hashcode == signature:
        return echostr
    else:
        return ""




'''
/wxcheck  post  微信平台使用post请求 将用户发送的消息 以xml的形式发送到我们的服务器上
'''
@app.route("/wxcheck" , methods = ['POST'])
def recive_msg_from_wx():
    #  Contains the incoming request data as string in case it came with a mimetype Flask does not handle.
    wx_data_str = request.data

    print wx_data_str
    receive_msg = wxmsg.parse_xml(wx_data_str)
    print "-------"
    print isinstance(receive_msg,wxmsg.Msg)
    print "==========="
    print receive_msg.MsgType == "text"

    print ""

    if isinstance(receive_msg,wxmsg.Msg) and receive_msg.MsgType == 'text':

        toUser = receive_msg.FromUserName
        fromUser = receive_msg.ToUserName
        content = Lament.get_response(receive_msg.Content.decode('utf-8')).text.encode('utf-8')

        replyMsg = towxmsg.TextMsg(toUser, fromUser, content)
        return replyMsg.send()
    else:
        print "未知消息，暂不处理"
        # 下面return 的 success只是为了让微信不要再尝试重复推送消息了
        return "success"





if __name__ == "__main__":
    app.run()
