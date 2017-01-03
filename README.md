# easybot
Learn to implement a chat bot with deep learning. 

The first version is based on: [tensorflow_chatbot](https://github.com/llSourcell/tensorflow_chatbot) from llSourcell.

# usage

1. Put the dataset into easybot/data/
[How to get the sample dataset](https://github.com/suriyadeepan/datasets) 

2. Change seq2seq.ini to switch to the training mode：

`mode = train`

3. Start training

`python execute.py`

4. Testing
You can stop the training anytime, the trained model will be saved easybot/in working_dir/
Change seq2seq.ini to switch to the testing mode, then start execute.py：

`mode = test
python execute.py
`

5. All the code for serve mode is in easybot/webui/
- Main app: 

`python webui/app.py`

- Startup/Shutdown:

`sh webui/startup.sh
sh webui/shutdown.sh`

- Background runing:

`sh webui/startup.sh`

- App Daemon:

`sh webui/app-daemon.sh`

- Archive log:

`sh webui/archivelog.sh`

6. Demonstration snapshot:

[http://www.easyapple.net/?p=1384](http://www.easyapple.net/?p=1384) 

