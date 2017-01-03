# easybot
Learn to implement a chat bot with deep learning. 

The first version is based on: [tensorflow_chatbot](https://github.com/llSourcell/tensorflow_chatbot) from llSourcell.

# usage
execute.py为Python主程序，程序有三种模式：训练、测试和服务，可通过修改配置文件 seq2seq.ini 来改变模式，如训练模式：

mode = train
然后运行如下命令启动程序：

python execute.py
测试模式：

mode = test
*注意：服务模式请直接启动 webui/app.py （需预先安装 Flask 环境，见setup.sh/requirements.txt）：

python webui/app.py
若需后台运行，请使用启动脚本：

sh webui/startup.sh
