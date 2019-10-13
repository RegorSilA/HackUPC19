from flask import Flask, flash, redirect, url_for, request, render_template
import time
import datetime
import serial
import telegram 
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters
import traceback
import heat

app = Flask(__name__, template_folder='./')
TOKEN = '969063074:AAH16iWup3H8bQvWxmwPBMgJeKmoPnkCcgA'
global ftime
global heatstat
global heattime
global is_ard
heatstat = -1
ftime=0
is_ard=False

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
    if heatstat == -1:
        return redirect(url_for('setup'))
    elif heatstat == 0 or heatstat == 1 or heatstat == 2:
        return redirect(url_for('timer', stat=heatstat))

@app.route('/timer')
def clock():
    return "{}".format(heatstat)

@app.route('/setup/', methods=["GET", "POST"])
def setup():
    if request.method == 'POST':
        temp = request.form['temp']
        return redirect(url_for('mode', temp=temp))
    return render_template('setup.html')

@app.route('/mode<string:temp>', methods=["GET", "POST"])
def mode(temp):
    global ftime
    if request.method == 'POST':
        if request.form['action'] == 'Turn on now':
            heatstat = 1
            if is_ard:
                return redirect(url_for('main', temp=temp, ftime_var=ftime, mode='now', roomtemp=roomtemp(ard)))
            else:
                return redirect(url_for('main', temp=temp, ftime_var=ftime, mode='now', roomtemp=False))
        elif request.form['action'] == 'Schedule':
            return redirect(url_for('setup_schedule', temp=temp))
    else:
        return render_template('setup_mode.html')

@app.route('/setup_schedule<string:temp>', methods=["GET", "POST"])
def setup_schedule(temp):
    if request.method == 'POST':
        ftime = request.form['time']
        strtime = time.strptime(ftime, "%H:%M")
        heatstat = 0
        try:
            return redirect(url_for('main', temp=temp, ftime_var=ftime, mode='schedule',roomtemp=roomtemp(ard)))
        except:
            return redirect(url_for('main', temp=temp, ftime_var=ftime, mode='schedule',roomtemp=False))            
    return render_template('setup_schedule.html')

@app.route('/main<string:temp>%<string:mode>%<string:ftime_var>%<string:roomtemp>', methods=["GET", "POST"])
def main(temp, ftime_var, mode, roomtemp):
    global heattime
    global ftime
    global heatstat
    ftime = ftime_var

    if True:
        if roomtemp!='False':
            string1 = "Room temperature: {}ºC\n".format(roomtemp)
        else:
            string1 = ""
        if mode=='now':
            # que et digui quant trigarà
            heattime = heat.TTiming(float(temp))
            ftime = datetime.datetime.now()+heattime
            string2 = "The room will be heated by {}".format(datetime.datetime.strftime(ftime, "%H:%M"))
            
        elif mode=='schedule':
            heattime = heat.TTiming(float(temp))
            itime = datetime.datetime.strptime(ftime, "%H:%M")-heattime
            string2 = "The room will start to be heated at {}. \n It will be finished by {}.".format(datetime.datetime.strftime(itime, "%H:%M"),
                datetime.datetime.strftime(itime+heattime, "%H:%M"))

    return render_template('main.html', value1=string1, value2=string2)

#redirect(url_for('econ_intro', temp=temp))

@app.route('/econ_intro<string:temp>', methods=["GET", "POST"])
def paraules(temp):
    return "Hola"


if __name__ == '__main__':
    # ARDUINO
    port = 'COM6'
    print('Detecting Arduino...')
    c = 0
    while not is_ard and c<5:
        c += 1
        try:
            ard = serial.Serial(port,9600)
        except:
            time.sleep(1.0)
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