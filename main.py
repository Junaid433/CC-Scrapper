import telebot
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
tok = os.environ.get('bot_env')
bot = telebot.TeleBot(tok)

@bot.message_handler(commands=['start'])
def cmds(message):
    bot.reply_to(message,text='Welcome. Hit /cmds or /help for available commands')

@bot.message_handler(commands=['help','cmds'])
def cmds(message):
    bot.reply_to(message,text='''
command - usage
/scr - /scr heckerdrops 100 531462
/scrsk - /scrsk heckerdrops 100
    ''')

@bot.message_handler(commands=['scr'])
def scrape_cc(message):
    try:
        parts = message.text.split()
        if len(parts) == 3:
            chat_id = parts[1]
            limit = parts[2]
            bin = 'All'
        elif len(parts) == 4:
            chat_id = parts[1]
            limit = parts[2]
            bin = parts[3]
        while True:
            raw = requests.get(
            'http://heckerdrops.live:5000/scrapper?chat_id='+chat_id+'&limit='+limit+'&bin='+bin+'',
            timeout = 120 
            ).json() 
            if 'This event loop is already running' in raw:
                time.sleep(5)
                continue
            else:
                break
        cards = raw['cards']
        found = raw['found']
        file = f'x{found} Scrapped.txt'
        if cards is not None:
            with open(file, "w+") as f:
                f.write(cards)
            with open(file, "rb") as f:
                cap = '<b>Scrapped Sucessfully ✅\nTarget -» <code>'+chat_id.upper()+'</code>\nFound -» <code>'+found+'</code>\nBin -» <code>'+bin+'</code>\nREQ BY -» <code>'+message.from_user.first_name+'</code></b>'
                bot.send_document(chat_id=message.chat.id, document=f, caption=cap,parse_mode='HTML')
                os.remove(file)
        elif cards is None:
            bot.reply_to(message,text='No cards were found.')    
    except Exception as e:
        bot.reply_to(message,text=str(e))   

@bot.message_handler(commands=['scrsk'])
def scrape_sk(message):
    try:
        parts = message.text.split()
        chat_id = parts[1]
        limit = parts[2]
        while True:
            raw = requests.get(
            'http://heckerdrops.live:5000/skscrapper?chat_id='+chat_id+'&limit='+limit,
            timeout = 120 
            ).json() 
            if 'This event loop is already running' in raw:
                time.sleep(5)
                continue
            else:
                break    
        cards = raw['sk']
        found = raw['found']
        file = f'x{found} Scrapped.txt'
        if cards is not None:
            with open(file, "w+") as f:
                f.write(cards)
            with open(file, "rb") as f:
                cap = '<b>Scrapped Sucessfully ✅\nTarget -» <code>'+chat_id.upper()+'</code>\nFound -» <code>'+found+'</code>\nREQ BY -» <code>'+message.from_user.first_name+'</code></b>'
                bot.send_document(chat_id=message.chat.id, document=f, caption=cap,parse_mode='HTML')
                os.remove(file)
        elif cards is None:
            bot.reply_to(message,text='No sk were found.')    
    except Exception as e:
        bot.reply_to(message,text=str(e))   

bot.polling()
