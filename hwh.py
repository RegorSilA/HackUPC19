from flask import Flask, flash, redirect, url_for, request, render_template
import time
import datetime
import serial
import telegram 
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters
import traceback

app = Flask(__name__, template_folder='./')
TOKEN = '969063074:AAH16iWup3H8bQvWxmwPBMgJeKmoPnkCcgA'
heatstat = -1

def roomtemp(ard):
    while ard.inWaiting()==0:
        pass
    temp = str(ard.readline(), 'utf-8').split()
    return int(float(temp[0]))

def error(func):
    print("Error in", func)
    traceback.print_exc()

def start(bot, update):
    msg = update.message
    try:
        msg.reply_text('Hello!')
    except:
        boterror('start')

def get_help(bot, update):
    pass

def stats(bot, update):
    try:
        msg = update.message
        now = datetime.datetime.now()
        ftime=datetime.datetime.now()+datetime.timedelta(minutes=20)
        try:
            if now < ftime:
                est = ftime-now
                msg.reply_text('The room temperature is {}ºC.\nRemaining time: {}:{}h'.format(roomtemp(ard), est.seconds//3600, (est.seconds//60)%60))
            else:
                msg.reply_text('The room temperature is {}ºC.\nThe room is already heated.'.format(roomtemp(ard)))
        except:
            msg.reply_text('The room is already heated.')
    except:
        traceback.print_exc()

@app.route('/')
def initiate():
    return redirect(url_for('setup'))

@app.route('/setup/', methods=["GET", "POST"])
def setup():
    if request.method == 'POST':
        temp = request.form['temp']
        return redirect(url_for('mode', temp=temp))
    heatstat = 0
    return render_template('setup.html')

@app.route('/mode<string:temp>', methods=["GET", "POST"])
def mode(temp):
    if request.method == 'POST':
        if request.form['action'] == 'Turn on now':
            try:
                return redirect(url_for('main', temp=temp, ftime='0', mode='now', roomtemp=roomtemp(ard)))
            except:
                return redirect(url_for('main', temp=temp, ftime='0', mode='now', roomtemp=False))
        elif request.form['action'] == 'Schedule':
            return redirect(url_for('setup_schedule', temp=temp))
    else:
        return render_template('setup_mode.html')

@app.route('/setup_schedule<string:temp>', methods=["GET", "POST"])
def setup_schedule(temp):
    if request.method == 'POST':
        ftime = request.form['time']
        strtime = time.strptime(ftime, "%H:%M:%S")
        heatstat = 0
        try:
            return redirect(url_for('main', temp=temp, ftime=ftime, mode='schedule',roomtemp=roomtemp(ard)))
        except:
            return redirect(url_for('main', temp=temp, ftime=ftime, mode='schedule',roomtemp=False))            
    return render_template('setup_schedule.html')

@app.route('/main<string:temp>%<string:mode>%<string:ftime>%<string:roomtemp>', methods=["GET", "POST"])
def main(temp, ftime, mode, roomtemp):
    if mode=='now':
        pass
    elif mode=='schedule':
        pass
    if roomtemp!='False':
        string1 = "Room temperature: {}ºC\n".format(roomtemp)
    else:
        string1 = ""
    if heatstat == 0:
        string2 = "The room is being heated."
    else:
        string2 = "The room is already heated."
    return string1+string2

if __name__ == '__main__':
    # ARDUINO
    port = 'COM6'
    print('Detecting Arduino...')
    is_ard = False
    c = 0
    while not is_ard and c<5:
        c += 1
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