# coding=utf-8

bot_name='@MisakiAobaBot'
DEBUG=False
################################################
#              Global Setting                  #
################################################

### ---Module---

# ---Python function
import os
import time
from datetime import datetime,tzinfo,timedelta
from datetime import time as stime#specific time
from string import Template
from random import randrange

# ---Telegram
from telegram import *
from telegram.ext import *
from telegram.ext.dispatcher import run_async
from telegram.error import *

token = os.environ['TELEGRAM_TOKEN']
updater = Updater(token,workers=16)

# ---My Module
from module import *
import word_echo
import menu

################################################
#                 Global var                   #
################################################
quote_search={} # Use on /quote
reply_pair={} # Use on catch reply
################################################
#                   command                    #
################################################
@do_after_root
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                    text=GLOBAL_WORDS.word_start,
                    parse_mode=ParseMode.HTML)

@do_after_root
@del_cmd
def help(bot, update):
    """Send a message when the command /help is issued."""
    if randrange(1000)<30:
        bot.send_message(chat_id=update.message.chat_id, text="ぜ")
    else:
        bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_help,
                    parse_mode=ParseMode.HTML)

@do_after_root
@del_cmd
def tbgame(bot, update):
    """Send a message when the command /tbgame is issued."""
    bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_tbgame,
                    parse_mode=ParseMode.HTML)

@run_async
@do_after_root
@del_cmd
def rule(bot, update):
    """Send a message when the command /rule is issued."""
    pipeline={'room_id':update.message.chat_id}
    key='room_rule'
    room_data=display_data('room_config',pipeline,key)
    room_rule=""
    if room_data is True:
        room_rule="本群組尚未建立規則。"
    else:
        room_rule=room_data
    if randrange(1000)<30:
        bot.send_message(chat_id=update.message.chat_id, text="ぜ")
    else:
        msg=bot.send_message(chat_id=update.message.chat_id, text=room_rule,
                        parse_mode=ParseMode.HTML)
        time.sleep(60)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)

@do_after_root
def config(bot, update):
    """Send a message when the command /config is issued."""
    """Config is use to let user to turn on/off some function"""
    bot.send_message(chat_id=update.message.chat_id,
        text='何がご用事ですか？',
        reply_markup=menu.main_menu_keyboard())

@run_async
@do_after_root
@del_cmd
def nanto(bot, update, args):
    """Send a message when the command /nanto is issued."""
    if not args:
        msg_1=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_1)
        time.sleep(1)
        msg_2=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_2)
        time.sleep(0.5)
        msg_3=bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
        time.sleep(2)
        msg_4=bot.send_message(chat_id=update.message.chat_id, text=GLOBAL_WORDS.word_nanto_4)
        time.sleep(10)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg_4.message_id)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
        bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)
    else:
        if '#' in ' '.join(args):
            input_text=' '.join(args).split('#')
            text="なんとっ!$username居然$text了！".replace('$text',input_text[1]).replace('$username',input_text[0])
            msg_1=bot.send_message(chat_id=update.message.chat_id, text=text)
            time.sleep(1)
            msg_2=bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
            time.sleep(5)
            text="明日も$textすると、きっといいことがあると思いますよぉ～。えへへぇ♪".replace('$text',input_text[1])
            msg_3=bot.send_message(chat_id=update.message.chat_id, text=text)
            time.sleep(30)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)
        else:
            input_text=' '.join(args)
            text="なんとっ!居然$text了！".replace('$text',input_text)
            msg_1=bot.send_message(chat_id=update.message.chat_id, text=text)
            time.sleep(1)
            msg_2=bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQADGgADT1ZbIFSw_UAI28HiAg")
            time.sleep(5)
            text="明日も$textすると、きっといいことがあると思いますよぉ～。えへへぇ♪".replace('$text',input_text)
            msg_3=bot.send_message(chat_id=update.message.chat_id, text=text)
            time.sleep(30)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_3.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_2.message_id)
            bot.delete_message(chat_id=update.message.chat_id, message_id=msg_1.message_id)

@do_after_root
def which(bot, update, args):
    """Send a message when the command /which is issued."""
    split_symbol="#"
    if update.message.date > init_time:
        if not args:
            text="請輸入要給我決定的事情♪\n記得用〔$symbol〕分開喔！".replace('$symbol',split_symbol)
            bot.send_message(chat_id=update.message.chat_id, text=text)
        else:
            things=' '.join(args).split(split_symbol)
            if len(things)==1:
                result=things[0]
                text="そんな$resたいなら、私と諮問することは必要じゃないでしょ？".replace('$res',result)
                bot.send_message(chat_id=update.message.chat_id, text=text)
            else:
                result=things[randrange(len(things))]
                text="わたしは〜♬［$res］が良いと思うよ〜えへへ。".replace('$res',result)
                bot.send_message(chat_id=update.message.chat_id, text=text)

