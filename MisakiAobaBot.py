# coding=utf-8

# BotFather-commend setting
"""
start-我是765事務所的事務員，青羽美咲
help-由青羽小姐提供您幫助
rule-本群規則瀏覽
state-群狀態
config-設定
tbgame-765プロゲーム部入口，進去跟大家玩桌遊吧
nanto-なんとぉ！
"""

# dev
"""
〖開發目標〗
！使用者指令與自主函式分隔(使用者指令 vs timer(自動控制用))
！群組對話與個人對話分隔(determin chat_id>0)

提醒功能
自由設定文字（config）
語言設定
資料庫設定
自動改群名
"""

################################################
#                   Global                     #
################################################
# import
from telegram import (Bot, Chat, Sticker, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,JobQueue
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
import logging
import time
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

bot_name='@MisakiAobaBot'
token = os.environ['TELEGRAM_TOKEN']
spreadsheet_key=os.environ['SPREAD_TOKEN']
# token will taken by heroku
# Please use test token when dev
# WARNING!!! Please use quarter space instead of tab
# This will cause fatal error

# global words

word_start = """青羽美咲です！宜しくお願い致します！
尋求幫助 - /help
"""

word_help = """
/help - 由青羽小姐提供您幫助
/rule - 本群規則瀏覽
/state - 群狀態
/config - 設定
/tbgame - 765プロゲーム部入口，進去跟大家玩桌遊吧
/nanto - なんとっ！

【みんなのリンク】
<a href="https://t.me/joinchat/IFtWTxKu7x6vuSK8HsFgsQ">〔765技術部〕</a>
技術部開放對BOT的意見以及回饋
<a href="https://t.me/joinchat/J-IqLA__7_O6N5_ED8jWHQ">〔SC TELE討論群〕</a>
<a href="https://twitter.com/imasml_theater">〔ML Twitter〕</a>
<a href="https://twitter.com/imassc_official">〔SC Twitter〕</a>
<a href="https://twitter.com/imascg_stage">〔CG Twitter〕</a>
"""
word_rule = """
　　　　<b>【台湾アイマスTelegram鯖ルール】</b>

<b>〖宗旨〗</b>
　　本群組為提供アイマス愛好者交流之群組，主要討論包含偶像大師本家、ML、CG、SC等等系列之討論，但<b>不限於此</b>。
　　也就是說任何討論皆可，但請注意不要太專注在自我小世界。

<b>〖討論限制〗</b>
　　A. 不得含有任意<b>辱罵、侮辱、挑撥、等侵害他人言論</b>
　　B. 禁止惡意的<b>廣告文</b>投放
　　C. 禁止任何違反<b>中華民國法律</b>之言論
　　D. 圖片限制：目前設定為<b>高度</b>限制

　　☞高度限制：任何圖片包括性暗示、擬獸，以及妨害風俗及18禁等圖片的最高限度禁止
　　中度限制：露點、高度露出、激凸之圖片的中度禁止
　　低度限制：僅限制露點圖片，包括三次元二次元

　　E. 為求言論自由性，A、B二條款為告訴乃論。
　　F. 若有以上違規事由者，管理者有權利停止其發言，停止時間一率為一週，視情況嚴重可以加重至一個月。
　　G. 群內不能打棒球
　　H. 也不能踢足球

<b>〖最後〗</b>
　　輕鬆地討論吧～！
"""

word_tbgame="""
<a href="https://t.me/joinchat/IFtWTxKG_KG-500YZBBnDA">〔765プロゲーム部♞〕</a>
<a href="https://memories.millimas.info/game_center">〔GREEMAS小遊戲〕</a>
"""

word_nanto_1="""
今日のログインボーナスはこちらです♪
明日はこちらがもらえますからね！
"""
word_nanto_2="""
☆★☆★☆★☆★☆★☆★☆★☆★
"""
word_nanto_3="""
なんとっー！
"""
word_nanto_4="""
ただいま、スペシャルログインボーナスを開催中です♪
明日もログインすると、きっといいことがあると思いますよぉ～。えへへぇ♪
"""

word_test="""
<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<a href="http://www.example.com/">inline URL</a>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
"""

word_state="""
版本：Alpha.0.3
開發者：Dephilia（蝶芙）
telegramID:@Dephilia
<a href="https://www.plurk.com/Dephillia">〔噗浪〕</a>
"""

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

################################################
#                   tool kits                  #
################################################
def c_tz(datetime,tz):
    t=datetime+timedelta(hours=tz)#轉換時區 tz為加減小時
    return t#datetime object

#key of spread sheet
def get_cell(key_word,worksheet):
    try:
        cell=worksheet.find(key_word)
    except:#not find
        return None
    else:
        return cell
#def set_cell(value,cell,sheet):
#    sheet.update_cell(cell.row,cell.col,value)

def is_admin(bot,update):
    #bool func to check auth
    adminlist=update.message.chat.get_administrators()
    is_admin=False
    for i in adminlist:
        if update.message.from_user.id==i.user.id:
            is_admin=True
    return is_admin

################################################
#                   command                    #
################################################
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_start,
                    parse_mode=ParseMode.HTML)

