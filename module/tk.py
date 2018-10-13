# Python function
import datetime as dt
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import time
import os
from random import randrange
from string import Template
from functools import wraps
from urllib import request
from telegram import Bot, Chat, Sticker, ReplyKeyboardMarkup, Message
from telegram.error import *

# ---error log setting
import logging
logging.basicConfig(format='[%(asctime)s](%(levelname)s) %(name)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# do once var
do_once_value=True

# Record bot init time
init_time = datetime.now()
quote_search={} # Use on /quote
reply_pair={} # Use on catch reply
################################################
#                   tool kits                  #
################################################
# decorator
def do_once(function):
    """decorator for function do once"""
    global do_once_value
    if do_once_value:
        do_once_value=False
        return function

def c_tz(datetime,tz):
    t=datetime+timedelta(hours=tz)#轉換時區 tz為加減小時

def user_admin_value(t_msg):
    """Dectect user if admin, return boolen value"""
    uid=t_msg.from_user.id
    print(uid)
    if not isinstance(uid, int):
        raise TypeError("user_admin_value needs telegram.Message type.")
        return
    try:
        adminlist=t_msg.message.chat.get_administrators()
        for i in adminlist:
            if uid==i.user.id:
                return True
    except TelegramError as e:
        if e=="There is no administrators in the private chat":
            logger.info('(%s):%s','user_admin_value',e)
        return True
    except:
        logger.warning('Unknown error in [user_admin_value] function.')
        return False

# decorator
def wait_for_timeOut(func):
    """Reply a msg for timeOut"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        """Dectect bot if admin, if True, del cmd"""
        try:
            return func(bot, update, *args, **kwargs)
        except TelegramError as e:
            if e=="Timed out":
                bot.send_message(chat_id=update.message.chat_id,
                    text='請稍候')
    return wrapped


def bot_is_admin(bot,update):
    """Dectect bot if admin, return boolen value"""
    bot_auth=False
    if update.message.chat.type=='private':
        return bot_auth
    else:
        adminlist=update.message.chat.get_administrators()
        me=bot.get_me()
        for b in adminlist:
                if me.id==b.user.id:
                    bot_auth=True
        return bot_auth

def room_member_num(bot,update):
    # count member number
    total_count=bot.get_chat_members_count(update.message.chat.id)
    bot_count=2
    human_count=total_count-bot_count
    return human_count

# decorator
def del_cmd(func):
    """This decorator is used to prevent the command input before init"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        """Dectect bot if admin, if True, del cmd"""
        if bot_is_admin(bot,update):
            try:
                bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            except:
                pass
        return func(bot, update, *args, **kwargs)
    return wrapped

def del_cmd_func(bot, update):
    """Dectect bot if admin, if True, del cmd"""
    if bot_is_admin(bot,update):
        try:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            pass

def randList(list):
    return list[randrange(len(list))]

# decorator
def do_after_root(func):
    """This decorator is used to prevent the command input before init"""
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.date <= init_time:
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

# decorator
def admin_cmd(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if not is_admin(bot,update):
            try:
                bot.send_message(chat_id=update.message.chat_id, text="Only admin can use this command.")
            except:
                bot.send_message(chat_id=update.callback_query.message.chat_id, text="Only admin can use this command.")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
def bool2text(v):
    if v:
        return '開啟'
    else:
        return '關閉'
# DB function
def db_switch_one_value(data_tag):
    dict={'tag': ''}
    dict['tag']=data_tag
    data_value = db.misaki_setting.find_one(dict)
    if data_value['value']:
        result = db.misaki_setting.update_one(
            dict,
            {'$set': {'value': False}},
            upsert=True)
        return False
    else:
        result = db.misaki_setting.update_one(
            dict,
            {'$set': {'value': True}},
            upsert=True)
        return True

def utc8now():
    return (datetime.now()+timedelta(hours=8)).strftime("%y/%m/%d %H:%M:%S")

def utc8now_datetime():
    return datetime.now()+timedelta(hours=8)

def if_int_negative(interval):
    if interval<0:
        return True
    else:
        return False

def formula(key,text,if_list=False,parameter_preword='-',sep_word=' '):
    """
    To make function has add function.
    Ex. If /funcion -h
    Help funcion will return true.
    Or
    Ex. /funcion -f=123
    will return '123'

    this funcion support many formula
    if user input /funcion -f=123 -d -w=abc
    formula('f',text) will return '123'
    """
    # key is what you want to dectect
    key_len=len(key)
    key_total=parameter_preword+key
    key_position=text.find(key_total)
    value=False
    if key_position>=0:
        start_point=key_position+key_len+1
        if start_point>(len(text)-1):
            value=True
        else:
            try:
                if text[start_point] == '=':
                    start_point+=1
                    return_value=""
                    while(start_point<len(text)):
                        if text[start_point]==sep_word:
                            break
                        return_value+=text[start_point]
                        start_point+=1
                    value=return_value
                    if if_list:
                        """input data like -data=a,b,c"""
                        value=[]
                        for i in return_value.split(','):
                            value.append(i)
                elif text[start_point] == sep_word:
                    value=True
                else:
                    value=False
            finally:
                pass
    return value

def url_valid(url):
    try:
        code = request.urlopen(url).code
    except:
        return False
    return True

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def htmlPharseTester(str):
    """This function is to fix Can't parse entities problem like (*>△<)"""
    right_mouth=False
    for i in str:
        if i=="<":
            right_mouth=True
        if i==">":
            right_mouth=False
    return not right_mouth
