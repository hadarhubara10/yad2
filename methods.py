import json
from tkinter import Button
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery




def check_if_clicked(data ,button ,buttoncb):
    
    if not "✅" in button.text:
        return  InlineKeyboardButton(button.text + "✅", callback_data=buttoncb)
    else:
        return button

def make_unclicked(data ,button ,buttoncb):
    
    if  "✅" in button.text:
        return  InlineKeyboardButton(button.text.removesuffix("✅"), callback_data=buttoncb)
    else:
        return button
def edit_filtered_message(userchoices):
    message_text="נכון לרגע זה בחרת בסינון הבא"+"\n"
    for index ,item in enumerate(userchoices):
        str=""        
        for i in userchoices[item]:
            str+=f"{i}, "
        message_text+=f'{item} - {str}\n'

    return message_text