def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_help, 
                    parse_mode=ParseMode.HTML)

def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_tbgame, 
                    parse_mode=ParseMode.HTML)

def rule(bot, update):
    """Send a message when the command /rule is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_rule, 
                    parse_mode=ParseMode.HTML)

def state(bot, update):
    """Send a message when the command /state is issued."""
    bot.send_message(chat_id=update.message.chat_id,
    text='目前室內人數：{}'.format(str(bot.get_chat_members_count(update.message.chat.id)))+'\n'+
    word_state,parse_mode=ParseMode.HTML)

def config(bot, update,args):
    """Send a message when the command /config is issued."""
    word_1="""
    <pre>    言いたいことがあるんだよ
    やっぱり$nameはかわいいよ
    すきすき大好き、やっぱ好き</pre>
    """
    word_2="""
    <pre>    やっと見つけたお姫様
    俺が生まれてきた理由
    それはお前に出会うため</pre>
    """
    word_3="""
    <pre>    俺と一緒に人生歩もう
    世界で一番愛してる
    
    ア・イ・シ・テ・ル</pre>
    """
    
    word_1=word_1.replace('$name',' '.join(args))
    t=' '.join(args)
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text="本功能目前沒有毛用")
    else:
        bot.send_message(chat_id=update.message.chat_id, text=word_1,
        parse_mode=ParseMode.HTML)
        time.sleep(9)
        bot.send_message(chat_id=update.message.chat_id, text=word_2,
        parse_mode=ParseMode.HTML)
        time.sleep(9)
        bot.send_message(chat_id=update.message.chat_id, text=word_3,
        parse_mode=ParseMode.HTML)

def nanto(bot, update):
    """Send a message when the command /nanto is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_1)
    time.sleep(1)
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_2)
    time.sleep(0.5)
    bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
    time.sleep(2)
    bot.send_message(chat_id=update.message.chat_id, text=word_nanto_4)

def title(bot,update,args):
    title = ' '.join(args)
    adminlist=update.message.chat.get_administrators()
    is_admin=False
    
    me=bot.get_me()
    bot_auth=False
    
    for i in adminlist:
        if update.message.from_user.id==i.user.id:
            is_admin=True
            
    for b in adminlist:
            if me.id==b.user.id:
                bot_auth=True
    
    if is_admin==True:
        if bot_auth==True:
            bot.set_chat_title(chat_id=update.message.chat_id, title=title)
            bot.send_message(chat_id=update.message.chat_id,text='できました！！')
        else:
            bot.send_message(chat_id=update.message.chat_id,text='失敗しました、能力不足ですね')
        
    else:
        bot.send_message(chat_id=update.message.chat_id,text='申し訳ございませんが、このコマンドは、管理者しか使いません\nOops!Only admin can change title.')