@do_after_root
@run_async
def quote(bot,update,args):
    # search parameter
    search_para=formula('f',' '.join(args))
    if search_para != False:
        if search_para=="":
            """Case 1: No words"""
            bot.send_message(chat_id=update.message.chat_id,text="Please enter word.")
            return
        # Search initialization
        find_result=quote_finder(search_para)
        result_length=len(find_result)
        search_init_time=datetime.now()
        global quote_search

        if result_length==0:
            """Case 2: No search result"""
            bot.send_message(chat_id=update.message.chat_id,text="No search result.")

        elif result_length<10:
            """Case 3: Result is less than 10"""
            # Hint user that result is in PM
            if if_int_negative(update.message.chat_id):
                bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

            # Test user has start bot
            try:
                bot.send_message(chat_id=update.message.from_user.id,
                    text="以下為【{}】的搜尋結果".format(search_para))
            except:
                bot.send_message(chat_id=update.message.chat_id,
                        text=GLOBAL_WORDS.word_PM_notice,
                        parse_mode='HTML')
                return

            # Package result
            result=[]
            t=""
            counter=1
            for i in find_result:
                t=t+str(counter)+'. '+'<pre>'+i['quote']+'</pre>'+' -- '+i['said']+'\n'
                counter+=1
            result.append(t)

            # Sending result
            try:
                quote_search[update.message.from_user.id]=result
                # save to globle var
                bot.send_message(chat_id=update.message.from_user.id,
                    text=result[0],
                    reply_markup=page_keyboard(result,1),
                    parse_mode='HTML')
            except:
                bot.send_message(chat_id=update.message.from_user.id,text="ぜ")
                return
                pass
            finally:
                search_total_time=(datetime.now()-search_init_time).total_seconds()
                t="結束搜尋。共有{}筆資料。\n共耗時{}秒。".format(result_length,search_total_time)
                bot.send_message(chat_id=update.message.from_user.id,text=t,parse_mode='HTML')

        else:
            """Case 4: Result is more than 10"""
            # Hint user that result is in PM
            if if_int_negative(update.message.chat_id):
                bot.send_message(chat_id=update.message.chat_id,text="結果將顯示於私人對話。")

            # Test user has start bot
            try:
                bot.send_message(chat_id=update.message.from_user.id,
                    text="以下為【{}】的搜尋結果".format(search_para))
            except:
                bot.send_message(chat_id=update.message.chat_id,
                        text=GLOBAL_WORDS.word_PM_notice,
                        parse_mode='HTML')
                return

            # Package result
            result=[]
            result_sub=[]
            counter=1
            for i in find_result:
                result_sub.append(str(counter)+'. '+'<pre>'+i['quote']+'</pre>'+' -- '+i['said']+'\n')
                counter+=1
                if len(result_sub) == 10:
                    t=""
                    for j in result_sub:
                        t+=j
                    result.append(t)
                    result_sub=[]
            # last message
            if result_sub!=[]:
                # Issue: for length is times of 10, will have more 1 page
                t=""
                for j in result_sub:
                    t+=j
                result.append(t)
                result_sub=[]

            try:
                # Sending result
                quote_search[update.message.from_user.id]=result # save to globle var
                bot.send_message(chat_id=update.message.from_user.id,
                    text=result[0],
                    reply_markup=page_keyboard(result,1),
                    parse_mode='HTML')
            except:
                bot.send_message(chat_id=update.message.from_user.id,text="ぜ")
                return
            finally:
                search_total_time=(datetime.now()-search_init_time).total_seconds()
                t="結束搜尋。共有{}筆資料共{}頁。\n共耗時{}秒。".format(result_length,int((result_length-1)/10)+1,search_total_time)
                bot.send_message(chat_id=update.message.from_user.id,text=t,parse_mode='HTML')
        return

    #daily quote
    if display_data('config',{'id':update.message.from_user.id},'day_quote')==False:
        del_cmd_func(bot,update)
        return
    else:

        modify_data('config',pipeline={'id':update.message.from_user.id},key='day_quote',update_value=False)

        del_cmd_func(bot,update)
    quote=randget()[0]
    text='<pre>'+quote['quote']+'</pre>\n'+'-----<b>'+quote['said']+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

