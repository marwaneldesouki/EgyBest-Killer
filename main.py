from os import system
system('pip install -r requirements.txt')
system('pip install --upgrade pip')


from telegram import update,Chat
from telegram import forcereply
from telegram.forcereply import ForceReply
import Constants as keys
from telegram.ext import *
import time
import threading
import get_links as GL
import telegram
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup,ForceReply
from keep_alive import keep_alive


bot = telegram.Bot(token=keys.API_KEY)
updater = Updater(keys.API_KEY, use_context=True)
admin_List=[490894370]
keyboard = [[InlineKeyboardButton('Share', url='https://t.me/UdemyD3_Bot'),InlineKeyboardButton('Donate', url='https://www.paypal.com/paypalme/deso163')]]
reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True,one_time_keyboard = True)


def is_Member(userId):
    is_mb = bot.get_chat_member("@EgyBestKiller_Community",userId)
    if(is_mb['status'] != "left"):
        return True
    else:
        return False

def get_User(update):
    user = update.message.from_user
    return user

def start_command(update, context):
   usr = get_User(update)
   if(is_Member(usr['id']) or 1087968824 == usr['id']): 
    if(usr['id'] in admin_List and (update.message.chat['type']=='private')):
      buttons = [
     [f"/stop_bot_{st_off_on}"]]

    context.bot.send_message(chat_id=update.message.chat_id,text=f"EgyBestKiller_Bot🤖 في {usr['username']} مرحبا :🇵🇸\nDeso هذا البوت صنع ب ❤️ من قبل\n💁‍♂️اذا أردت المساعدة من فضلك\n/help 👈<- أضغط هنا\n\n🇬🇧: Welcome {usr['username']} to UdemyD3_Bot🤖\nThis Bot Made With ❤️ By Deso\nIf u want need please💁‍♂️\nClick here👉-> /help",reply_markup=reply_markup)
    keyboardx = ReplyKeyboardMarkup(buttons, resize_keyboard=True, selective = False,one_time_keyboard = True)
    context.bot.send_message(chat_id=update.message.chat_id,text="🔥👆", reply_markup=keyboardx)
   else:
        context.bot.send_message(chat_id=update.message.chat_id,text=f"رجاء🙏:\nيجب أن تكون مشترك في الجروب الخاص بالبوت📑\nلأستعمال البوت🤖.\nرابط القناة:\nt.me/udemyd3bot")
           

def help_command(update, context):
    update.message.reply_text('help')

def update_command(update, context):
    global st_off_on
    if(R.stop_bot):
        R.stop_bot=False
        st_off_on = "OFF"
    else:  
        R.stop_bot=True
        st_off_on = "ON"
    buttons = [
     [f"/stop_bot_{st_off_on}"]]
    keyboardx = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text("update Status is updated", reply_markup=keyboardx)
###########

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def handle_message(update, context):
    usr = get_User(update)
    if(is_Member(usr['id']) or 1087968824 == usr['id']):
        text = str(update.message.text).lower()
        print(text)
        arrlist = GL.ShowSuggestions(text)
        try:
            if(arrlist.__len__()!=0):
                button_list = []
                for movie_name,movie_link in arrlist:
                    button_list.append([InlineKeyboardButton(movie_name, callback_data = str(movie_link))])
                reply_markup=InlineKeyboardMarkup(button_list)
                bot.send_message(chat_id=update.message.chat_id, text=':أختر أسم الفلم',reply_markup=reply_markup)
            else:
                 threadx = threading.Thread(target=send_CourseList(update,arrlist))
                 threadx.start()
        except:
            if(update.message.chat['type']=='private'):
                error(update,context)
    else:
            context.bot.send_message(chat_id=update.message.chat_id,text=f"رجاء🙏:\nيجب أن تكون مشترك في الجروب الخاص بالبوت📑\nلأستعمال البوت🤖.\nرابط القناة:\nt.me/udemyd3bot")


def error(update, context):
  try:
    print(f"Update {update} caused error {context.error}")
    update.message.reply_text(ar['error'])
  except:
    print("error")

def ShowCallBack(update,context):
    text = str(update.callback_query.data).lower()
    if(text.__contains__("movie")):
        bot.send_message(chat_id=update.callback_query.message.chat.id, text=GL.get_MovieDetails(text))
    else:
        bot.send_message(chat_id=update.callback_query.message.chat.id, text=GL.get_SeriesDetails(text))
        
def main():
    print("Bot Started")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler(['stop_bot_off', 'stop_bot_on'], update_command))
    dp.add_handler(CallbackQueryHandler(ShowCallBack))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)
    time.sleep(1)
    updater.start_polling()
    updater.idle()


keep_alive()
t2 = threading.Thread(target=main())
t2.start()
