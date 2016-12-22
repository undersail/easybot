echo "start checking ..."
date

while true
do

	ps -fe | grep app.py | grep -v grep
	if [ $? -ne 0 ]
	then
		echo "app.py is not running, will start now"
		sh ./startup.sh
	else
		echo "app.py is running."
	fi
	sleep 10

done

echo "stop checking."
