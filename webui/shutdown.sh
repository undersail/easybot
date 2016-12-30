echo "stopping..."
kill $(ps -ef | grep "app.py" | awk '{print $2}')