#mention that bot need to be an admin of sgroup
#should change automatically and get title from DB,though JOBquece
#function for test

def set_remind_time(bot,update,args):
    #do not test public cause there's no auth check yet
    #check auth
    #if is_admin(bot,update)==True:
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    #got from google api
    #attach mine for example
    #try to set in environ values but got fail
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    if not args:
        return
    
    text=' '.join(args)
    l_text=text.split('%%')
    tsheet=sheet.worksheet('name')
    cell=get_cell(l_text[0],tsheet)
    if cell==None:
        tsheet.insert_row([l_text[0],l_text[1],l_text[2],update.message.from_user.id], 2)
    else:
        tsheet.update_cell(cell.row,cell.col+1,l_text[1])
        tsheet.update_cell(cell.row,cell.col+2,l_text[2])
        tsheet.update_cell(cell.row,cell.col+3,update.message.from_user.id)

def aisatu(bot, update):
    if update.message.new_chat_members != None:
        for u in update.message.new_chat_members:
            if u.is_bot == False:
                text='$usernameさん、ようこそ事務所へ！\n輸入 /help 可以尋求幫助'
                # text = text.replace('$username',u.first_name.encode('utf-8'))
                text = text.replace('$username',u.first_name)
                bot.send_message(chat_id=update.message.chat_id,text=text)

    if update.message.left_chat_member != None:
        if update.message.left_chat_member.is_bot == False:
            text='まだ会いましょう！$usernameさん！'
            # text = text.replace('$username',update.message.left_chat_member.first_name.encode('utf-8'))
            text = text.replace('$username',update.message.left_chat_member.first_name)
            bot.send_message(chat_id=update.message.chat_id,text=text)

def test(bot, update):
    """Send a message when the command /test is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=word_test, 
                  parse_mode=ParseMode.HTML)

def notiger(bot, update):
    """Send a message when the command /notiger is issued."""
    word_notiger="""
    <pre>    ジャンプをしない！
    ミックスしない！
    クラップしない！～叫ばない！
    マナーを守ろう ｲｪｯﾀｲｶﾞｰ！
    ﾀｲｶﾞｰ!ﾌｧｲﾔｰ!ｻｲﾊﾞｰ!ﾌｧｲﾊﾞｰ!ﾀﾞｲﾊﾞｰ!ﾊﾞｲﾊﾞｰ!ｼﾞｬｰｼﾞｬｰ!!</pre>
    """
    bot.send_message(chat_id=update.message.chat_id, text=word_notiger, 
                  parse_mode=ParseMode.HTML)

def mission_callback(bot,job):
    # somaction

    # 玩人狼玩到忘記每日
    bot.send_message(chat_id='-1001290696540',text='做每日')
                  
def echo(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.sticker.file_id)

def echo2(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):
    if update.message.text.find('MisakiAobaBot')!=-1:
        bot.send_message(chat_id=update.message.chat_id, text="すみません、よく分かりません。")

################################################
#                   main                       #
################################################
def main():
    """Start the bot."""
    # ---TOKEN---
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # <function start>

    # ---daily jobs---
    # mission_callback every 22:30 daily
    job_m=updater.job_queue.run_daily(mission_callback,stime(14,30))

    # ---Command answer---
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tbgame", tbgame))
    dp.add_handler(CommandHandler("state", state))
    dp.add_handler(CommandHandler("config", config, pass_args=True))
    dp.add_handler(CommandHandler("set_remind_time", set_remind_time, pass_args=True))
    dp.add_handler(CommandHandler("nanto", nanto))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("notiger", notiger))
    # dp.add_handler(CommandHandler("title", title, pass_args=True))

    # ---Message answer---
    #dp.add_handler(MessageHandler(Filters.sticker, echo))
    #dp.add_handler(MessageHandler(Filters.text, echo2))
    #dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(MessageHandler(Filters.all, aisatu))
    
    # <function end>

    # log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()

    # IDLE
    updater.idle()


################################################
#                   program                    #
################################################
if __name__ == '__main__':
    main()
