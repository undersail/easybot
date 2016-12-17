from flask import Flask, render_template, request, make_response
from flask import jsonify

import time  
import hashlib

try:  
    import xml.etree.cElementTree as ET  
except ImportError:  
    import xml.etree.ElementTree as ET

app = Flask(__name__,static_url_path="/static") 

#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    return jsonify( { 'text': execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, request.form['msg'] ) } )

# Wechat auth
@app.route('/wechat', methods = ['GET', 'POST'] )  
def wechat_auth():  
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
  if request.method == 'POST':
    # Get the infomations from the recv_xml.  
    xml_recv = ET.fromstring(request.data)  
    ToUserName = xml_recv.find("ToUserName").text  
    FromUserName = xml_recv.find("FromUserName").text  
    Content = xml_recv.find("Content").text
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    reply_msg = execute.decode_line(sess, model, enc_vocab, rev_dec_vocab, Content)
    response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), reply_msg ) )
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