@do_after_root
def randPic(bot,update,args):
    idol_name=' '.join(args)
    idol_name=idol_name.lower()
    if idol_name=='':
        url=randget_idol('all')[0]['url']
    elif idol_name in GLOBAL_WORDS.idol_list:
        try:
            url=randget_idol(idol_name)[0]['url']
        except IndexError:
            bot.send_message(chat_id=update.message.chat_id,text='這位偶像還沒有圖喔！')
            return
        except:
            bot.send_message(chat_id=update.message.chat_id,text='發生不明錯誤。')
            return

    elif idol_name not in GLOBAL_WORDS.idol_list:
        bot.send_message(chat_id=update.message.chat_id,text='だれ？')
        return
    else:
        return

    try:
        bot.send_photo(chat_id=update.message.chat_id,photo=url)
    except TimedOut:
        bot.send_message(chat_id=update.message.chat_id,text='讀取中...')
    except:
        bot.send_message(chat_id=update.message.chat_id,text='這位偶像還沒有圖喔！')



@do_after_root
def sticker_matome(bot,update):
    link=display_alldata('sticker')
    slink=''
    for i in link:
        slink=slink+'<a href="https://telegram.me/addstickers/'+i['setname']+'">'+i['about']+'</a>\n'
    try:
        bot.send_message(chat_id=update.message.from_user.id,text=slink,parse_mode='HTML')
    except:
        startme=GLOBAL_WORDS.word_PM_notice
        bot.send_message(chat_id=update.message.chat_id,text=startme,parse_mode='HTML')
    else:
        bot.send_message(chat_id=update.message.chat_id,text='看私訊～～♪')

@do_after_root
def savepic(bot, update):
    """Send a message when the command /savepic is issued."""
    """Send msg to ask user and save pic"""
    mention_url='tg://user?id={}'.format(update.message.from_user.id)
    first_name=update.message.from_user.first_name
    # m_ent=[MessageEntity('mention',offset=0, length=len(first_name),user=update.message.from_user)]
    text='<a href="{}">{}</a>さん、何がご用事ですか？'.format(mention_url,first_name)
    f=ForceReply(force_reply=True,selective=True)
    rpl=bot.send_message(chat_id=update.message.chat_id,
        text=text,reply_to_message=update.message,reply_markup=f,parse_mode='HTML')
    global reply_pair
    reply_pair[update.message.from_user.id]=rpl

def forcesave(bot, update):
    chat_id=update.message.chat_id

    last_data=room_state_getter(room_id=chat_id)


    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中...')
    except TimedOut:
        logger.error('(%s):Update time out.','forcesave')
    except Unauthorized:
        logger.error('(%s):Bot is not in room.','forcesave')
    except BadRequest:
        pass
    room_data={
        'room_id':update.message.chat_id,
        'room_name':update.message['chat']['title'],
        'update_time':datetime.now(),
        'total_message':update.message.message_id,
        'members_count':update.message.chat.get_members_count()
        }
    insert_data('room_state',room_data)

    if last_data==None:
        text="初次儲存。儲存成功。"
        try:
            bot.send_message(chat_id=chat_id,text=text)
        except BadRequest:
            pass
    else:
        wt=room_data['total_message']-last_data['total_message']
        mb=room_data['members_count']-last_data['members_count']
        tm_temp=(room_data['update_time']-last_data['update_time'])
        tm=strfdelta(tm_temp, "{hours}小時{minutes}分鐘")
        temp=Template("更新成功！\n在$time內，水量上漲了$water的高度，出現了$member個野生的P。")
        text=temp.substitute(time=tm,water=wt,member=mb)
        try:
            bot.send_message(chat_id=chat_id,text=text)
        except BadRequest:
            pass

def addecho(bot, update, args):
    context=' '.join(args)
    if context=="":
        bot.send_message(chat_id=update.message.chat_id,
            text='請輸入資料！\n輸入<pre>\\addecho -h</pre> 以尋求幫助。',
            parse_mode='HTML')
        return

    if formula('h',context):
        """help"""
        addEcho_help(update,bot)
        return

    try:
        data=word_echo.addEcho_main(context,update=update,bot=bot)
        if data:
            mongo_data=insert_data('words_echo',data)
            logger.info("Insert echo data sucessful:%s ID=%s",str(data['words']),mongo_data.inserted_id)
            bot.send_message(chat_id=update.message.chat_id,text='資料寫入成功！')
        else:
            logger.info("Insert echo data failed.")
            bot.send_message(chat_id=update.message.chat_id,text='資料寫入失敗！')

    except TimedOut:
        bot.send_message(chat_id=update.message.chat_id,text='Saving...')

