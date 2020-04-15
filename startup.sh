while true;
do
    python sample/flask/webapi.py |& tee -a webapi-startup.log
done

