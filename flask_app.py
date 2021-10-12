from flask import Flask, request
import json
import telepot
import urllib3
import requests
from telepot.namedtuple import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,ForceReply#,KeyboardButton
import listOfItems
import re
import SQLDB
import os
import usersDB
import graph_itemsum
import passwords
#from ConstConfigurations import *

'''
App configurations
'''
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = passwords.secret
bot = telepot.Bot(passwords.token)

bot.setWebhook("https://pricesCompareBot.pythonanywhere.com/{}".format(secret), max_connections=1)


'''
Constant configurations
'''

COMPAREBUT="השווה וחסוך💰"
BOREDBUT="🥱משועמם בתור?"
ABOUTBUT="👾אודות הבוט"
UPDAETBUT="עודכן לאחרונה ב:"
CHANNELBUT="ערוץ מבצעים💸"
UNDERSTOODBUT="👌הבנתי!"
DO_NOT_TYPEBUT="🤦🏼‍♀️!!!אין לי כח להקליד"
BACKBUT="🔙חזור"
MY_LISTBUT="הרשימה שלי 📝"
ADD_TO_LISTBUT="הוסף לרשימה ✏️"
DEL_FROM_LISTBUT="מחק מהרשימה ❌"
DEL_ALL_LISTBUT="מחק את כל הרשימה✖️"
SHOW_ALLBUT="הצג סהכ 📊"
LISTBUT="רשימת קניות📜"
VIDEO_BUT="לא הבנתי 📹"
BRANCHES_BUT="בחירת רשתות וסניפים 🎯"
OSHERAD_BUT="אושר עד 🔵"
RAMILEVI_BUT="רמי לוי 🔴"
YOHANANOF_BUT="יוחננוף 🟡"
ADD_BRANCHE_BUT="הוסף סניף להשוואה 🏬"
DEL_BRANCHE_BUT="הסר סניף להשוואה ❌"
ALL_MY_BRANCHE_BUT="הסניפים שלי 📈"
ALL_USERS_BUT="all users"
CPU_BUT="cpu use"

MAINKEYBOARD = ReplyKeyboardMarkup(keyboard=[[COMPAREBUT],[BOREDBUT,LISTBUT],[ABOUTBUT,BRANCHES_BUT],[UPDAETBUT]])
SUBKEYBOARD = ReplyKeyboardMarkup(keyboard=[[UNDERSTOODBUT],[VIDEO_BUT],[DO_NOT_TYPEBUT],[BACKBUT]])
LISTKEYBOERD = ReplyKeyboardMarkup(keyboard=[[MY_LISTBUT],[DEL_ALL_LISTBUT,SHOW_ALLBUT],[BACKBUT]])
ITEM_KEYBOERD = ReplyKeyboardMarkup(keyboard=[[ADD_TO_LISTBUT,DEL_FROM_LISTBUT]])
BRANCHES_KEYBOERD = ReplyKeyboardMarkup(keyboard=[[OSHERAD_BUT],[RAMILEVI_BUT],[YOHANANOF_BUT],[ALL_MY_BRANCHE_BUT],[BACKBUT]])
BRANCHES_LIST_KEYBOERD = ReplyKeyboardMarkup(keyboard=[[ADD_BRANCHE_BUT,DEL_BRANCHE_BUT],[ALL_MY_BRANCHE_BUT],[BACKBUT]])
ADMIN_KEYBOERD = ReplyKeyboardMarkup(keyboard=[[ALL_USERS_BUT,CPU_BUT],[BACKBUT]])

MY_USER_NAME=" @yonilabell "
HELLO="שלום "
TO_COMPANS="כדי להשוות מחיר אנא בחר סניפים להשוואה והכנס מזהה מוצר שנמצא מתחת לברקוד"
TO_COMPANS+=" או הכנס שם מוצר ובחר מהרשימה "
BOT_DEVANS="הבוט בפיתוח ע'י"
WAIT_ANS="כבר שולח סרטון, כמה שניות"
UNDERSTOODANS="בסדר גמור, מובן לחלוטין ! יש לי פתרון לעצלנים כמוני, פשוט צלם את הברקוד עם הספרות מתחתיו ושלח את התמונה לבוט הזה: @qrcrbot. ושלח לי את התוצאה "
BACKANS="🔙חזרתי"
CHANANS="https://t.me/salesChan"
TYPEANS="הכנס מזהה מוצר"
NOT_FOUNDANS='לא הבנתי את בקשתך'
BRANCHES_ANS="בחר רשת"
ADD_DEL_ANS='הוסף או מחק'
DONE_ANS='בוצע!'
ADD_COMANDREP="אוקי! מה להוסיף"
DEL_COMANDREP="אוקי! מה למחוק"
SELECT_BRANCH_REP='בחר סניף'
NOTE_REP="*מציג רק עבור הסניפים שבהן קיימים כל המוצרים ברשימה"
NO_STORE_REP="לא קיימים סניפים להשוואה! אנא הוסף סניפים."
RamiLevi='רמי לוי'
osherad='אושר עד'
yohananof='יוחננוף'

