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
		act=$(stat -c %Y ./app.log)
		cur=$(date +%s)
		span=$[$cur - $act]
		timeout=600
		if [ ${span} -gt ${timeout} ]
		then
			echo inactive time more than ${timeout} seconds, about to restart.
			sh ./archivelog.sh
			sh ./shutdown.sh
		else
			echo last active time is ${span} seconds ago.
		fi
	fi
	sleep 10

done

echo "stop checking."
