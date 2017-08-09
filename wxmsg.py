# -*- coding: utf-8 -*-
# filename : wxmsg   微信公众平台定义的消息格式

import xml.etree.ElementTree as ET


'''
   按照wx平台定义的消息的xml结构 解析消息类型，目前只解析了文本和图片消息
   各种消息类型的xml数据包格式说明：
   wx->us :https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140453
'''
def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)

    # 获取MsgType结点，然后判断消息类型
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


# 下面是不同类型的wxMsg

'''
  文本消息
'''
class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

'''
  图片消息
'''
class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text