def finduser(bot, update, args):
    """used to find user data from user_id"""
    context=' '.join(args)
    data=context.split('#')
    try:
        room_id=int(data[0])
        user_id=int(data[1])
    except ValueError:
        logger.warning("Lack of information while find user")
        bot.send_message(chat_id=update.message.chat_id,text="請輸入正確的格式。")
        return

    try:
        user_data=bot.get_chat_member(chat_id=room_id,user_id=user_id)
        first_name=user_data.user.first_name
        last_name=user_data.user.last_name
        username=user_data.user.username
        text="User {} in chat {} is {} {} with username:{}.".format(user_id,room_id,first_name,last_name,username)
        bot.send_message(chat_id=update.message.chat_id,text=text)
    except UnboundLocalError:
        logger.warning("Wrong information while find user")
        bot.send_message(chat_id=update.message.chat_id,text="請輸入正確的代號。")
        return

def testfunc(bot, update):
    """print something"""
    print(str(is_admin(bot, update)))
################################################
#               not command                    #
################################################
def key_word_reaction(bot,update):
    """Observe all msg from user."""
    key_words=update.message.text #record
    ###################################
    #        key word reaction        #
    ###################################
    def wordEcho(user_switch,room_switch):
        """Detect what user say and misaki will response."""
        # --Step.1 Switch--
        if user_switch==False or room_switch==False:
            """Switch"""
            return False

        word_pool=[] #create a pool to save those have chance to send
        def comparator(word,data):
            """Input text, compare to data in database, return value and save in pool."""
            # word is str, where data is a dict
            if not isinstance(word, str):
                raise TypeError
            if not isinstance(data, dict):
                raise TypeError

            """check if all word correct will go"""
            try:
                for check in data['words']:
                    if data['allco'] == False:
                        "one word correct will go"
                        if word.find(check)!=-1:
                            return data
                    else:
                        "all word correct will go"
                        if word.find(check)!=-1:
                            continue
                        else:
                            return False
                        return data
            except TypeError:
                logger.error("Words type wrong:%s",str(words))
            return False
            # If nothing return false

        # --Step.2 Compare data--
        echo_data=display_alldata('words_echo') # Catch all data in db
        for d in echo_data:
            # Search data in db
            data_value=comparator(key_words,d)
            if data_value:
                word_pool.append(data_value)
                # If search engine has result, save it to pool

        if not word_pool:
            # If pool has nothing, return
            return False

        # --Step.3 Pick data from pool--
        pool_rand=weighted_random()
        type="" # Video / Photo / String
        for i in word_pool:
            """
            Determine its type. Msg or Video or Photo? Pack it and send.
            Note that echo may be video.
            """
            echo=i['echo']
            photo=i['photo']
            video=i['video']
            prob=i['prob']
            els=i['els']

            if echo:
                """ECHO case"""
                if i['echo_list']:
                    """If echo is a list"""
                    each_prob=int(prob/len(echo))
                    for each_echo in echo:
                        rand_data={"Type":"STRING","Data":each_echo}
                        pool_rand.add(rand_data,each_prob)
                else:
                    rand_data={"Type":"STRING","Data":echo}
                    pool_rand.add(rand_data,prob)
                if url_valid(els):
                    rand_data={"Type":"VIDEO","Data":els}
                    pool_rand.add(rand_data,1000-prob)
                elif els==None:
                    pool_rand.add_none(1000-prob)
                else:
                    rand_data={"Type":"STRING","Data":els}
                    pool_rand.add(rand_data,1000-prob)
            elif photo:
                """PHOTO case"""
                if i['echo_list']:
                    """If echo is a list"""
                    each_prob=int(prob/len(photo))
                    for each_photo in photo:
                        rand_data={"Type":"PHOTO","Data":each_photo}
                        pool_rand.add(rand_data,each_prob)
                else:
                    rand_data={"Type":"PHOTO","Data":photo}
                    pool_rand.add(rand_data,prob)

                if els==None:
                    pool_rand.add_none(1000-prob)
                else:
                    rand_data={"Type":"PHOTO","Data":els}
                    pool_rand.add(rand_data,1000-prob)
            elif video:
                """VIDEO case"""
                if i['echo_list']:
                    """If echo is a list"""
                    each_prob=int(prob/len(video))
                    for each_video in video:
                        rand_data={"Type":"VIDEO","Data":each_video}
                        pool_rand.add(rand_data,each_prob)
                else:
                    rand_data={"Type":"VIDEO","Data":video}
                    pool_rand.add(rand_data,prob)
                if els==None:
                    pool_rand.add_none(1000-prob)
                else:
                    rand_data={"Type":"VIDEO","Data":els}
                    pool_rand.add(rand_data,1000-prob)




        # --Step.4 Send--
        cid=update.message.chat_id
        def msgSend(words):
            try:
                bot.send_message(chat_id=cid,text=words)
            except:
                logger.error("Word echo failed while sending word %s.",words)
        def videoSend(vid):
            try:
                bot.send_video(chat_id=cid, video=vid)
            except:
                logger.error("Word echo failed while sending video %s.",vid)
        def picSend(pic):
            try:
                bot.send_photo(chat_id=cid, photo=pic)
            except:
                logger.error("Word echo failed while sending photo %s.",pic)

        jump_from_pool=pool_rand.output_one()
        if jump_from_pool==None:
            return
        pool_type=jump_from_pool['Type']
        if pool_type=="STRING":
            msgSend(jump_from_pool['Data'])
        elif pool_type=="PHOTO":
            photoSend(jump_from_pool['Data'])
        elif pool_type=="VIDEO":
            videoSend(jump_from_pool['Data'])

    ###################################
    #          reply_pair             #
    ###################################
    global reply_pair
    try:
        m=reply_pair[update.message.from_user.id]
    except KeyError:
        pass
    else:
        """Main function"""
        function_type=m[0]
        if function_type=="RULE_EDIT":
            """RULE_EDIT"""
            if update.message.reply_to_message==m[1]:
                room_data={
                'room_id':update.message.chat_id,
                'room_name':update.message['chat']['title'],
                'update_time':update.message.date,
                'room_rule':update.message.text
                }

                updata_data("room_config",{'room_id':update.message.chat_id},{"$set":room_data})
                bot.send_message(chat_id=update.message.chat_id,text="更新成功！")
            del reply_pair[update.message.from_user.id]
    ###################################
    #              picsave            #
    ###################################
    if update.message.text.find("@db")!=-1:
        cmd_word_save=update.message.text.replace("@db","").lower()
        if cmd_word_save in GLOBAL_WORDS.idol_list:
            rmsg=update.message.reply_to_message
            try:
                if url_valid(rmsg.text):
                    idol_db={
                        'name':cmd_word_save,
                        'url':rmsg.text,
                        'date':datetime.now(),
                        'saved_by':update.message.from_user.id
                    }
                    insert_data('ml_idol_pic_colle',idol_db)
                    echo_word='画像が保存されました！'
                    bot.send_message(chat_id=update.message.chat_id,text=echo_word)
            except AttributeError:
                bot.send_message(chat_id=update.message.chat_id,text="画像がない。保存失敗しました。")
        elif cmd_word_save=='':
            bot.send_message(chat_id=update.message.chat_id,text="もう！こんな遊ばなってください！")
        else:
            bot.send_message(chat_id=update.message.chat_id,text="知らない人ですよ。")
        # Exit region
        return
    ###################################
    #          quote collector        #
    ###################################
    record=False
    test=update.message.text
    if test.find(' #名言')!=-1 or test.find('#名言 ')!=-1:
        if update.message.reply_to_message==None and update.message.from_user.is_bot==False:
            test=test.replace(' #名言','').replace('#名言 ','')
            qdict={
                'quote': test,
                'said': update.message.from_user.first_name,
                'tag': '',
                'said_id':update.message.from_user.id,
                'date':datetime.now()
                }
            insert_data('quote_main',qdict)
            record=True
    if test.find('#名言')!=-1 and record==False:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qdict={
                'quote': update.message.reply_to_message.text,
                'said': update.message.reply_to_message.from_user.first_name,
                'tag': '',
                'said_id':update.message.reply_to_message.from_user.id,
                'date':datetime.now()
                }
            insert_data('quote_main',qdict)

    """RUN"""
    # switch
    user_reply_switch=display_data('config',{'id':update.message.from_user.id},'reply')

    wordEcho(user_switch=user_reply_switch,room_switch=True)