forcereply=ForceReply(force_reply=True)



'''
The app
'''
app = Flask(__name__)
@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    try:

        if "message" in update:

            chat_id=str(update["message"]["from"]["id"])
            user_name=str(update["message"]["from"]["first_name"])
            txmsg=update["message"]["text"]
            if "text" in update["message"]:
                manage(chat_id,user_name,txmsg)

            else:
                send_not_found(chat_id)


        elif "callback_query" in update:
                manage_callback(update)

        else:
            send_not_found(chat_id)

    except:
        '''
        if something is wrong send dev (me..) msg
        '''
        bot.sendMessage("318861933","wtf "+str(update))

    return "OK"




'''
Functions
'''

# func 1
def isHe(txt):
    '''
    check if text is hebrew
    '''

    x = re.match(r"^[\u0590-\u05fe\s]*$", txt)
    if x:
        return True
    else:
        return False

# func 2
def MyGetItemAPI(chat_id,item):
    '''
    get item's json from API and format it to send back
    '''
    r=''
    for store in usersDB.get_stores(chat_id):

        try:

            aitem=requests.get("https://yonilabell.pythonanywhere.com/getp/"+str(store)+"/"+item)
            j1=json.loads(aitem.content)


            astor=requests.get("https://yonilabell.pythonanywhere.com/getstore/"+str(store))
            j2=json.loads(astor.content)

            if "name" in j1:

                if r == '':
                    r+=str(j1["name"])+'\n'

                snm=str(j2['0']).split('\n')[0].replace(':','')
                r+=str(store).split('/')[0].replace("osherad",osherad).replace("RamiLevi",RamiLevi).replace("yohananof",yohananof)+' '+snm

                if "price" in j1:
                    r+=': '+str(j1["price"])
                    r+='\n'

                if "promo" in j1:
                       r+=' *מבצע* '+str(j1["promo"])+'\n'

        except:
            pass

    if r=='':
        r="לא קיים בסניפים שלך!"
    else:
        r+='ברקוד:'
        r+=item
    return r

# func 3
def MyGetItemNameAPI(itemid):
    '''
    get item's mame from API, if not-found return false
    '''
    try:
        response=requests.get("http://yonilabell.pythonanywhere.com/getitembyid/"+itemid)
        price=json.loads(response.content)
        reply=str(price)
        return reply

    except:
        return False


# func 4
def new_user(chat_id,user_name):
    '''
    if it is a new user add to the DB and send me a msg
    '''
    try:
        res=requests.get("https://yonilabell.pythonanywhere.com/adduser/"+chat_id+"/"+user_name)
        if str(res)=='<Response [200]>':
            bot.sendMessage("318861933",user_name)
    except:
        pass



