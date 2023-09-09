#!/bin/sh
ngrok http 5000 --hostname=saati.ngrok.dev &
python app.py &
python recieve.py &
python receive.py &
python receive.py &
wait
