#!/bin/bash




PYTHON_PATH=/usr/bin/python

DAEMON=`echo ~/twister/bin/start_client.py`

LOG_PATH=`echo ~/twister/twisterclient.log`

NAME=twisterclient
DESC="twister client"


STATUS=$(ps ax | grep python | grep start_client.py)
EPSTATUS=$(ps ax | grep python | grep ExecutionProcess.py)




test -f $DAEMON || exit 0

set -e

case "$1" in
  start)
        echo -n ">>>>||||  Starting $DESC: "

        if [ -n "$STATUS" ]
        then
            echo already running..
            ps ax | grep python | grep start_client.py
        else
            nohup $PYTHON_PATH -u $DAEMON > $LOG_PATH &
        fi

        echo "$NAME.  ||||<<<<<"
        ;;

  stop)
        echo -n ">>>>||||  Stopping $DESC: "

        if [ -n "$EPSTATUS" ]
        then
            kill -9 `ps ax | grep python | grep ExecutionProcess.py | awk '{print $1}'`
        fi

        if [ -n "$STATUS" ]
        then
            kill -9 `ps ax | grep python | grep start_client.py | awk '{print $1}'`
        fi

        echo "$NAME.  ||||<<<<"
        ;;

  restart)
        echo -n ">>>>||||  Restarting $DESC: "

        if [ -n "$EPSTATUS" ]
        then
            kill -9 `ps ax | grep python | grep ExecutionProcess.py | awk '{print $1}'`
        fi

        if [ -n "$STATUS" ]
        then
            kill -9 `ps ax | grep python | grep start_client.py | awk '{print $1}'`
        fi

        nohup $PYTHON_PATH -u $DAEMON > $LOG_PATH &

        echo "$NAME.  ||||<<<<"
        ;;

  status)
        echo -n ">>>>||||  Status $DESC: "
        echo -e "\n"

        if [ -n "$STATUS" ]
        then
            ps ax | grep python | grep start_client.py
            echo -e "\n"
            ps ax | grep python | grep ExecutionProcess.py
        else
            echo not running..
        fi

        echo -e "\n"
        echo "$NAME.  ||||<<<<"
        ;;

  *)
        echo ">>>>||||  Usage: "$1" {start|stop|restart|status}  ||||<<<<"
        exit 1

esac

exit 0
