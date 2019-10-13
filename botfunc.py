from flask import Flask, redirect, url_for, request, render_template
import time
import datetime
import serial
import telegram 
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters
from hwh import *
from hwh import ard
import traceback

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
                msg.reply_text('The room temperature is {}ºC.\nRemaining time: {}h'.format(roomtemp(ard), datetime.strftime(est, "%H:%M")))
            else:
                msg.reply_text('The room temperature is {}ºC.\nThe room is already heated.'.format(roomtemp(ard)))
        except:
            msg.reply_text('The room temperature is {}ºC.\nThe room is already heated.'.format(roomtemp(ard)))
    except:
        traceback.print_exc()