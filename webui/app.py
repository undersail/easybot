from flask import Flask, render_template, request, make_response
from flask import jsonify

import time  
import hashlib

try:  
    import xml.etree.cElementTree as ET  
except ImportError:  
    import xml.etree.ElementTree as ET

import MySQLdb
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='xxxx',
        passwd='xxxxxxxx',
        db ='xxxxxxxx',
        )
cur = conn.cursor()

app = Flask(__name__,static_url_path="/static") 

#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    req_msg = request.form['msg']
    res_msg = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, req_msg )
    res_msg = res_msg.replace('_UNK', '^_^')

    #insert msg to db
    sql = "insert into t_dialogs(dialog_type, dialog_time, req_msg, res_msg, req_user, res_user, remark) values('webpage',%d,'%s','%s','%s','%s','')"
    cur.execute(sql % (int(time.time()), MySQLdb.escape_string(req_msg), MySQLdb.escape_string(res_msg), 'websession', 'easybot'))
    conn.commit()
    return jsonify( { 'text': res_msg } )

# Wechat auth
@app.route('/wechat', methods = ['GET', 'POST'] )  
def wechat():  
  # auth
  if request.method == 'GET':  
    token = 'easybot_wechat' # token  
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
  # reply
  if request.method == 'POST':
    # Get the infomations from the recv_xml.  
    xml_recv = ET.fromstring(request.data)  
    ToUserName = xml_recv.find("ToUserName").text  
    FromUserName = xml_recv.find("FromUserName").text  
    Content = xml_recv.find("Content").text
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    res_msg = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, Content)
    res_msg = res_msg.replace('_UNK', '^_^')

    #insert msg to db
    sql = "insert into t_dialogs(dialog_type, dialog_time, req_msg, res_msg, req_user, res_user, remark) values('wechat',%d,'%s','%s','%s','%s','')"
    cur.execute(sql % (int(time.time()), MySQLdb.escape_string(Content), MySQLdb.escape_string(res_msg), MySQLdb.escape_string(FromUserName), 'easybot'))
    conn.commit()

    response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), res_msg ) )
    response.content_type = 'application/xml'  
    return response 

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