def message_callback(bot, update):

    ###################################
    #              aisatu             #
    ###################################
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

################################################
#              repeating command               #
################################################

def misaki_changeday_alarm(bot,job):
    # 玩人狼玩到忘記每日
    bot.send_message(chat_id='-1001290696540',text=GLOBAL_WORDS.word_do_mission)

def save_room_state(bot, job):
    ######################
    #put in your group id#
    ######################
    chat_id=-1001290696540

    last_data=room_state_getter()

    try:
        msg=bot.send_message(chat_id=chat_id,text='聊天室資訊更新中...')
    except TimedOut:
        logger.error('(%s):Update time out.','save_room_state')
    except Unauthorized:
        logger.error('(%s):Bot is not in room.','save_room_state')
    except BadRequest:
        pass
    room_data={
        'room_id':msg.chat_id,
        'room_name':msg['chat']['title'],
        'update_time':datetime.now(),
        'total_message':msg.message_id,
        'members_count':msg.chat.get_members_count()
        }
    insert_data('room_state',room_data)

    wt=room_data['total_message']-last_data['total_message']
    mb=room_data['members_count']-last_data['members_count']
    tm_temp=(room_data['update_time']-last_data['update_time'])
    tm=strfdelta(tm_temp, "{hours}小時{minutes}分鐘")
    temp=Template("更新成功！\n在$time內，水量上漲了$water的高度，出現了$member個野生的P。")
    text=temp.substitute(time=tm,water=wt,member=mb)
    try:
        bot.send_message(chat_id=chat_id,text=text)
    except BadRequest:
        pass

