LOGFILE=$(date +applog_%Y%m%d_%H%M%S.log)
mv ./app.log ./logs/${LOGFILE}
echo ${LOGFILE} archived
touch app.log
