from flask import Flask, render_template, request, make_response
from flask import jsonify

import sys
import time  
import hashlib
import threading

def heartbeat():
    print time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time()))
    timer = threading.Timer(60, heartbeat)
    timer.start()
timer = threading.Timer(60, heartbeat)
timer.start()

try:  
    import xml.etree.cElementTree as ET  
except ImportError:  
    import xml.etree.ElementTree as ET

import MySQLdb
conn= MySQLdb.connect(
        host='localhost',
        port = 1234,
        user='xxxx',
        passwd='xxxxxxxx',
        db ='xxxxxxxx',
        )

import re
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

app = Flask(__name__,static_url_path="/static") 

#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    req_msg = request.form['msg']
    res_msg = '^_^'
    
    # ensure not Chinese
    match = zhPattern.search(req_msg)
    if match:
      res_msg = "Sorry, I can't speak Chinese right now, maybe later."
    else:
      res_msg = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, req_msg )
    res_msg = res_msg.replace('_UNK', '^_^')
    
    # ensure not empty
    if res_msg == '':
      res_msg = 'Let me think about it ...'

    return jsonify( { 'text': res_msg } )

    #insert msg to db
    sql = "insert into t_dialogs(dialog_type, dialog_time, req_msg, res_msg, req_user, res_user, remark) values('webpage',%d,'%s','%s','%s','%s','')"
    cur = conn.cursor()
    cur.execute(sql % (int(time.time()), MySQLdb.escape_string(req_msg), MySQLdb.escape_string(res_msg), 'websession', 'easybot'))
    conn.commit()
    conn.close()

# Wechat auth
@app.route('/wechat', methods = ['GET', 'POST'] )  
def wechat():  
  # auth
  """
  if request.method == 'GET':  
    token = 'xxxxxxxx' # token  
    query = request.args  
    signature = query.get('signature', '')  
    timestamp = query.get('timestamp', '')  
    nonce = query.get('nonce', '')  
    echostr = query.get('echostr', '')  
    s = [timestamp, nonce, token]  
    s.sort()  
    s = ''.join(s)  
    if ( hashlib.sha1(s).hexdigest() == signature ):    
      return make_response(echostr)  
  """
  # reply
  if request.method == 'POST':
    req_msg = 'Hi'
    res_msg = '^_^'
    remark = ''
    # Get the infomations from the recv_xml.  
    xml_recv = ET.fromstring(request.data)  
    toUserName = xml_recv.find("ToUserName").text  
    fromUserName = xml_recv.find("FromUserName").text  
    # createTime = xml_recv.find("CreateTime").text
    # msgId = xml_recv.find("MsgId").text
    msgType = xml_recv.find("MsgType").text
    if msgType == 'text':
      content = xml_recv.find("Content").text
      req_msg = content
      res_msg = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, req_msg)
      res_msg = res_msg.replace('_UNK', '^_^')
      remark = 'text'
    elif msgType == 'image':
      picUrl = xml_recv.find("PicUrl").text
      # mediaId = xmlrecv.find("MediaId").text
      req_msg = picUrl
      res_msg = 'So you sent me a picture?\r\n' + picUrl
      remark = 'image'
    elif msgType == 'voice':
      # mediaId = xmlrecv.find("MediaId").text
      # format = xmlrecv.find("Format").text
      recognition = xml_recv.find("Recognition").text
      req_msg = recognition
      if req_msg != None and  req_msg != '':
        res_msg = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, req_msg)
        res_msg = res_msg.replace('_UNK', '^_^')
        res_msg = 'Do you mean: ' + req_msg + '?\r\n' + res_msg
      else:
        req_msg = 'unknown'
        res_msg = 'What are you saying about?'
      remark = 'voice'
    elif msgType == 'event':
      event = xml_recv.find("Event").text
      if event == 'subscribe':
        req_msg = 'Hi easybot, finally I found you!'
        res_msg = "Hey body, nice to meet you! Let's talk about what shall we do."
      elif event == 'unsubscribe':
        req_msg = 'Bye easybot, I think I will leave.'
        res_msg = 'So finally you will go? Bye! Best wishes!'
      remark = 'event'
    else:
      req_msg = 'unknown'
      res_msg = 'So can we speak normally? Or at least send me some normal thing, e.g. your naked picture.'
      remark = 'other'

    # ensure not Chinese
    match = zhPattern.search(req_msg)
    if match:
      res_msg = "Sorry, I can't speak Chinese right now, maybe later."
    
    # ensure not empty
    if res_msg == '':
      res_msg = 'Let me think about it ...'
  
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    response = make_response( reply % (fromUserName, toUserName, str(int(time.time())), res_msg ) )
    response.content_type = 'application/xml'  
    return response 

    #insert msg to db
    sql = "insert into t_dialogs(dialog_type, dialog_time, req_msg, res_msg, req_user, res_user, remark) values('wechat',%d,'%s','%s','%s','%s','%s')"
    cur = conn.cursor()
    cur.execute(sql % (int(time.time()), MySQLdb.escape_string(req_msg), MySQLdb.escape_string(res_msg), MySQLdb.escape_string(fromUserName), 'easybot', remark))
    conn.commit()
    conn.close()

@app.route("/")
def index(): 
    return render_template("index.html")
#############

'''
Init seq2seq model

    1. Call main from execute.py
    2. Create decode_line function that takes message as input
'''
#_________________________________________________________________
import tensorflow as tf
import execute

sess = tf.Session()
sess, model, enc_vocab, rev_dec_vocab = execute.init_session(sess, conf='seq2seq_serve.ini')
#_________________________________________________________________

# start app
if (__name__ == "__main__"): 
    app.run(host = '0.0.0.0', port = 80) 