def daily_reset(bot,job):
    modify_many_data('config',pipeline={"day_quote":False},key='day_quote',update_value=True)



################################################
#                   inline                     #
################################################
def inline_handler(bot,update):
    query=update.inline_query.query

    #rand pic
    def pic_url(name):
        result=randget_idol(name)
        if result:
            return result[0]['url']
        return randget_idol('all')[0]['url']

    name=query.lower()
    rand_idol_pic=InlineQueryResultPhoto(
        id=str(datetime.now()),
        title='RANDPIC',
        photo_url=pic_url(name),
        thumb_url="https://i.imgur.com/kdAihxk.jpg"
    )

    bot.answer_inline_query(inline_query_id=update.inline_query.id,
    results=[rand_idol_pic],
    cache_time=2,
    is_personal=True)


# error logs
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('(Update %s):"%s"', update, error)
################################################
#                   init                       #
################################################
@do_once
def initialization():
    # ---Record init time---
    global init_time
    init_time = datetime.now()
    logger.info("(%s):Bot start.","initialization")
################################################
#                   main                       #
################################################
def main():
    """Start the bot."""

    # <initialization>
    initialization()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dj = updater.job_queue

    # <function start>

    # ---repeating jobs---
    # mission_callback every 22:30 daily
    dj.run_daily(misaki_changeday_alarm,stime(14,30))
    # mission_show record every 8 hours
    m_history=[stime(7,0,0),stime(15,0,0),stime(23,0,0)]
    for t in m_history:
        #plug in mission time with loop
        dj.run_daily(save_room_state,t)
    # mission refresh daily gasya
    dj.run_daily(daily_reset,stime(14,59,59))

    # ---Command answer---
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rule", rule))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tbgame", tbgame))
    dp.add_handler(CommandHandler("config", config))
    dp.add_handler(CommandHandler("nanto", nanto, pass_args=True))
    dp.add_handler(CommandHandler("which", which, pass_args=True))
    dp.add_handler(CommandHandler("quote",quote, pass_args=True))
    dp.add_handler(CommandHandler("randpic",randPic, pass_args=True))
    dp.add_handler(CommandHandler("sticker",sticker_matome))
    dp.add_handler(CommandHandler("forcesave",forcesave))
    dp.add_handler(CommandHandler("addecho", addecho, pass_args=True))

    # hidden funcgion
    dp.add_handler(CommandHandler("finduser", finduser, pass_args=True))

    # test function
    if DEBUG:

        # dp.add_handler(CommandHandler("savepic",savepic))
        dp.add_handler(CommandHandler("testfunc",testfunc))

    # ---Menu function---
    dp.add_handler(CallbackQueryHandler(menu.menu_actions))

    # ---Inline function---
    dp.add_handler(InlineQueryHandler(inline_handler))

    # ---Message answer---
    dp.add_handler(MessageHandler(Filters.text, key_word_reaction))
    dp.add_handler(MessageHandler(Filters.all, message_callback))

    # <function end>

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # IDLE
    updater.idle()


################################################
#                   program                    #
################################################
if __name__ == '__main__':
    main()
