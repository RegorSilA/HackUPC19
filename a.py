from flask import Flask, redirect, url_for, request, render_template
import time
import datetime
import serial
import telegram 
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters
from botfunc import *

app = Flask(__name__, template_folder='./')
TOKEN = '969063074:AAH16iWup3H8bQvWxmwPBMgJeKmoPnkCcgA'



@app.route('/setup/', methods=["GET", "POST"])
def setup():
    if request.method == 'POST':
        temp = request.form['temp']
        return redirect(url_for('mode', temp=temp))
    return render_template('setup.html')

def roomtemp(ard):
    while ard.inWaiting()==0:
        pass
    temp = str(ard.readline(), 'utf-8').split()
    return int(float(temp[0]))

@app.route('/mode<string:temp>', methods=["GET", "POST"])
def mode(temp):
    if request.method == 'POST':
        if request.form['action'] == 'Turn on now':
            return redirect(url_for('main', temp=temp, ftime='0', mode='now', roomtemp=roomtemp(ard)))
        elif request.form['action'] == 'Schedule':
            return redirect(url_for('setup_schedule', temp=temp))
    else:
        return render_template('setup_mode.html')

@app.route('/setup_schedule<string:temp>', methods=["GET", "POST"])
def setup_schedule(temp):
    if request.method == 'POST':
        ftime = request.form['time']
        strtime = time.strptime(ftime, "%H:%M:%S")
        return redirect(url_for('main', temp=temp, ftime=ftime, mode='schedule',roomtemp=roomtemp(ard),finished=0))
    return render_template('setup_schedule.html')

@app.route('/main<string:temp>%<string:mode>%<string:ftime>%<string:roomtemp>%<string:finished>', methods=["GET", "POST"])
def main(temp, ftime, mode, roomtemp, finished):
    if mode=='now':
        pass
    elif mode=='schedule':
        pass
    return "Room temeperature: {}ºC".format(roomtemp)

if __name__ == '__main__':
    # ARDUINO
    port = 'COM6'
    print('Detecting Arduino...')
    is_ard = False
    while not is_ard:
        try:
            ard = serial.Serial(port,9600)
            time.sleep(1.0)
        except:
            continue
        print('Arduino detected in port {}'.format(port))
        is_ard = True
    # TELEGRAM BOT
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", get_help))
    dp.add_handler(CommandHandler("stats", stats))
    updater.start_polling()
    #updater.idle()
    # WEB APP
    app.run(port='69', threaded=True)