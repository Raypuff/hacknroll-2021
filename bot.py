#telegram bot extension
from telegram.ext import Filters, MessageHandler, CommandHandler, Updater
from pprint import pformat

#tesseract extensions
from PIL import Image
import pytesseract
import cv2
import os

#emojify extensions
#from emoji import UNICODE_EMOJI as emojis, emojize, demojize
#from fuzzywuzzy import process as fuzzy_match
#import nltk
#import random
#import re
#import sys

#stemmer = nltk.PorterStemmer()
#emoji_names = list(map(demojize, emojis))
#pos_to_filter = ["PRP", "CC", "TO"]
#flags_to_filter = ["1f1e", "1f1f", "1f3f"]

state_dict = {}
#{'user_key': 'default/ocr/emojify'}

BOT_TOKEN = '1549113548:AAE-BKExAkN-CvXPMDCUl10XJS5ba0ncaos'
updater = Updater(token=BOT_TOKEN, use_context=True)

def loading(update, context):
    user_key = str(update.effective_chat.id)
    context.bot.send_message(
        chat_id = user_key,
        text = """
weceived! pwocessing youw copy pasta fow you pwease wait...
"""
    )

def pastify(file_name):
    image = cv2.imread(file_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.threshold(gray, 0, 255,
    cv2.THRESH_BINARY | cv2. THRESH_OTSU)[1]

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text

def uwuify(text):
    result = text.lower()
    result = result.replace("l", "w")
    result = result.replace("r", "w")
    result = result.replace("you", "uwu")
    result = result.replace("is", "ish")
    result = result.replace("when", "whewn")
    result = result.replace("it", "iwt")
    result = result.replace("and", "awnd")
    result = result.replace("been", "bewn")
    result = result.replace("not", "nowt")
    result = result.replace("just", "juwst")
    result = result.replace("can", "cawn")
    result = result.replace("one", "owne")
    result = result.replace("don't", "down't")
    result = result.replace("can't", "cawn't")
    return result

def emojify(text):
    word_list = text.split()
    def add_emoji(word):
        if nltk.pos_tag([word])[0][1] in pos_to_filter:
            return word
        stem = stemmer.stem(word)
        (match_name, match_value) = fuzzy_match.extractOne(stem, emoji_names)
        if match_value < 75:
            return word
        emoji_name = match_name
        emoji = emojize(emoji_name)
        if any(flag in emoji.encode("unicode-escape").decode("ASCII") for flag in flags_to_filter) and match_value != 100:
            return word
        return word + " " + random.randint(1,3) * emoji
    emojipasta = " ".join(map(add_emoji, word_list))
    return emojipasta

def handler(update, context):
    user_key = str(update.effective_chat.id)
    text_reply = update.effective_message.text
    username = update.effective_chat.username
    date = update.effective_message.date.strftime('%c') 

    #print(pformat(update.to_dict()))

    if user_key not in state_dict or text_reply == '/start':
        state_dict[user_key] = 'default'

        context.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = """
wewcome to 'me and the boys copypasta bot' uwu
type /help fow a wist of usefuw commands OwO
"""
        )  
    
    elif state_dict[user_key] == 'default':
        if text_reply == '/help':
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = """
/start - youw jouwney begins hewe uwu
/help - a wist of usefuw commands OwO
/ocr - tuwn any image with text into copy-pasting materiaw hehexD
/uwuify - tuwn any text into uwu material rAwr :3
/emojify - tuwn any text into copypasta materiaw XD
"""
            )

        elif text_reply == '/ocr':
            state_dict[user_key] = 'ocr'
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = """
send me an image with text (prefewably an uncomprwessed file) and i'ww tuwn iwt intwo copy-pasting materiaw hehe
"""
            )

        elif text_reply == '/uwuify':
            state_dict[user_key] = 'uwuify'
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = """
send me text thawt uwu wawnt me tuwu beautify awnd uwuify fow uwu
"""
            )

        elif text_reply == '/emojify':
#            state_dict[user_key] = 'emojify'
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = """
uwu this pawt of me ish not weady yet b-but i pwomise i'm twying o-okay!!
"""
#send me text thawt uwu wawnt me tuwu emojify to copypasta worthy materiaw for uwu

            )

        else:
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = """
that is nyot a vawid command
pwease type /help for a wist of usefuw commands
"""
            )

    elif state_dict[user_key] == 'ocr':
   
        if text_reply == '/exit':
            state_dict[user_key] = 'default'
            context.bot.send_message(
                            chat_id = update.effective_chat.id,
                            text = """
exiting ocr mode uwu...
"""
                )
        elif len(update.effective_message.photo) > 0 or update.effective_message.document is not None:
            loading(update, context) 
            file_id = ''
            if len(update.effective_message.photo) > 0:
                file_id = str(update.effective_message.photo[0].file_id)
            elif update.effective_message.document is not None:
                file_id = str(update.effective_message.document.file_id)

            file_path = context.bot.getFile(file_id)        
            photo_file = file_path.download('pasta.png')
            copypasta = pastify('pasta.png')
            
            log = "{x}: \n@{y} processed the following in ocr mode:\n{z}".format(x = date, y = username, z = copypasta)
            print(log)

            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "hewe is youw copypasta " + username + "!! hope you wike it uwu"
                )
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = copypasta
                )
            state_dict[user_key] = 'default'
            context.bot.send_message(
                            chat_id = update.effective_chat.id,
                            text = """
exiting ocr mode uwu...
"""
                )
        else:
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = """
thawt iws nowt an image ow an uncompwessed file :( pwease twy again ow type /exit tu exit ocr mode orz
"""
                )

    elif state_dict[user_key] == 'uwuify':
        if text_reply == '/exit':
            state_dict[user_key] = 'default'
            context.bot.send_message(
                            chat_id = update.effective_chat.id,
                            text = """
exiting uwuify mode OwO...
""" 
                )
        elif text_reply[0] == '/':
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = """
thawt iws nowt an vawid command... pwease twy again ow type /exit tu exit uwuify mode orz
"""
                )
        else:
            result = uwuify(text_reply)
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "hewe is youw uwuified message " + username + "!! hope you wike it xD"
                )
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = result
                )
            log = "{x}: \n@{y} processed the following in uwuify mode:\n{z}".format(x = date, y = username, z = result)
            print(log)
            state_dict[user_key] = 'default'
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = "exiting uwuifiy mode ^w^"
                )

    elif state_dict[user_key] == 'emojify':
        if text_reply[0] == '/':
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = """
thawt iws nowt an vawid command... pwease twy again ow type /exit tu exit emojify mode :3
"""
                )
        else:
            result = emojify(text_reply)
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = result
                )
            

updater.dispatcher.add_handler(MessageHandler(Filters.all, handler))
updater.start_polling()
print("the boys are making pasta...")
