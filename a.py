from flask import Flask, request, render_template
import time
app = Flask(__name__, template_folder='./')

@app.route('/setup/', methods=["GET", "POST"])
def setup():
    global temp
    global strtime
    if request.method == 'POST':
        temp = request.form['temp']
        ftime = request.form['time']
        strtime = time.strptime(ftime, "%H:%M:%S")
        return "Thank you. Your room's temperature will be {}ºC at {}.".format(temp, ftime)
    return render_template('setup.html')
    #print(args)
    #return('Tomàquet')
'''
def setup2():
    return render_template('setup.html')
'''

@app.route('/setup/now')
def now():
    return "Now"

@app.route('/setup/schedule')
def schedule():
    return "Schedule"

if __name__ == '__main__':
    app.run(port='69')