# func 5
def manage(chat_id,user_name,txmsg):

    if txmsg=="/start":
        new_user(chat_id,user_name)
        bot.sendMessage(chat_id,HELLO+user_name,reply_markup=MAINKEYBOARD)

    elif txmsg==COMPAREBUT :
        bot.sendMessage(chat_id,TO_COMPANS,reply_markup=SUBKEYBOARD)

    elif txmsg==BOREDBUT :
        bot.sendMessage(chat_id, "@gamebot")

    elif txmsg==ABOUTBUT :
        bot.sendMessage(chat_id,BOT_DEVANS+MY_USER_NAME,reply_markup=MAINKEYBOARD)

    elif txmsg==UPDAETBUT :
        lastUp=requests.get("http://yonilabell.pythonanywhere.com/lastUpdated")
        bot.sendMessage(chat_id,lastUp.content,reply_markup=MAINKEYBOARD)

    elif txmsg==CHANNELBUT :
        bot.sendMessage(chat_id, CHANANS,reply_markup=MAINKEYBOARD)

    elif txmsg==UNDERSTOODBUT :
        bot.sendMessage(chat_id, "😃יופי",reply_markup=MAINKEYBOARD)

    elif txmsg==DO_NOT_TYPEBUT :
        bot.sendMessage(chat_id,UNDERSTOODANS,reply_markup=MAINKEYBOARD)

    elif txmsg==BACKBUT or txmsg=='/back':
        bot.sendMessage(chat_id,BACKANS,reply_markup=MAINKEYBOARD)

    elif txmsg==BRANCHES_BUT:
        bot.sendMessage(chat_id,BRANCHES_ANS,reply_markup=BRANCHES_KEYBOERD)

    elif txmsg==VIDEO_BUT:

        bot.sendVideo(chat_id,video='BAACAgQAAxkDAAIyNGA_YapWDFjY3AOgjUe2Rv0q6f7UAAIECAACZK74UZdmZgphJ4q4HgQ',reply_markup=MAINKEYBOARD)

    elif txmsg==MY_LISTBUT :
        r=SQLDB.sqldb(user_name,chat_id,"0","0","all")
        bot.sendMessage(chat_id,r,reply_markup=LISTKEYBOERD)

    elif txmsg==DEL_ALL_LISTBUT :
        text=SQLDB.sqldb(user_name,chat_id,"0","0","delall")
        bot.sendMessage(chat_id,text,reply_markup=LISTKEYBOERD)


    elif txmsg==SHOW_ALLBUT :

        text=SQLDB.sqldb(user_name,chat_id,"0","0","list")

        try:

            graph_itemsum.get_graph(text,str(chat_id))
            file_name=str(chat_id)+"graph.png"
            bot.sendPhoto(chat_id,photo=open(file_name,"rb"),reply_markup=LISTKEYBOERD)
            os.remove(file_name)
            bot.sendMessage(chat_id,NOTE_REP,reply_markup=LISTKEYBOERD)

        except:
            bot.sendMessage(chat_id,NOTE_REP,reply_markup=LISTKEYBOERD)




    elif txmsg in [OSHERAD_BUT,RAMILEVI_BUT,YOHANANOF_BUT]:

        if  txmsg==OSHERAD_BUT:
            stor='osherad'
        elif txmsg==RAMILEVI_BUT:
            stor='RamiLevi'
        else:
            stor='yohananof'

        response=requests.get('https://yonilabell.pythonanywhere.com/getsubstores/'+stor)
        substores=json.loads(response.content)

        myinline_keyboard=[]
        for subid , subadd in substores.items():
            myinline_keyboard.append([InlineKeyboardButton(text=str(subadd), callback_data=stor+'/'+subid.zfill(3))])
        keyboard = InlineKeyboardMarkup(inline_keyboard=myinline_keyboard)
        bot.sendMessage(chat_id,SELECT_BRANCH_REP,reply_markup=keyboard)

    elif txmsg==LISTBUT :
        bot.sendMessage(chat_id,LISTBUT,reply_markup=LISTKEYBOERD)

    elif txmsg==ADD_BRANCHE_BUT:
        bot.sendMessage(chat_id,'ADD',reply_markup=MAINKEYBOARD)

    elif txmsg==DEL_BRANCHE_BUT:
        bot.sendMessage(chat_id,'DEL',reply_markup=MAINKEYBOARD)

    elif txmsg==ALL_MY_BRANCHE_BUT:
        mystores=usersDB.get_stores(chat_id)
        if(mystores):
            reply=''
            for store in mystores:
                reply+=get_and_format_store(store)
        else:
            reply=NO_STORE_REP
        bot.sendMessage(chat_id,reply,reply_markup=BRANCHES_KEYBOERD)


    elif txmsg.isdigit():

        itemid=txmsg

        reply=MyGetItemAPI(chat_id,itemid)

        bot.sendMessage(chat_id,reply,reply_markup=MAINKEYBOARD)

    elif (("Here is the text" in txmsg) and (txmsg[18:].isdigit())):

        itemid=txmsg[18:]

        reply=MyGetItemAPI(chat_id,itemid)

        bot.sendMessage(chat_id,reply,reply_markup=MAINKEYBOARD)


    elif(isHe(txmsg)):
        reply= txmsg
        response=requests.get("https://yonilabell.pythonanywhere.com/getitembymame/"+ txmsg)
        itemname=json.loads(response.content)
        if len(itemname)==0:
            bot.sendMessage(chat_id,NOT_FOUNDANS)
        else:
            myinline_keyboard=[]
            for x, y in itemname.items():
                myinline_keyboard.append([InlineKeyboardButton(text=str(x), callback_data=str(y))])
            keyboard = InlineKeyboardMarkup(inline_keyboard=myinline_keyboard)


            bot.sendMessage(chat_id,reply,reply_markup=keyboard)

    #admin use
    elif txmsg == "admin":
        if chat_id=="318861933" :
            bot.sendMessage(chat_id,"hey yoni",reply_markup=ADMIN_KEYBOERD)
        else:
            bot.sendMessage(chat_id,"Unauthorized",reply_markup=MAINKEYBOARD)

    elif txmsg == ALL_USERS_BUT:
        if chat_id=="318861933" :
            r=requests.get("https://yonilabell.pythonanywhere.com/admin/getusers")
            bot.sendMessage(chat_id,r.content,reply_markup=ADMIN_KEYBOERD)
        else:
            bot.sendMessage(chat_id,"Unauthorized",reply_markup=MAINKEYBOARD)

    elif txmsg == CPU_BUT:
        if chat_id=="318861933" :

            username = 'yonilabell'
            token = '7381dcf0c78540bea188304a8db15c4b10d320a0'
            response = requests.get(
                'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
                    username=username
                ),
                headers={'Authorization': 'Token {token}'.format(token=token)}
            )
            if response.status_code == 200:
                res='CPU quota info: '
                res+=str(json.loads(response.content))
            else:
                res=('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

            bot.sendMessage(chat_id,res,reply_markup=ADMIN_KEYBOERD)

        else:
            bot.sendMessage(chat_id,"Unauthorized",reply_markup=MAINKEYBOARD)

    else:
        send_not_found(chat_id)


# func 6
def manage_callback(update):
    chat_id = update["callback_query"]["from"]["id"]
    user_name = update["callback_query"]["from"]["first_name"]
    data = update["callback_query"]["data"]
    msgid=update["callback_query"]["id"]
    if data.isdigit():

        reply=MyGetItemAPI(chat_id,data)

        myinline_keyboard=[[InlineKeyboardButton(text=DEL_FROM_LISTBUT, callback_data='DEL,'+data),InlineKeyboardButton(text=ADD_TO_LISTBUT, callback_data='ADD,'+data)]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=myinline_keyboard)
        bot.sendMessage(chat_id,reply,reply_markup=keyboard)
        bot.answerCallbackQuery(callback_query_id=msgid,text=ADD_DEL_ANS)

    elif "DEL"  in  data or "ADD" in data  :

        itemid=data[4:]
        itemname=MyGetItemNameAPI(itemid)
        action=str(data).split(',')

        if action[0]=='ADD' and itemname:

            r=SQLDB.sqldb(user_name,chat_id,itemid,itemname,"add")
            bot.sendMessage(chat_id,r,reply_markup=LISTKEYBOERD)

        elif action[0]=='DEL' and itemname:

            r=SQLDB.sqldb(user_name,chat_id,itemid,itemname,"delete")
            bot.sendMessage(chat_id,r,reply_markup=LISTKEYBOERD)

        else:
            send_not_found(chat_id)


    elif ('add' not in data) and ('del' not in data):

        reply=get_and_format_store(data)
        myinline_keyboard=[[InlineKeyboardButton(text=ADD_BRANCHE_BUT, callback_data='add,'+data),InlineKeyboardButton(text=DEL_BRANCHE_BUT, callback_data='del,'+data)]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=myinline_keyboard)
        bot.sendMessage(chat_id,reply,reply_markup=keyboard)
        bot.answerCallbackQuery(callback_query_id=msgid,text=ADD_DEL_ANS)

    else:
        bot.answerCallbackQuery(callback_query_id=msgid,text=DONE_ANS)
        action=str(data).split(',')
        if action[0]=='add':
            a=usersDB.add_store(chat_id,str(action[1]))
            bot.sendMessage(chat_id,str(a))
        elif action[0]=='del':
            a=usersDB.del_store(chat_id,str(action[1]))
            bot.sendMessage(chat_id,str(a))


# func 7
def get_and_format_store(store):
        response=requests.get("https://yonilabell.pythonanywhere.com/getstore/"+store)
        astore=json.loads(response.content)
        sname=str(store).split('/')[0]
        reply=str(sname)+' '+ str(astore['0'])
        reply=reply.replace("yohananof",yohananof).replace("RamiLevi",RamiLevi).replace("osherad",osherad)
        return reply+'\n'

# func 8
def send_not_found(chat_id):
    bot.sendMessage(chat_id, NOT_FOUNDANS,reply_markup=MAINKEYBOARD)
